/* greenserver.be — panier commun (Cloudflare Worker + KV)

   La page https://greenserver.be/share/ parle à ce Worker. Les fichiers sont stockés dans un espace KV,
   le mot de passe est vérifié ici, côté serveur : il n'apparaît jamais dans le code du site.

   Routes (toutes demandent l'en-tête X-Password, sauf OPTIONS) :
     GET    /files       liste des fichiers  (avec X-Admin-Password : dit aussi si le mot de passe admin est bon)
     POST   /files       dépôt : corps = le fichier brut, en-tête X-Filename = nom encodé (encodeURIComponent)
     GET    /files/<id>  téléchargement
     DELETE /files/<id>  suppression, avec X-Admin-Password (désactivée si ADMIN_PASSWORD n'est pas défini)

   Réglages du Worker (Cloudflare > Workers > ce Worker > Settings) :
     FILES            liaison vers l'espace KV (Bindings > KV namespace)            obligatoire
     PASSWORD         mot de passe commun (Variables and Secrets > Secret)           obligatoire
     ADMIN_PASSWORD   mot de passe pour supprimer des fichiers (Secret)              facultatif
     ALLOWED_ORIGINS  sites autorisés, séparés par des virgules (Text)               facultatif
                      par défaut : https://greenserver.be,https://www.greenserver.be
     MAX_MB           taille maximale d'un fichier en Mo, 25 au plus (Text)          facultatif, 25 par défaut
*/

const KV_MAX_BYTES = 25 * 1024 * 1024;           // limite d'une valeur KV
const DEFAULT_ORIGINS = "https://greenserver.be,https://www.greenserver.be";

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const allowed = String(env.ALLOWED_ORIGINS || DEFAULT_ORIGINS).split(",").map((s) => s.trim()).filter(Boolean);
    const origin = req.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
      "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "X-Password, X-Admin-Password, X-Filename, Content-Type",
      "Access-Control-Expose-Headers": "Content-Disposition",
      "Access-Control-Max-Age": "86400",
      "Vary": "Origin"
    };
    const json = (data, status = 200) => new Response(JSON.stringify(data), {
      status, headers: { ...cors, "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }
    });
    const fail = (status, code) => json({ error: code }, status);

    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (!env.FILES) return fail(500, "no_kv_binding");
    if (!env.PASSWORD) return fail(500, "no_password_set");

    const parts = url.pathname.split("/").filter(Boolean);       // ["files"] ou ["files", "<id>"]
    if (parts[0] !== "files" || parts.length > 2) return fail(404, "not_found");

    if (!(await same(req.headers.get("X-Password") || "", env.PASSWORD))) {
      await sleep(700);                                           // freine les essais en série
      return fail(401, "bad_password");
    }

    const id = parts[1];
    try {
      if (!id) {
        if (req.method === "GET") return await listFiles(req, env, json);
        if (req.method === "POST") return await upload(req, env, json, fail);
        return fail(405, "method_not_allowed");
      }
      if (!/^[a-z0-9]{10,40}$/.test(id)) return fail(404, "not_found");
      if (req.method === "GET") return await download(id, env, cors, fail);
      if (req.method === "DELETE") return await remove(req, id, env, json, fail);
      return fail(405, "method_not_allowed");
    } catch (e) {
      return json({ error: "server_error", detail: String(e && e.message || e).slice(0, 200) }, 500);
    }
  }
};

/* ---------- routes ---------- */

async function listFiles(req, env, json) {
  const files = [];
  let cursor;
  do {
    const page = await env.FILES.list({ prefix: "f:", cursor });
    for (const k of page.keys) {
      const m = k.metadata || {};
      files.push({ id: k.name.slice(2), name: m.n || k.name.slice(2), size: m.s || 0, type: m.t || "", date: m.d || "" });
    }
    cursor = page.list_complete ? null : page.cursor;
  } while (cursor);
  files.sort((a, b) => String(b.date).localeCompare(String(a.date)));

  const adminHeader = req.headers.get("X-Admin-Password");
  const out = { files, maxBytes: maxBytes(env), canDelete: !!env.ADMIN_PASSWORD };
  if (adminHeader !== null) {
    out.admin = !!env.ADMIN_PASSWORD && await same(adminHeader, env.ADMIN_PASSWORD);
    if (!out.admin) await sleep(700);
  }
  return json(out);
}

async function upload(req, env, json, fail) {
  const max = maxBytes(env);
  const declared = Number(req.headers.get("Content-Length") || 0);
  if (declared > max) return fail(413, "too_large");

  let name = "";
  try { name = decodeURIComponent(req.headers.get("X-Filename") || ""); } catch (e) { name = ""; }
  name = cleanName(name);
  if (!name) return fail(400, "no_file_name");

  const body = await req.arrayBuffer();
  if (!body.byteLength) return fail(400, "empty_file");
  if (body.byteLength > max) return fail(413, "too_large");

  const type = String(req.headers.get("Content-Type") || "application/octet-stream").slice(0, 100);
  const id = Date.now().toString(36) + randomId(10);
  const meta = { n: name, s: body.byteLength, t: type, d: new Date().toISOString() };
  try {
    await env.FILES.put("f:" + id, body, { metadata: meta });
  } catch (e) {
    return fail(507, "storage_full_or_daily_limit");             // 1 Go plein ou 1000 écritures/jour atteintes
  }
  return json({ file: { id, name, size: meta.s, type, date: meta.d } }, 201);
}

async function download(id, env, cors, fail) {
  const r = await env.FILES.getWithMetadata("f:" + id, { type: "stream" });
  if (!r || r.value === null) return fail(404, "not_found");
  const m = r.metadata || {};
  const headers = {
    ...cors,
    "Content-Type": "application/octet-stream",                  // jamais interprété par le navigateur
    "Content-Disposition": contentDisposition(m.n || id),
    "X-Content-Type-Options": "nosniff",
    "Cache-Control": "no-store"
  };
  if (m.s) headers["Content-Length"] = String(m.s);
  return new Response(r.value, { headers });
}

async function remove(req, id, env, json, fail) {
  if (!env.ADMIN_PASSWORD) return fail(403, "delete_disabled");
  if (!(await same(req.headers.get("X-Admin-Password") || "", env.ADMIN_PASSWORD))) {
    await sleep(700);
    return fail(403, "bad_admin_password");
  }
  await env.FILES.delete("f:" + id);
  return json({ deleted: id });
}

/* ---------- outils ---------- */

function maxBytes(env) {
  const mb = Number(env.MAX_MB);
  return mb > 0 ? Math.min(Math.floor(mb * 1024 * 1024), KV_MAX_BYTES) : KV_MAX_BYTES;
}

// Comparaison sans fuite de temps : on compare les empreintes SHA-256 des deux chaînes.
async function same(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([a, b].map((s) => crypto.subtle.digest("SHA-256", enc.encode(String(s)))));
  const u = new Uint8Array(x), v = new Uint8Array(y);
  let diff = 0;
  for (let i = 0; i < u.length; i++) diff |= u[i] ^ v[i];
  return diff === 0;
}

function cleanName(name) {
  let n = String(name).replace(/[\u0000-\u001f\u007f]/g, "").replace(/[\\/]/g, "_").trim();
  n = n.replace(/^\.+/, "");                                     // pas de nom caché ou « .. »
  if (n.length > 180) {                                          // garde l'extension
    const dot = n.lastIndexOf(".");
    const ext = dot > 0 && n.length - dot <= 12 ? n.slice(dot) : "";
    n = n.slice(0, 180 - ext.length) + ext;
  }
  return n;
}

function contentDisposition(name) {
  const ascii = name.replace(/[^\x20-\x7e]/g, "_").replace(/["\\]/g, "_");
  return "attachment; filename=\"" + ascii + "\"; filename*=UTF-8''" + encodeURIComponent(name);
}

function randomId(n) {
  const abc = "abcdefghijklmnopqrstuvwxyz0123456789";
  const bytes = crypto.getRandomValues(new Uint8Array(n));
  let s = "";
  for (const b of bytes) s += abc[b % abc.length];
  return s;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
