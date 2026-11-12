/* greenserver.be — eWon Backup Cleaner
   Swaps the device-specific "#_6_…" encrypted values of an eWon backup (firmware >= 14.9s3 / 22.1s3)
   for a clear password, so the same backup can be restored on other eWons.
   Everything runs in the browser: files are read and rewritten locally, nothing is sent to greenserver.be. */

/* ======================= Core (no DOM) ======================= */
const EwonCore = (() => {
  "use strict";
  const SCAN_EXT = /\.(txt|csv|ini|cfg|conf|xml|json)$/i;
  // eWon encrypted value: #_<n>_<base64>, at the start of a value (after ':' ';' '"' '=' or line start)
  const TOKEN_RE = /(?<=^|[:;"=])#_(\d+)_[^;"\s]+/g;

  const PARAMS = {
    FtpPassword:    { label: "FTP password" },
    SmtpAuthPass:   { label: "SMTP password" },
    DMClientPwd:    { label: "Data Mailbox" },
    VPNSecretKey:   { label: "Talk2M VPN key", action: "delete",
                      note: "Line removed by default: each eWon has its own key, the target keeps its own." },
    PPPClPassword1: { label: "ISP / PPP 1" },
    PPPClPassword2: { label: "ISP / PPP 2" },
    CBDDnsPass:     { label: "DynDNS" },
    DefAdmPass:     { label: "Factory admin password", action: "delete",
                      note: "Line removed by default: the target eWon keeps its own factory password (the one on its label)." },
    WANPxyPass:     { label: "WAN proxy" },
    AdslPass:       { label: "ADSL" },
    PIN:            { label: "SIM PIN", action: "delete",
                      note: "Line removed by default: a wrong PIN could lock the SIM card." },
    WifiPSK:        { label: "Wi-Fi key" },
    UsbIpPwd:       { label: "USB/IP" },
    BoltCfgPassword:{ label: "Bolt" }
  };

  /* ---------- bytes <-> text (latin1 keeps every byte) ---------- */
  function latin1Decode(u8) {
    let s = "";
    for (let i = 0; i < u8.length; i += 0x8000)
      s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
    return s;
  }
  function latin1Encode(s) {
    const u8 = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) {
      const c = s.charCodeAt(i);
      if (c > 255) throw new Error("Character can't be encoded: " + s[i]);
      u8[i] = c;
    }
    return u8;
  }
  const basename = (p) => p.replace(/\/+$/, "").split("/").pop();

  function looksText(u8) {
    const n = Math.min(u8.length, 65536);
    for (let i = 0; i < n; i++) if (u8[i] === 0) return false;
    return true;
  }
  const isScannable = (name, data) => SCAN_EXT.test(name) && data.length < 50e6 && looksText(data);

  /* ---------- eWon CSV line (separator ;) ---------- */
  function splitFields(s) {
    const out = []; let i = 0; const n = s.length;
    for (;;) {
      const start = i; let value = "", quoted = false;
      if (s[i] === '"') {
        quoted = true; i++;
        while (i < n) {
          if (s[i] === '"') { if (s[i + 1] === '"') { value += '"'; i += 2; continue; } i++; break; }
          value += s[i++];
        }
        while (i < n && s[i] !== ";") value += s[i++];
      } else {
        while (i < n && s[i] !== ";") value += s[i++];
      }
      out.push({ value, quoted, start, end: i });
      if (i >= n) break;
      i++;
      if (i === n) { out.push({ value: "", quoted: false, start: i, end: i }); break; }
    }
    return out;
  }

  /* ---------- finding the encrypted values ---------- */
  function scanText(text, opts) {
    const includeOld = !!(opts && opts.includeOld);
    const parts = text.split(/(\r\n|\n|\r)/);
    const lines = [];
    for (let k = 0; k < parts.length; k += 2) lines.push({ c: parts[k], eol: parts[k + 1] || "" });
    const findings = [];
    let header = null, section = null;

    lines.forEach((ln, i) => {
      const c = ln.c;
      if (/^:[A-Za-z]/.test(c)) { section = c.slice(1).trim(); header = null; return; }
      const kv = /^([A-Za-z_][\w.]*):/.exec(c);
      let fields = null;
      if (!kv && c.includes(";")) {
        fields = splitFields(c);
        if (fields.length >= 3 && fields.every((f) => f.quoted)) { header = fields.map((f) => f.value); return; }
      }
      TOKEN_RE.lastIndex = 0;
      let m;
      while ((m = TOKEN_RE.exec(c))) {
        const version = +m[1];
        if (version !== 6 && !includeOld) continue;
        const f = { line: i, start: m.index, end: m.index + m[0].length, token: m[0], version,
                    section, kind: "other", label: "Encrypted value", sub: section ? "section " + section : "",
                    canDelete: false, defaultAction: "replace", note: "", isAdm: false };
        if (kv && m.index >= kv[0].length) {
          const p = PARAMS[kv[1]];
          Object.assign(f, { kind: "kv", key: kv[1], label: p ? p.label : kv[1], sub: kv[1],
                             canDelete: true, defaultAction: (p && p.action) || "replace", note: (p && p.note) || "" });
        } else if (fields) {
          const idx = fields.findIndex((x) => m.index >= x.start && m.index <= x.end);
          let login = null;
          if (header) {
            const li = header.findIndex((h) => /^login$/i.test(h));
            if (li >= 0 && fields[li]) login = fields[li].value;
          } else if (idx === 4 && fields[3] && /^\d+$/.test(fields[0].value)) {
            login = fields[3].value; // user line: Id;FirstName;LastName;Login;Password;…
          }
          const isAdm = login !== null && login.toLowerCase() === "adm";
          Object.assign(f, { kind: "csv", col: idx, login, isAdm,
                             label: login !== null ? "User “" + login + "”" : "Field " + (idx + 1),
                             sub: (header && header[idx]) || (login !== null ? "Password" : f.sub),
                             canDelete: login !== null && !isAdm });
        }
        findings.push(f);
      }
    });

    // comcfg.txt: always offer a PIN row, even when the PIN isn't #_6 encrypted or is missing
    if (opts && opts.pinRow && !findings.some((f) => f.key === "PIN")) {
      const base = { kind: "kv", key: "PIN", label: PARAMS.PIN.label, sub: "PIN", version: 0, section: null,
                     defaultAction: "keep", note: "", isAdm: false };
      const i = lines.findIndex((ln) => /^PIN:/.test(ln.c));
      if (i >= 0) findings.push(Object.assign(base, { synthetic: "clear", line: i, start: 4, end: lines[i].c.length,
                                                      token: lines[i].c.slice(4), canDelete: true }));
      else findings.push(Object.assign(base, { synthetic: "missing", line: lines.length, start: 0, end: 0,
                                               token: "", canDelete: false }));
    }
    return { lines, findings };
  }

  function validateValue(v) {
    if (v === "") return "Empty value (pick “Clear” if that's what you want)";
    if (!/^[\x20-\x7E]*$/.test(v)) return "Printable ASCII characters only";
    if (/[";]/.test(v)) return "The characters \" and ; aren't allowed";
    return null;
  }
  function validatePin(v) {
    if (v === "") return "Empty PIN (pick “Clear” or “Remove line”)";
    if (!/^\d{4,8}$/.test(v)) return "The PIN must be 4 to 8 digits";
    return null;
  }

  /* ---------- applying the choices ---------- */
  function applyText(scan) {
    const byLine = new Map();
    for (const f of scan.findings) {
      if (!byLine.has(f.line)) byLine.set(f.line, []);
      byLine.get(f.line).push(f);
    }
    let out = ""; const changes = [];
    scan.lines.forEach((ln, i) => {
      const fs = byLine.get(i);
      if (!fs) { out += ln.c + ln.eol; return; }
      if (fs.some((f) => f.action === "delete")) { changes.push({ line: i + 1, before: ln.c, after: null }); return; }
      let c = ln.c;
      fs.slice().sort((a, b) => b.start - a.start).forEach((f) => {
        if (f.action === "keep") return;
        const v = f.action === "clear" ? "" : f.value;
        c = c.slice(0, f.start) + v + c.slice(f.end);
      });
      if (c !== ln.c) changes.push({ line: i + 1, before: ln.c, after: c });
      out += c + ln.eol;
    });
    // missing lines to append at the end of the file (e.g. PIN)
    for (const f of scan.findings) {
      if (f.synthetic !== "missing" || f.action !== "replace") continue;
      const eol = (scan.lines.find((ln) => ln.eol) || { eol: "\r\n" }).eol;
      const endedWithEol = out === "" || /(\r\n|\n|\r)$/.test(out);
      const added = f.key + ":" + f.value;
      out += (endedWithEol ? "" : eol) + added + (endedWithEol ? eol : "");
      changes.push({ line: scan.lines.length + (endedWithEol ? 0 : 1), before: null, after: added });
    }
    return { text: out, changes };
  }

  /* ---------- TAR ---------- */
  function readStr(u8, off, len) {
    let s = "";
    for (let i = off; i < off + len && i < u8.length; i++) { if (u8[i] === 0) break; s += String.fromCharCode(u8[i]); }
    return s;
  }
  function readOctal(u8, off, len) {
    if (u8[off] & 0x80) { let v = 0; for (let i = off + 1; i < off + len; i++) v = v * 256 + u8[i]; return v; }
    const s = readStr(u8, off, len).trim();
    return s ? parseInt(s, 8) : 0;
  }
  function headerSum(h) { let s = 0; for (let i = 0; i < 512; i++) s += (i >= 148 && i < 156) ? 32 : h[i]; return s; }
  function isZeroBlock(u8, off) { for (let i = off; i < off + 512; i++) if (u8[i]) return false; return true; }
  function isTar(u8) {
    if (u8.length < 512 || isZeroBlock(u8, 0)) return false;
    return readOctal(u8, 148, 8) === headerSum(u8.subarray(0, 512));
  }
  function parsePax(data) {
    const txt = new TextDecoder("utf-8").decode(data); const rec = {}; let i = 0;
    while (i < txt.length) {
      const sp = txt.indexOf(" ", i); if (sp < 0) break;
      const len = parseInt(txt.slice(i, sp), 10); if (!len) break;
      const r = txt.slice(sp + 1, i + len - 1); const eq = r.indexOf("=");
      if (eq > 0) rec[r.slice(0, eq)] = r.slice(eq + 1);
      i += len;
    }
    return rec;
  }
  const isRegular = (t) => t === "0" || t === "7";

  function parseTar(u8) {
    const entries = []; let off = 0, pendingLong = null, pendingPax = null;
    while (off + 512 <= u8.length) {
      if (isZeroBlock(u8, off)) break;
      const h = u8.subarray(off, off + 512);
      if (readOctal(u8, off + 148, 8) !== headerSum(h))
        throw new Error("Invalid tar archive (bad checksum at byte " + off + ")");
      const type = h[156] === 0 ? "0" : String.fromCharCode(h[156]);
      const size = readOctal(u8, off + 124, 12);
      let name = readStr(u8, off, 100);
      if (readStr(u8, off + 257, 6) === "ustar") { const pre = readStr(u8, off + 345, 155); if (pre) name = pre + "/" + name; }
      const dataLen = "123456".includes(type) ? 0 : size;
      if (off + 512 + dataLen > u8.length) throw new Error("Truncated tar archive");
      const data = u8.subarray(off + 512, off + 512 + dataLen);
      const e = { off, type, size, data, rawLen: 512 + Math.ceil(dataLen / 512) * 512 };
      if (type === "L" || type === "K") { e.meta = true; if (type === "L") pendingLong = readStr(data, 0, data.length); }
      else if (type === "x") { e.meta = true; const p = parsePax(data); e.pax = p; if (p.path) pendingPax = p.path; }
      else if (type === "g") { e.global = true; }
      else {
        e.name = pendingPax || pendingLong || name;
        e.paxSize = entries.length && entries[entries.length - 1].pax && "size" in entries[entries.length - 1].pax;
        pendingLong = pendingPax = null;
      }
      entries.push(e);
      off += e.rawLen;
    }
    return { src: u8, entries, end: off };
  }

  function rebuildEntry(src, e, data) {
    const h = src.slice(e.off, e.off + 512);
    const sz = data.length.toString(8).padStart(11, "0") + "\0";
    if (sz.length > 12) throw new Error("File too large for the tar header");
    for (let i = 0; i < 12; i++) h[124 + i] = sz.charCodeAt(i);
    for (let i = 148; i < 156; i++) h[i] = 32;
    const ck = headerSum(h).toString(8).padStart(6, "0") + "\0 ";
    for (let i = 0; i < 8; i++) h[148 + i] = ck.charCodeAt(i);
    const out = new Uint8Array(512 + Math.ceil(data.length / 512) * 512);
    out.set(h, 0); out.set(data, 512);
    return out;
  }

  // replacements: Map(entry index -> Uint8Array); removed: Set(entry index)
  function buildTar(tar, replacements, removed) {
    const chunks = []; let pending = [];
    tar.entries.forEach((e, i) => {
      if (e.meta) { pending.push(e); return; }
      if (removed && removed.has(i)) { pending = []; return; }
      for (const m of pending) chunks.push(tar.src.subarray(m.off, m.off + m.rawLen));
      pending = [];
      if (replacements && replacements.has(i)) {
        if (e.paxSize) throw new Error("pax tar with extended size isn't supported for " + e.name);
        chunks.push(rebuildEntry(tar.src, e, replacements.get(i)));
      } else chunks.push(tar.src.subarray(e.off, e.off + e.rawLen));
    });
    for (const m of pending) chunks.push(tar.src.subarray(m.off, m.off + m.rawLen));
    let len = chunks.reduce((a, c) => a + c.length, 0) + 1024;
    if (tar.src.length % 10240 === 0) len = Math.ceil(len / 10240) * 10240;
    const out = new Uint8Array(len); let p = 0;
    for (const c of chunks) { out.set(c, p); p += c.length; }
    return out;
  }

  /* ---------- ZIP ---------- */
  const CRC_TABLE = (() => { const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t; })();
  function crc32(u8) { let c = 0xFFFFFFFF; for (let i = 0; i < u8.length; i++) c = CRC_TABLE[(c ^ u8[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
  const isZip = (u8) => u8.length >= 4 && u8[0] === 0x50 && u8[1] === 0x4B && (u8[2] === 3 || u8[2] === 5);
  const isGzip = (u8) => u8.length >= 2 && u8[0] === 0x1F && u8[1] === 0x8B;

  async function streamThrough(u8, format, Ctor) {
    const s = new Blob([u8]).stream().pipeThrough(new Ctor(format));
    return new Uint8Array(await new Response(s).arrayBuffer());
  }
  const inflateRaw = (u8) => streamThrough(u8, "deflate-raw", DecompressionStream);
  const gunzip = (u8) => streamThrough(u8, "gzip", DecompressionStream);

  async function parseZip(u8) {
    const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
    let eocd = -1;
    for (let i = u8.length - 22; i >= Math.max(0, u8.length - 22 - 65535); i--)
      if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
    if (eocd < 0) throw new Error("Invalid ZIP");
    const count = dv.getUint16(eocd + 10, true); let cd = dv.getUint32(eocd + 16, true);
    if (count === 0xFFFF || cd === 0xFFFFFFFF) throw new Error("ZIP64 isn't supported");
    const files = [];
    for (let k = 0; k < count; k++) {
      if (dv.getUint32(cd, true) !== 0x02014b50) throw new Error("Invalid ZIP (central directory)");
      const flags = dv.getUint16(cd + 8, true), method = dv.getUint16(cd + 10, true);
      const csize = dv.getUint32(cd + 20, true);
      const nlen = dv.getUint16(cd + 28, true), xlen = dv.getUint16(cd + 30, true), clen = dv.getUint16(cd + 32, true);
      const lho = dv.getUint32(cd + 42, true);
      const nb = u8.subarray(cd + 46, cd + 46 + nlen);
      const name = (flags & 0x800) ? new TextDecoder("utf-8").decode(nb) : latin1Decode(nb);
      cd += 46 + nlen + xlen + clen;
      if (name.endsWith("/")) continue;
      if (flags & 1) throw new Error("Password-protected ZIP isn't supported (" + name + ")");
      const start = lho + 30 + dv.getUint16(lho + 26, true) + dv.getUint16(lho + 28, true);
      const comp = u8.subarray(start, start + csize);
      let data;
      if (method === 0) data = comp.slice();
      else if (method === 8) data = await inflateRaw(comp);
      else throw new Error("ZIP compression method " + method + " isn't supported (" + name + ")");
      files.push({ name, data });
    }
    return files;
  }

  function buildZip(files) {
    const enc = new TextEncoder(); const d = new Date();
    const time = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
    const date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    const locals = [], centrals = []; let off = 0;
    for (const f of files) {
      const nb = enc.encode(f.name), crc = crc32(f.data), sz = f.data.length;
      const lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x800, true); lh.setUint16(8, 0, true);
      lh.setUint16(10, time, true); lh.setUint16(12, date, true); lh.setUint32(14, crc, true);
      lh.setUint32(18, sz, true); lh.setUint32(22, sz, true); lh.setUint16(26, nb.length, true); lh.setUint16(28, 0, true);
      locals.push(new Uint8Array(lh.buffer), nb, f.data);
      const ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true); ch.setUint16(8, 0x800, true);
      ch.setUint16(10, 0, true); ch.setUint16(12, time, true); ch.setUint16(14, date, true); ch.setUint32(16, crc, true);
      ch.setUint32(20, sz, true); ch.setUint32(24, sz, true); ch.setUint16(28, nb.length, true);
      ch.setUint32(42, off, true);
      centrals.push(new Uint8Array(ch.buffer), nb);
      off += 30 + nb.length + sz;
    }
    const cdSize = centrals.reduce((a, c) => a + c.length, 0);
    const eo = new DataView(new ArrayBuffer(22));
    eo.setUint32(0, 0x06054b50, true); eo.setUint16(8, files.length, true); eo.setUint16(10, files.length, true);
    eo.setUint32(12, cdSize, true); eo.setUint32(16, off, true);
    const all = [...locals, ...centrals, new Uint8Array(eo.buffer)];
    const out = new Uint8Array(all.reduce((a, c) => a + c.length, 0)); let p = 0;
    for (const c of all) { out.set(c, p); p += c.length; }
    return out;
  }

  return { PARAMS, latin1Decode, latin1Encode, basename, isScannable, splitFields, scanText, validateValue, validatePin, applyText,
           isTar, parseTar, buildTar, isRegular, isZip, isGzip, gunzip, parseZip, buildZip, crc32 };
})();
if (typeof module !== "undefined") module.exports = EwonCore;

/* ======================= Page ======================= */
(() => {
  "use strict";
  if (typeof document === "undefined" || !document.getElementById("ew-files")) return;
  const Core = EwonCore;
  const $ = (s, r = document) => r.querySelector(s);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") n.className = v;
      else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
      else if (v === true) n.setAttribute(k, "");
      else if (v !== false && v != null) n.setAttribute(k, v);
    }
    for (const k of kids.flat()) if (k != null) n.append(k.nodeType ? k : document.createTextNode(String(k)));
    return n;
  };

  const opts = { pwd: "adm", pin: "", suffix: "_clear", dropComcfg: false, includeOld: false };
  const items = [];
  let seq = 0;

  /* ---------- per-row rules (PIN apart) ---------- */
  const isPinRow = (x) => x.kind === "kv" && x.key === "PIN";
  const rowError = (x) => x.action !== "replace" ? null : (isPinRow(x) ? Core.validatePin(x.value) : Core.validateValue(x.value));
  function initRow(x) {
    x.custom = false; x.customAction = false;
    if (isPinRow(x)) { x.action = opts.pin ? "replace" : x.defaultAction; x.value = opts.pin; }
    else { x.action = x.defaultAction; x.value = opts.pwd; }
  }
  function pinNote(x) {
    if (x.action === "replace") return (x.synthetic === "missing" ? "PIN line added to comcfg.txt. " : "") +
      "The PIN must match this eWon's SIM card (3 wrong tries lock the SIM).";
    if (x.action === "clear") return "Empty PIN: if the SIM asks for one, the cellular link won't come up.";
    if (x.action === "keep") return x.synthetic === "missing"
      ? "No PIN line in this backup: the eWon keeps its current PIN. Enter a PIN in the settings to add one."
      : "The backup's PIN is kept as it is.";
    return x.synthetic ? "Line removed: the target eWon keeps its current PIN." : Core.PARAMS.PIN.note;
  }
  const isComcfg = (name) => /comcfg/i.test(Core.basename(name));
  const isIgnored = (it, file) => opts.dropComcfg && it.kind !== "txt" && isComcfg(file.name);

  // Reads the settings back from the page (browsers may restore them after a reload or Back)
  function syncOpts() {
    opts.pwd = $("#ew-pwd").value;
    opts.pin = $("#ew-pin").value.trim();
    opts.suffix = $("#ew-suffix").value;
    opts.dropComcfg = $("#ew-dropcom").checked;
    opts.includeOld = $("#ew-old").checked;
    $("#ew-suffix-preview").textContent = opts.suffix;
    $("#ew-pwd").classList.toggle("invalid", !!Core.validateValue(opts.pwd));
    $("#ew-pin").classList.toggle("invalid", opts.pin !== "" && !!Core.validatePin(opts.pin));
    $("#ew-pinwarn").hidden = !(opts.dropComcfg && opts.pin);
  }

  /* ---------- loading ---------- */
  function splitExt(name) {
    const m = /^(.*?)((\.tar)?\.(tar|tgz|gz|zip|txt))$/i.exec(name);
    return m ? [m[1], m[2]] : [name, ""];
  }
  function defaultOutName(it) {
    if (it.kind === "txt") return it.baseName;           // FTP: the name must stay config.txt / comcfg.txt
    const [stem, ext] = splitExt(it.baseName);
    return stem + opts.suffix + (it.kind === "tar" ? ".tar" : (ext || ".zip"));
  }

  function makeTarItem(displayName, baseName, u8) {
    const tar = Core.parseTar(u8);
    const files = []; let fileCount = 0;
    tar.entries.forEach((e, idx) => {
      if (e.meta || e.global || !Core.isRegular(e.type)) return;
      fileCount++;
      if (Core.isScannable(e.name, e.data)) files.push({ ref: idx, name: e.name, text: Core.latin1Decode(e.data) });
    });
    const tarBase = /\.(tgz|tar\.gz|gz)$/i.test(baseName) ? baseName.replace(/\.(tgz|tar\.gz|gz)$/i, ".tar") : baseName;
    return { kind: "tar", displayName, baseName: tarBase, tar, files, fileCount,
             comcfgRefs: tar.entries.map((e, i) => (!e.meta && e.name && Core.basename(e.name).toLowerCase() === "comcfg.txt") ? i : -1).filter((i) => i >= 0) };
  }
  function makeZipItem(displayName, baseName, zfiles) {
    const files = [];
    zfiles.forEach((f, idx) => { if (Core.isScannable(f.name, f.data)) files.push({ ref: idx, name: f.name, text: Core.latin1Decode(f.data) }); });
    return { kind: "zip", displayName, baseName, zfiles, files, fileCount: zfiles.length,
             comcfgRefs: zfiles.map((f, i) => Core.basename(f.name).toLowerCase() === "comcfg.txt" ? i : -1).filter((i) => i >= 0) };
  }
  function makeTxtItem(name, u8) {
    return { kind: "txt", displayName: name, baseName: name, files: [{ ref: 0, name, text: Core.latin1Decode(u8) }], fileCount: 1, comcfgRefs: [] };
  }

  function scanItem(it) {
    it.findingCount = 0; it.rowCount = 0;
    for (const f of it.files) {
      f.scan = Core.scanText(f.text, { includeOld: opts.includeOld, pinRow: isComcfg(f.name) });
      for (const x of f.scan.findings) initRow(x);
      it.findingCount += f.scan.findings.filter((x) => !x.synthetic).length;
      it.rowCount += f.scan.findings.length;
    }
  }

  async function ingest(file) {
    let u8 = new Uint8Array(await file.arrayBuffer());
    const name = file.name;
    try {
      if (Core.isZip(u8)) {
        const zf = await Core.parseZip(u8);
        const tars = zf.filter((f) => Core.isTar(f.data));
        const gz = zf.filter((f) => Core.isGzip(f.data) && /\.(tgz|gz)$/i.test(f.name));
        if (tars.length || gz.length) {
          for (const t of tars) addItem(makeTarItem(name + " › " + t.name, Core.basename(t.name), t.data));
          for (const g of gz) addItem(makeTarItem(name + " › " + g.name, Core.basename(g.name), await Core.gunzip(g.data)));
        } else addItem(makeZipItem(name, name, zf));
      } else if (Core.isGzip(u8)) {
        u8 = await Core.gunzip(u8);
        if (!Core.isTar(u8)) throw new Error("This .gz doesn't contain a tar archive");
        addItem(makeTarItem(name, name, u8));
      } else if (Core.isTar(u8)) {
        addItem(makeTarItem(name, name, u8));
      } else if (Core.isScannable(name.toLowerCase().endsWith(".txt") ? name : name + ".txt", u8)) {
        addItem(makeTxtItem(name, u8));
      } else throw new Error("Unknown format (expected .tar, .zip, .tar.gz or a text file)");
    } catch (err) {
      addItem({ kind: "error", displayName: name, error: err.message || String(err) });
    }
  }

  function addItem(it) {
    it.id = ++seq;
    syncOpts();
    if (it.kind !== "error") { scanItem(it); it.outName = defaultOutName(it); it.outCustom = false; }
    items.push(it);
    render();
  }

  /* ---------- output ---------- */
  function itemErrors(it) {
    const errs = [];
    for (const f of it.files || []) {
      if (isIgnored(it, f)) continue;
      for (const x of f.scan.findings) if (rowError(x)) errs.push(x);
    }
    return errs;
  }
  function changedFiles(it) {
    return (it.files || []).filter((f) => !isIgnored(it, f))
      .map((f) => ({ f, r: Core.applyText(f.scan) })).filter((o) => o.r.changes.length);
  }
  function buildOutput(it) {
    const changed = changedFiles(it);
    if (it.kind === "txt") return Core.latin1Encode(changed.length ? changed[0].r.text : it.files[0].text);
    const repl = new Map(changed.map((o) => [o.f.ref, Core.latin1Encode(o.r.text)]));
    const removed = new Set(opts.dropComcfg ? it.comcfgRefs : []);
    if (it.kind === "tar") return Core.buildTar(it.tar, repl, removed);
    return Core.buildZip(it.zfiles.filter((_, i) => !removed.has(i)).map((zf) => {
      const i = it.zfiles.indexOf(zf);
      return { name: zf.name, data: repl.has(i) ? repl.get(i) : zf.data };
    }));
  }
  function download(name, u8) {
    const url = URL.createObjectURL(new Blob([u8], { type: "application/octet-stream" }));
    const a = el("a", { href: url, download: name });
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  }

  /* ---------- rendering ---------- */
  const shortTok = (t) => t.length > 22 ? t.slice(0, 18) + "…" : t;

  function renderRow(it, file, x) {
    const opt = (v, t) => el("option", { value: v }, t);
    const sel = el("select", { "aria-label": "Action" },
      x.synthetic === "missing"
        ? [opt("keep", "Don't add"), opt("replace", "Add a PIN line")]
        : [x.synthetic ? opt("keep", "Keep as is") : null,
           opt("replace", x.kind === "csv" ? "Replace the password" : "Replace with"),
           opt("clear", "Clear"),
           x.canDelete ? opt("delete", x.kind === "csv" ? "Remove the user" : "Remove line") : null]);
    sel.value = x.action;
    const pin = isPinRow(x);
    const ignored = isIgnored(it, file);
    const inp = el("input", { type: "text", value: x.value, spellcheck: "false", autocomplete: "off", "aria-label": "New value",
                              inputmode: pin ? "numeric" : null, maxlength: pin ? "8" : null, placeholder: pin ? "PIN" : null });
    const note = (x.note || pin || ignored) ? el("div", { class: "note" }) : null;
    const syncInp = () => {
      sel.value = x.action;
      inp.value = x.value;
      sel.disabled = ignored;
      inp.disabled = ignored || x.action !== "replace";
      const e = ignored ? null : rowError(x);
      inp.classList.toggle("invalid", !!e);
      inp.title = e || "";
      if (note) {
        note.textContent = ignored ? "comcfg.txt is removed from the backup: this line won't be written."
                                   : (pin ? pinNote(x) : x.note);
        note.classList.toggle("pin", !ignored && pin && x.action === "replace");
      }
    };
    sel.addEventListener("change", () => { x.action = sel.value; x.customAction = true; syncInp(); refreshCard(it); });
    inp.addEventListener("input", () => { x.value = inp.value; x.custom = true; syncInp(); refreshCard(it); });
    x._sync = syncInp;
    syncInp();
    const current = x.synthetic === "missing" ? "(no line)" : (x.synthetic && x.token === "" ? "(empty)" : shortTok(x.token));
    return el("tr", { class: ignored ? "ignored" : null },
      el("td", {}, el("code", {}, Core.basename(file.name)),
        el("div", { class: "sub" }, x.synthetic === "missing" ? "to add" : "line " + (x.line + 1))),
      el("td", {}, el("strong", {}, x.label), x.sub ? el("div", { class: "sub" }, x.sub) : null, note),
      el("td", {}, el("code", { title: x.token }, current)),
      el("td", {}, sel),
      el("td", { class: "val" }, inp));
  }

  function renderCard(it) {
    const closeBtn = el("button", { type: "button", class: "ew-x", title: "Remove from the list", "aria-label": "Remove from the list", onclick: () => removeItem(it) }, "✕");
    if (it.kind === "error") {
      return el("div", { class: "ew-card" },
        el("div", { class: "ew-head" }, el("span", { class: "led red", "aria-hidden": "true" }), el("span", { class: "name" }, it.displayName), el("span", { class: "spacer" }), closeBtn),
        el("div", { class: "ew-msg err" }, it.error));
    }
    const kindLbl = it.kind === "tar" ? "TAR · " + it.fileCount + " files" : it.kind === "zip" ? "ZIP · " + it.fileCount + " files" : "Text";
    const count = it.findingCount;
    const head = el("div", { class: "ew-head" },
      el("span", { class: "led " + (count ? "amber" : "on"), "aria-hidden": "true" }),
      el("span", { class: "name" }, it.displayName),
      el("span", { class: "chip" }, kindLbl),
      el("span", { class: "chip " + (count ? "found" : "none") }, count ? count + " encrypted value" + (count > 1 ? "s" : "") : "No #_6 value"),
      it.comcfgRefs.length && opts.dropComcfg ? el("span", { class: "chip" }, "comcfg.txt removed") : null,
      el("span", { class: "spacer" }),
      closeBtn);

    const card = el("div", { class: "ew-card" }, head);
    if (it.rowCount) {
      const tbody = el("tbody");
      for (const f of it.files) for (const x of f.scan.findings) tbody.append(renderRow(it, f, x));
      card.append(el("div", { class: "table-scroll" }, el("table", {},
        el("thead", {}, el("tr", {}, el("th", { scope: "col" }, "File"), el("th", { scope: "col" }, "Parameter"), el("th", { scope: "col" }, "Current value"), el("th", { scope: "col" }, "Action"), el("th", { scope: "col" }, "New value"))),
        tbody)));
      it._diff = el("div", { class: "diff" });
      card.append(el("details", {}, el("summary", {}, "Preview the changed lines"), it._diff));
    } else {
      const scanned = it.files.map((f) => Core.basename(f.name)).join(", ") || "no text file";
      card.append(el("div", { class: "ew-msg" }, "Files checked: " + scanned + ". Nothing to replace" + (opts.includeOld ? "." : ": this backup can already be restored on another eWon as it is.")));
    }
    const outInp = el("input", { type: "text", value: it.outName, spellcheck: "false", "aria-label": "Output file name" });
    outInp.addEventListener("input", () => { it.outName = outInp.value; it.outCustom = true; refreshCard(it); });
    it._outInp = outInp;
    it._err = el("span", { class: "err" });
    it._btn = el("button", { type: "button", class: "btn", onclick: () => { try { download(it.outName, buildOutput(it)); } catch (e) { it._err.textContent = e.message; } } }, "Download");
    card.append(el("div", { class: "ew-foot" }, outInp, it._btn, it._err));
    it._card = card;
    refreshCard(it);
    return card;
  }

  function refreshCard(it) {
    if (it.kind === "error" || !it._btn) return;
    const errs = itemErrors(it);
    const nameOk = it.outName.trim() !== "";
    it._btn.disabled = errs.length > 0 || !nameOk;
    it._err.textContent = errs.length ? errs.length + " invalid value" + (errs.length > 1 ? "s" : "") + ": " + rowError(errs[0]) : (nameOk ? "" : "Empty file name");
    if (it._diff) {
      it._diff.replaceChildren();
      const ch = changedFiles(it);
      if (!ch.length) it._diff.append(el("pre", {}, "No change."));
      for (const { f, r } of ch) {
        it._diff.append(el("div", { class: "f" }, f.name));
        for (const c of r.changes) {
          if (c.before !== null) it._diff.append(el("pre", { class: "d" }, el("span", { class: "ln" }, "-" + c.line), c.before));
          if (c.after !== null) it._diff.append(el("pre", { class: "a" }, el("span", { class: "ln" }, "+" + c.line), c.after));
        }
      }
    }
  }

  function render() {
    $("#ew-list").replaceChildren(...items.map(renderCard));
    const ok = items.filter((i) => i.kind !== "error").length;
    $("#ew-toolbar").hidden = items.length < 1;
    $("#ew-all").hidden = ok < 2;
  }
  function removeItem(it) { items.splice(items.indexOf(it), 1); render(); }

  /* ---------- settings ---------- */
  $("#ew-pwd").addEventListener("input", () => {
    syncOpts();
    for (const it of items) for (const f of it.files || []) for (const x of f.scan.findings)
      if (!x.custom && !isPinRow(x)) { x.value = opts.pwd; if (x._sync) x._sync(); }
    items.forEach(refreshCard);
  });
  $("#ew-pin").addEventListener("input", () => {
    syncOpts();
    for (const it of items) for (const f of it.files || []) for (const x of f.scan.findings) {
      if (!isPinRow(x)) continue;
      if (!x.custom) x.value = opts.pin;
      if (!x.customAction && !(x.custom && x.value)) x.action = opts.pin ? "replace" : x.defaultAction;
      if (x._sync) x._sync();
    }
    items.forEach(refreshCard);
  });
  $("#ew-suffix").addEventListener("input", () => {
    syncOpts();
    for (const it of items) if (it.kind !== "error" && !it.outCustom) { it.outName = defaultOutName(it); if (it._outInp) it._outInp.value = it.outName; refreshCard(it); }
  });
  $("#ew-dropcom").addEventListener("change", () => { syncOpts(); render(); });
  $("#ew-old").addEventListener("change", () => { syncOpts(); items.forEach((it) => it.kind !== "error" && scanItem(it)); render(); });
  window.addEventListener("pageshow", syncOpts);
  window.addEventListener("load", syncOpts);

  $("#ew-clearlist").addEventListener("click", () => { items.length = 0; render(); });
  $("#ew-all").addEventListener("click", () => {
    const ok = items.filter((i) => i.kind !== "error");
    const bad = ok.filter((i) => itemErrors(i).length);
    if (bad.length) { bad.forEach(refreshCard); bad[0]._card.scrollIntoView({ behavior: "smooth" }); return; }
    const used = new Set();
    const files = ok.map((it) => {
      let n = it.outName, k = 1;
      while (used.has(n.toLowerCase())) { const [s, e] = splitExt(it.outName); n = s + "_" + (++k) + e; }
      used.add(n.toLowerCase());
      return { name: n, data: buildOutput(it) };
    });
    download("ewon_backups" + opts.suffix + ".zip", Core.buildZip(files));
  });

  /* ---------- drag and drop ---------- */
  const drop = $("#ew-drop");
  const handle = async (list) => { for (const f of list) await ingest(f); };
  $("#ew-files").addEventListener("change", (e) => { handle([...e.target.files]); e.target.value = ""; });
  ["dragenter", "dragover"].forEach((t) => window.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((t) => window.addEventListener(t, (e) => { e.preventDefault(); if (t === "drop" || e.target === document.documentElement) drop.classList.remove("over"); }));
  window.addEventListener("drop", (e) => { drop.classList.remove("over"); if (e.dataTransfer && e.dataTransfer.files.length) handle([...e.dataTransfer.files]); });

  syncOpts();
  render();
})();
