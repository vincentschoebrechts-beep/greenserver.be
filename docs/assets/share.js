/* greenserver.be — File exchange / Panier commun
   Talks to the Cloudflare Worker whose address is in <section id="sh" data-api="…">.
   The password is checked by the Worker; this page only keeps it for the browser session. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const root = $("sh");
  const API = String(root.dataset.api || "").trim().replace(/\/+$/, "");

  /* ---------- language: English by default, French if chosen (?lang=fr or remembered choice) ---------- */
  const TEXTS = {
    en: {
      navTools: "Tools", other: "Français", otherCode: "fr",
      state: "Password protected", title: "File exchange",
      lead: "Drop files here and pick up the ones others have left. Everyone with the password sees and can download every file.",
      offline: "The file exchange isn't connected yet.",
      pwdLabel: "Password", open: "Open", checking: "Checking…",
      dropTitle: "Drop files here", dropHint: (mb) => "or click to choose them. Up to " + mb + " per file.",
      filesTitle: "Files", refresh: "Refresh", lock: "Lock",
      colName: "Name", colSize: "Size", colDate: "Added", colActions: "Actions",
      empty: "No files yet.", count: (n) => n + (n === 1 ? " file" : " files"),
      download: "Download", downloading: "Downloading…", del: "Delete", sure: "Sure?",
      manage: "Manage: delete files", adminLabel: "Administrator password", adminOk: "Enable deleting",
      adminOn: "Deleting is enabled for this session.", adminBad: "Wrong administrator password.",
      adminOff: "Deleting isn't set up on the server.",
      privacy: "Files are stored on Cloudflare and stay until they are deleted. Anyone with the password can download them, so don't drop anything confidential, such as an eWon backup with its passwords in clear.",
      footer: "No cookies, no visitor tracking, fonts served from this site.",
      uploading: (p) => "Uploading… " + p + " %", uploaded: "Added", tooBig: (mb) => "Too large: " + mb + " at most.",
      deleted: (n) => n + " deleted.",
      err: {
        bad_password: "Wrong password.", too_large: "File too large.", empty_file: "Empty file.",
        storage_full_or_daily_limit: "The exchange is full, or today's upload limit is reached. Try again tomorrow.",
        not_found: "This file no longer exists.", network: "Can't reach the server. Check your connection.",
        bad_admin_password: "Wrong administrator password.", delete_disabled: "Deleting isn't set up on the server.",
        other: "Something went wrong"
      },
      locale: "en-GB", units: ["bytes", "KB", "MB", "GB"]
    },
    fr: {
      navTools: "Outils", other: "English", otherCode: "en",
      state: "Protégé par mot de passe", title: "Panier commun",
      lead: "Déposez des fichiers ici et récupérez ceux que d'autres ont laissés. Toute personne qui a le mot de passe voit et peut télécharger tous les fichiers.",
      offline: "Le panier commun n'est pas encore connecté.",
      pwdLabel: "Mot de passe", open: "Ouvrir", checking: "Vérification…",
      dropTitle: "Déposez vos fichiers ici", dropHint: (mb) => "ou cliquez pour les choisir. " + mb + " au plus par fichier.",
      filesTitle: "Fichiers", refresh: "Actualiser", lock: "Verrouiller",
      colName: "Nom", colSize: "Taille", colDate: "Ajouté le", colActions: "Actions",
      empty: "Aucun fichier pour l'instant.", count: (n) => n + (n <= 1 ? " fichier" : " fichiers"),
      download: "Télécharger", downloading: "Téléchargement…", del: "Supprimer", sure: "Sûr ?",
      manage: "Gérer : supprimer des fichiers", adminLabel: "Mot de passe administrateur", adminOk: "Activer la suppression",
      adminOn: "Suppression activée pour cette session.", adminBad: "Mot de passe administrateur incorrect.",
      adminOff: "La suppression n'est pas configurée sur le serveur.",
      privacy: "Les fichiers sont stockés chez Cloudflare et restent jusqu'à ce qu'on les supprime. Toute personne qui a le mot de passe peut les télécharger : n'y déposez rien de confidentiel, comme un backup eWon avec ses mots de passe en clair.",
      footer: "Pas de cookies, pas de pistage, polices servies par ce site.",
      uploading: (p) => "Envoi… " + p + " %", uploaded: "Ajouté", tooBig: (mb) => "Trop gros : " + mb + " au plus.",
      deleted: (n) => n + " supprimé.",
      err: {
        bad_password: "Mot de passe incorrect.", too_large: "Fichier trop gros.", empty_file: "Fichier vide.",
        storage_full_or_daily_limit: "Le panier est plein, ou la limite de dépôts du jour est atteinte. Réessayez demain.",
        not_found: "Ce fichier n'existe plus.", network: "Serveur injoignable. Vérifiez votre connexion.",
        bad_admin_password: "Mot de passe administrateur incorrect.", delete_disabled: "La suppression n'est pas configurée sur le serveur.",
        other: "Une erreur s'est produite"
      },
      locale: "fr-BE", units: ["octets", "Ko", "Mo", "Go"]
    }
  };

  function remember(key, value, store) { try { (store || localStorage).setItem(key, value); } catch (e) {} }
  function recall(key, store) { try { return (store || localStorage).getItem(key); } catch (e) { return null; } }
  function forget(key, store) { try { (store || localStorage).removeItem(key); } catch (e) {} }

  function initialLang() {
    const asked = new URLSearchParams(location.search).get("lang");
    if (asked === "fr" || asked === "en") { remember("langue", asked); return asked; }
    const memo = recall("langue");
    return memo === "fr" ? "fr" : "en";
  }
  let lang = initialLang();
  let T = TEXTS[lang];

  function applyLang() {
    T = TEXTS[lang];
    document.documentElement.lang = lang;
    document.title = T.title + ", greenserver.be";
    document.querySelectorAll("[data-t]").forEach((n) => { const v = T[n.dataset.t]; if (typeof v === "string") n.textContent = v; });
    const link = $("sh-lang");
    link.textContent = T.other; link.lang = link.hreflang = T.otherCode; link.href = "?lang=" + T.otherCode;
    $("sh-tools").href = lang === "fr" ? "../fr/#outils" : "../#tools";
    $("sh-drop-hint").textContent = T.dropHint(size(state.maxBytes));
    if (state.files) renderFiles();
  }
  $("sh-lang").addEventListener("click", (e) => {
    e.preventDefault();
    lang = T.otherCode; remember("langue", lang);
    history.replaceState(null, "", "?lang=" + lang);
    applyLang();
  });

  /* ---------- state ---------- */
  const state = { pwd: recall("panier-mdp", sessionStorage) || "", admin: recall("panier-admin", sessionStorage) || "",
                  isAdmin: false, files: null, maxBytes: 25 * 1024 * 1024 };

  function size(n) {
    const u = T.units; let i = 0; let v = n;
    while (v >= 1024 && i < u.length - 1) { v /= 1024; i++; }
    const s = i === 0 ? String(v) : v.toLocaleString(T.locale, { maximumFractionDigits: v < 10 ? 1 : 0 });
    return s + " " + u[i];
  }
  function when(iso) {
    const d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleString(T.locale, { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
  }
  const errText = (code) => T.err[code] || (T.err.other + (code ? " (" + code + ")." : "."));

  /* ---------- server ---------- */
  async function call(path, opts = {}) {
    const headers = Object.assign({ "X-Password": state.pwd }, opts.headers || {});
    let res;
    try { res = await fetch(API + path, Object.assign({}, opts, { headers, cache: "no-store" })); }
    catch (e) { const err = new Error("network"); err.code = "network"; throw err; }
    if (!res.ok) {
      let code = "http_" + res.status;
      try { code = (await res.json()).error || code; } catch (e) {}
      const err = new Error(code); err.code = code; err.status = res.status; throw err;
    }
    return res;
  }

  async function loadList() {
    const headers = state.admin ? { "X-Admin-Password": state.admin } : {};
    const data = await (await call("/files", { headers })).json();
    state.files = data.files || [];
    state.maxBytes = data.maxBytes || state.maxBytes;
    state.isAdmin = !!data.admin;
    if (state.admin && !data.admin) { state.admin = ""; forget("panier-admin", sessionStorage); }
    $("sh-admin").hidden = !data.canDelete;
    $("sh-drop-hint").textContent = T.dropHint(size(state.maxBytes));
    renderFiles();
    return data;
  }

  /* ---------- views ---------- */
  function show(view) {
    $("sh-off").hidden = view !== "off";
    $("sh-gate").hidden = view !== "gate";
    $("sh-app").hidden = view !== "app";
  }

  function button(text, cls, onClick) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "btn small " + cls; b.textContent = text;
    b.addEventListener("click", onClick);
    return b;
  }

  function renderFiles() {
    const tbody = $("sh-tbody");
    tbody.replaceChildren();
    const files = state.files || [];
    $("sh-count").textContent = T.count(files.length);
    $("sh-empty").hidden = files.length > 0;
    for (const f of files) {
      const tr = document.createElement("tr");
      const name = document.createElement("td"); name.className = "sh-name"; name.textContent = f.name;
      const sz = document.createElement("td"); sz.className = "sh-num"; sz.textContent = size(f.size);
      const dt = document.createElement("td"); dt.className = "sh-num"; dt.textContent = when(f.date);
      const act = document.createElement("td"); act.className = "sh-act";
      act.append(button(T.download, "", (e) => downloadFile(f, e.currentTarget)));
      if (state.isAdmin) act.append(button(T.del, "ghost danger", (e) => deleteFile(f, e.currentTarget)));
      tr.append(name, sz, dt, act);
      tbody.append(tr);
    }
  }

  function status(text) { $("sh-status").textContent = text || ""; }

  /* ---------- actions ---------- */
  async function downloadFile(f, btn) {
    btn.disabled = true; btn.textContent = T.downloading; status("");
    try {
      const blob = await (await call("/files/" + encodeURIComponent(f.id))).blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a"); a.href = url; a.download = f.name;
      document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    } catch (e) {
      if (e.code === "bad_password") return lockOut(e.code);
      status(errText(e.code));
      if (e.code === "not_found") loadList().catch(() => {});
    } finally { btn.disabled = false; btn.textContent = T.download; }
  }

  async function deleteFile(f, btn) {
    if (btn.dataset.armed !== "1") {                      // two clicks to delete
      btn.dataset.armed = "1"; btn.textContent = T.sure;
      setTimeout(() => { if (btn.isConnected) { btn.dataset.armed = ""; btn.textContent = T.del; } }, 3500);
      return;
    }
    btn.disabled = true;
    try {
      await call("/files/" + encodeURIComponent(f.id), { method: "DELETE", headers: { "X-Admin-Password": state.admin } });
      state.files = state.files.filter((x) => x.id !== f.id);
      renderFiles(); status(T.deleted(f.name));
    } catch (e) {
      if (e.code === "bad_password") return lockOut(e.code);
      status(errText(e.code)); btn.disabled = false;
    }
  }

  function uploadOne(file) {
    const li = document.createElement("li");
    const nm = document.createElement("span"); nm.className = "sh-up-name"; nm.textContent = file.name;
    const st = document.createElement("span"); st.className = "sh-up-state";
    const bar = document.createElement("progress"); bar.max = 100; bar.value = 0;
    li.append(nm, bar, st);
    $("sh-uploads").prepend(li);

    if (file.size > state.maxBytes) { li.className = "bad"; bar.remove(); st.textContent = T.tooBig(size(state.maxBytes)); return Promise.resolve(); }
    if (file.size === 0) { li.className = "bad"; bar.remove(); st.textContent = T.err.empty_file; return Promise.resolve(); }

    return new Promise((resolve) => {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", API + "/files");
      xhr.setRequestHeader("X-Password", state.pwd);
      xhr.setRequestHeader("X-Filename", encodeURIComponent(file.name));
      xhr.setRequestHeader("Content-Type", file.type || "application/octet-stream");
      xhr.upload.onprogress = (e) => { if (e.lengthComputable) { const p = Math.round(e.loaded / e.total * 100); bar.value = p; st.textContent = T.uploading(p); } };
      xhr.onload = () => {
        bar.remove();
        let data = {}; try { data = JSON.parse(xhr.responseText); } catch (e) {}
        if (xhr.status === 201 && data.file) {
          li.className = "ok"; st.textContent = T.uploaded;
          state.files = [data.file].concat((state.files || []).filter((x) => x.id !== data.file.id));
          renderFiles();
        } else if (data.error === "bad_password") {
          lockOut("bad_password");
        } else {
          li.className = "bad"; st.textContent = errText(data.error || "http_" + xhr.status);
        }
        resolve();
      };
      xhr.onerror = () => { bar.remove(); li.className = "bad"; st.textContent = errText("network"); resolve(); };
      xhr.send(file);
    });
  }
  async function uploadAll(list) { for (const f of list) await uploadOne(f); }

  function lockOut(code) {
    state.pwd = ""; state.admin = ""; state.isAdmin = false; state.files = null;
    forget("panier-mdp", sessionStorage); forget("panier-admin", sessionStorage);
    $("sh-uploads").replaceChildren(); status("");
    show("gate");
    $("sh-gate-status").textContent = code ? errText(code) : "";
    $("sh-pwd").value = ""; $("sh-pwd").focus();
  }

  async function unlock(pwd) {
    state.pwd = pwd;
    $("sh-gate-status").textContent = T.checking;
    try {
      await loadList();
      remember("panier-mdp", pwd, sessionStorage);
      $("sh-gate-status").textContent = "";
      show("app");
      return true;
    } catch (e) {
      state.pwd = ""; forget("panier-mdp", sessionStorage);
      show("gate");
      $("sh-gate-status").textContent = errText(e.code);
      return false;
    }
  }

  /* ---------- events ---------- */
  $("sh-gate").addEventListener("submit", (e) => { e.preventDefault(); const p = $("sh-pwd").value; if (p) unlock(p); });
  $("sh-lock").addEventListener("click", () => lockOut(""));
  $("sh-refresh").addEventListener("click", () => { status(""); loadList().catch((e) => e.code === "bad_password" ? lockOut(e.code) : status(errText(e.code))); });
  $("sh-files").addEventListener("change", (e) => { const l = [...e.target.files]; e.target.value = ""; uploadAll(l); });
  $("sh-admin-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const p = $("sh-adminpwd").value; if (!p) return;
    state.admin = p;
    try {
      const data = await loadList();
      if (data.admin) { remember("panier-admin", p, sessionStorage); $("sh-admin-status").textContent = T.adminOn; $("sh-adminpwd").value = ""; }
      else $("sh-admin-status").textContent = data.canDelete ? T.adminBad : T.adminOff;
    } catch (err) { $("sh-admin-status").textContent = errText(err.code); }
  });

  const drop = $("sh-drop");
  ["dragenter", "dragover"].forEach((t) => window.addEventListener(t, (e) => { e.preventDefault(); if (!$("sh-app").hidden) drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((t) => window.addEventListener(t, (e) => { e.preventDefault(); if (t === "drop" || e.target === document.documentElement) drop.classList.remove("over"); }));
  window.addEventListener("drop", (e) => {
    drop.classList.remove("over");
    if (!$("sh-app").hidden && e.dataTransfer && e.dataTransfer.files.length) uploadAll([...e.dataTransfer.files]);
  });

  /* ---------- start ---------- */
  applyLang();
  if (!API) show("off");
  else if (state.pwd) unlock(state.pwd);
  else show("gate");
})();
