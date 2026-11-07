/* greenserver.be — SMTP Tester
   1. DNS check of a sender domain (MX, SPF, DMARC, DKIM) over DNS over HTTPS.
   2. Builds the test commands (port, test message with curl, certificate with OpenSSL).
   Everything runs in the browser; nothing is sent to greenserver.be. */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);

  function el(tag, text, cls) {
    const n = document.createElement(tag);
    if (text != null) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  }

  /* ================= 1. DNS ================= */

  const RESOLVERS = [
    (name, type) => fetch("https://cloudflare-dns.com/dns-query?name=" + encodeURIComponent(name) + "&type=" + type,
      { headers: { accept: "application/dns-json" } }),
    (name, type) => fetch("https://dns.google/resolve?name=" + encodeURIComponent(name) + "&type=" + type)
  ];

  async function dns(name, type) {
    let lastErr = null;
    for (const ask of RESOLVERS) {
      try {
        const res = await ask(name, type);
        if (!res.ok) throw new Error("HTTP " + res.status);
        return await res.json();
      } catch (e) { lastErr = e; }
    }
    throw lastErr || new Error("DNS");
  }

  const T = { CNAME: 5, MX: 15, TXT: 16 };
  const answers = (j, type) => (j && j.Answer ? j.Answer : []).filter(a => a.type === type);

  // A TXT record arrives quoted, sometimes split into several strings: join them back.
  function txtData(d) {
    const parts = String(d).match(/"((?:[^"\\]|\\.)*)"/g);
    if (!parts) return String(d);
    return parts.map(p => p.slice(1, -1).replace(/\\(\d{3}|.)/g, (m, g) => g.length === 3 ? String.fromCharCode(+g) : g)).join("");
  }

  function cleanDomain(v) {
    v = String(v || "").trim().toLowerCase();
    if (v.includes("@")) v = v.split("@").pop();
    v = v.replace(/^[a-z][a-z0-9+.-]*:\/\//, "").split(/[\/?#:\s]/)[0].replace(/\.$/, "");
    const ok = /^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,62}$/.test(v);
    return ok ? v : null;
  }

  const LEVEL_LABEL = { on: "OK", amber: "Worth checking", red: "Problem", off: "Information" };

  function item(level, what, nodes) {
    const li = el("li");
    const led = el("span", null, "led " + level);
    led.setAttribute("role", "img");
    led.setAttribute("aria-label", LEVEL_LABEL[level]);
    const detail = el("div", null, "detail");
    nodes.forEach(n => detail.append(n));
    li.append(led, el("span", what, "what"), detail);
    return li;
  }
  const P = t => el("p", t);
  const PRE = t => el("pre", t);

  function checkMx(j) {
    const recs = answers(j, T.MX).map(a => a.data.replace(/\.$/, ""))
      .sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
    if (recs.length) {
      return item("on", "Receiving (MX)", [P("The domain can receive mail: replies and bounces have somewhere to go."), PRE(recs.join("\n"))]);
    }
    return item("amber", "Receiving (MX)", [P("No receiving server. A send-only domain can do without one, but replies and bounces will go nowhere.")]);
  }

  function analyseSpf(s) {
    const allM = s.match(/(?:^|\s)([+~?-]?)all(?=\s|$)/i);
    const lookups = (s.match(/(?:^|\s)[+~?-]?(?:include:|a(?=[\s:/]|$)|mx(?=[\s:/]|$)|ptr(?=[\s:]|$)|exists:|redirect=)/gi) || []).length;
    const notes = [];
    let level = "on";
    if (allM && (allM[1] === "+" || allM[1] === "")) {
      level = "red";
      notes.push("+all or a bare all lets any server send for this domain. Replace it with ~all or -all.");
    } else if (allM && allM[1] === "?") {
      level = "amber";
      notes.push("?all is neutral: SPF says nothing about unlisted servers.");
    } else if (allM && allM[1] === "~") {
      notes.push("~all: unlisted servers are treated as suspicious.");
    } else if (allM && allM[1] === "-") {
      notes.push("-all: unlisted servers are rejected.");
    } else if (!/redirect=/i.test(s)) {
      level = "amber";
      notes.push("No all at the end: SPF says nothing about other servers.");
    }
    if (lookups > 10) {
      level = "red";
      notes.push(lookups + " DNS lookups at the first level alone: the standard allows 10 in total, so SPF will fail.");
    } else {
      notes.push(lookups + " DNS lookup" + (lookups === 1 ? "" : "s") + " at the first level (10 at most, nested includes counted).");
    }
    return { level, notes };
  }

  function checkSpf(j) {
    const spfs = answers(j, T.TXT).map(a => txtData(a.data)).filter(t => /^v=spf1(\s|$)/i.test(t));
    if (!spfs.length) {
      return item("amber", "SPF", [P("No SPF record on the domain. It isn't always a blocker (some relays check SPF on their own return-path subdomain), but many filters look at it.")]);
    }
    if (spfs.length > 1) {
      return item("red", "SPF", [P("Several SPF records: the standard allows only one, so filters treat SPF as invalid. Merge them into a single record."), PRE(spfs.join("\n"))]);
    }
    const r = analyseSpf(spfs[0]);
    return item(r.level, "SPF", [PRE(spfs[0]), ...r.notes.map(P)]);
  }

  function checkDmarc(j) {
    const recs = answers(j, T.TXT).map(a => txtData(a.data)).filter(t => /^v=DMARC1/i.test(t));
    if (!recs.length) {
      return item("amber", "DMARC", [P("No DMARC. It's recommended for everyone, and Gmail and Yahoo require it from bulk senders.")]);
    }
    if (recs.length > 1) {
      return item("red", "DMARC", [P("Several DMARC records: none will be applied. Keep only one."), PRE(recs.join("\n"))]);
    }
    const p = (recs[0].match(/(?:^|;)\s*p\s*=\s*([a-z]+)/i) || [])[1];
    const pol = {
      none: "p=none: monitoring only, nothing is blocked.",
      quarantine: "p=quarantine: failing mail goes to spam.",
      reject: "p=reject: failing mail is rejected."
    }[(p || "").toLowerCase()];
    return item(pol ? "on" : "amber", "DMARC", [PRE(recs[0]), P(pol || "The p= policy is missing or unreadable.")]);
  }

  function checkDkim(sel, j) {
    const what = "DKIM (" + sel + ")";
    const cn = answers(j, T.CNAME).map(a => a.data.replace(/\.$/, ""));
    const txt = answers(j, T.TXT).map(a => txtData(a.data));
    const key = txt.find(t => /(?:^|;)\s*p\s*=/i.test(t));
    const via = cn.length ? P("Through a CNAME pointing to " + cn[cn.length - 1] + ".") : null;
    if (key) {
      if (/(?:^|;)\s*p\s*=\s*(?:;|$)/i.test(key)) {
        return item("red", what, [P("The key is empty (p=): it has been revoked."), PRE(key)]);
      }
      const short = key.replace(/(p\s*=\s*)([A-Za-z0-9+/=]{48})[A-Za-z0-9+/=]+/, "$1$2…");
      return item("on", what, [P("Public key found."), ...(via ? [via] : []), PRE(short)]);
    }
    if (cn.length) {
      return item("amber", what, [P("The CNAME exists (pointing to " + cn[cn.length - 1] + ") but returns no key. Check the target with your email provider.")]);
    }
    return item("red", what, [P("Nothing found for this selector. Check its name in the DKIM-Signature header (s=…) or in your email provider's dashboard.")]);
  }

  function fallbackHelp(d) {
    return item("off", "Command line", [
      P("The same checks with nslookup (Windows, Linux, macOS):"),
      PRE("nslookup -type=MX " + d + "\nnslookup -type=TXT " + d + "\nnslookup -type=TXT _dmarc." + d)
    ]);
  }

  async function runDns(e) {
    e.preventDefault();
    const out = $("#dns-results");
    const status = $("#dns-status");
    const d = cleanDomain($("#dom").value);
    out.replaceChildren();
    if (!d) {
      status.textContent = "Enter a domain name, such as greenserver.be, or an address like alerts@greenserver.be.";
      $("#dom").focus();
      return;
    }
    const sels = $("#sel").value.split(/[\s,;]+/).map(s => s.trim().toLowerCase()).filter(s => /^[a-z0-9._-]+$/.test(s));
    status.textContent = "Querying DNS for " + d + "…";
    const btn = $("#dns-form button[type=submit]");
    btn.disabled = true;
    try {
      const [mx, txt, dmarc, ...dkim] = await Promise.all([
        dns(d, "MX"), dns(d, "TXT"), dns("_dmarc." + d, "TXT"),
        ...sels.map(s => dns(s + "._domainkey." + d, "TXT"))
      ]);
      if (mx.Status === 3 && txt.Status === 3) {
        out.append(item("red", "Domain", [P("This domain doesn't exist in DNS. Check the spelling.")]));
        status.textContent = "";
        return;
      }
      out.append(checkMx(mx), checkSpf(txt), checkDmarc(dmarc));
      if (sels.length) sels.forEach((s, i) => out.append(checkDkim(s, dkim[i])));
      else out.append(item("off", "DKIM", [P("Enter a selector to check the DKIM key. It appears in the DKIM-Signature header of a sent message (s=…) or in your email provider's dashboard.")]));
      const t = new Date();
      status.textContent = "Results for " + d + ", checked at " + t.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }) + ".";
    } catch (err) {
      status.textContent = "DNS couldn't be queried from this browser (network, blocker or firewall).";
      out.append(fallbackHelp(d));
    } finally {
      btn.disabled = false;
    }
  }

  /* ================= 2. Test commands ================= */

  const DEFAULT_PORT = { starttls: "587", tls: "465", none: "25" };
  let lastEnc = "starttls";

  // Strip characters that would break the quoting in the commands.
  const val = id => { const n = $("#" + id); return (n.value || "").trim().replace(/["'`$\\\s]/g, "") || n.placeholder; };
  const isIp = h => /^\d{1,3}(?:\.\d{1,3}){3}$/.test(h) || h.includes(":");

  function cmdBlock(title, desc, code, warn) {
    const wrap = el("div", null, "cmd");
    wrap.append(el("h3", title));
    if (desc) wrap.append(el("p", desc));
    if (warn) { const w = el("p", warn, "note-box"); wrap.append(w); }
    const box = el("div", null, "cmd-box");
    const pre = el("pre");
    pre.append(el("code", code));
    const b = el("button", "Copy", "copy");
    b.type = "button";
    b.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(code); }
      catch (_) {
        const r = document.createRange(); r.selectNodeContents(pre);
        const s = getSelection(); s.removeAllRanges(); s.addRange(r); document.execCommand("copy");
      }
      b.textContent = "Copied";
      setTimeout(() => { b.textContent = "Copy"; }, 1500);
    });
    box.append(pre, b);
    wrap.append(box);
    return wrap;
  }

  function buildCommands() {
    const f = $("#cmd-form");
    const os = f.querySelector('input[name="os"]:checked').value;      // win | unix
    const enc = f.querySelector('input[name="enc"]:checked').value;    // starttls | tls | none
    const portIn = $("#port");
    if (enc !== lastEnc) {
      if (!portIn.value || portIn.value === DEFAULT_PORT[lastEnc]) portIn.value = DEFAULT_PORT[enc];
      lastEnc = enc;
    }
    const auth = $("#auth").checked;
    $("#user").disabled = !auth;
    $("#insecure").disabled = enc === "none";
    $("#norevoke").disabled = enc === "none" || os !== "win";

    const host = val("host");
    const port = String(parseInt(portIn.value, 10) || DEFAULT_PORT[enc]);
    const ipRaw = ($("#ip").value || "").trim().replace(/[^0-9a-fA-F.:]/g, "");
    const useResolve = !!ipRaw && !isIp(host);
    const target = useResolve ? ipRaw : host;
    const from = val("from");
    const to = val("to");
    const user = ($("#user").value || "").trim().replace(/["'`$\\\s]/g, "") || from;
    const insecure = $("#insecure").checked && enc !== "none";
    const noRevoke = $("#norevoke").checked && enc !== "none" && os === "win";
    const win = os === "win";
    const out = $("#out");
    out.replaceChildren();

    // 1. Port
    out.append(win
      ? cmdBlock("Is the port open?", "In PowerShell. Look for “TcpTestSucceeded : True”.", "Test-NetConnection " + target + " -Port " + port)
      : cmdBlock("Is the port open?", "“succeeded” or “open” means the port answers.", "nc -vz " + target + " " + port));

    // 2. Test message
    const mail = win
      ? '@"\nFrom: <' + from + '>\nTo: <' + to + '>\nSubject: SMTP test\nDate: $((Get-Date).ToUniversalTime().ToString(\'r\'))\n\nThis is a test message.\n"@ | Set-Content -Encoding ascii mail.txt'
      : "cat > mail.txt <<EOF\nFrom: <" + from + ">\nTo: <" + to + ">\nSubject: SMTP test\nDate: $(LC_ALL=C date '+%a, %d %b %Y %H:%M:%S %z')\n\nThis is a test message.\nEOF";
    out.append(cmdBlock("The test message", "Creates mail.txt in the current folder.", mail));

    // 3. Sending with curl
    const scheme = enc === "tls" ? "smtps" : "smtp";
    const L = [(win ? "curl.exe" : "curl") + ' -v --url "' + scheme + "://" + host + ":" + port + '"'];
    if (enc === "starttls") L.push("--ssl-reqd");
    if (useResolve) L.push('--resolve "' + host + ":" + port + ":" + ipRaw + '"');
    if (noRevoke) L.push("--ssl-no-revoke");
    if (insecure) L.push("-k");
    if (auth) L.push("--user '" + user + ":PASSWORD'");
    L.push('--mail-from "' + from + '"', '--mail-rcpt "' + to + '"');
    if (!win) L.push("--crlf");
    L.push("--upload-file mail.txt");
    const cont = win ? " `" : " \\";
    const curl = L.map((l, i) => (i ? "  " : "") + l + (i < L.length - 1 ? cont : "")).join("\n");
    let warn = null;
    if (auth && enc === "none") warn = "Without encryption, the username and password travel in clear text: AUTH PLAIN is just base64, readable by anyone who captures the traffic.";
    else if (insecure) warn = "-k turns off certificate checking. Fine for troubleshooting, never in production.";
    out.append(cmdBlock("Sending", (auth ? "Replace PASSWORD directly in the terminal, never on this page. " : "") + "-v shows the whole conversation with the server." + (useResolve ? " --resolve sends the connection to " + ipRaw + " while still checking the certificate against " + host + "." : ""), curl, warn));

    // 4. Certificate
    if (enc !== "none") {
      const st = enc === "starttls" ? "-starttls smtp " : "";
      let code, desc, w2 = null;
      if (isIp(host)) {
        code = "openssl s_client " + st + "-connect " + host + ":" + port + " -brief </dev/null";
        w2 = "The server is given as an IP address, so its certificate can't match. Enter its name instead (for example smtp.office365.com) and put the IP in “Connect via IP”.";
      } else {
        code = "openssl s_client " + st + "-connect " + target + ":" + port + " -servername " + host + " -verify_hostname " + host + " -verify_return_error -brief </dev/null";
      }
      desc = (win ? "OpenSSL doesn't come with Windows: run this command in Git Bash (installed with Git for Windows). " : "") + "Look for “Verification: OK”: the certificate is valid and matches the name.";
      out.append(cmdBlock("The certificate", desc, code, w2));
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const dnsForm = $("#dns-form");
    if (dnsForm) dnsForm.addEventListener("submit", runDns);
    const f = $("#cmd-form");
    if (f) {
      f.addEventListener("input", buildCommands);
      f.addEventListener("change", buildCommands);
      f.addEventListener("submit", e => e.preventDefault());
      buildCommands();
    }
  });

  // Exposed for automated tests.
  window.__smtpTester = { txtData, cleanDomain, analyseSpf };
})();
