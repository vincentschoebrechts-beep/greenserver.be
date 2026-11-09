#!/usr/bin/env python3
"""
Construit la formation « SAP from the shop floor / SAP vu de l'atelier » dans docs/sap/.

    python outils/sap_course/build.py

Génère : docs/sap/ (anglais), docs/sap/fr/ (français), docs/assets/sap-questions.js.
Le contenu se modifie dans content_en.py, content_fr.py et questions.py, puis on relance ce script.
"""
import html
import json
import os
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import content_en as EN  # noqa: E402
import content_fr as FR  # noqa: E402
from questions import Q  # noqa: E402

DOCS = ICI.parent.parent / "docs"
SAP = DOCS / "sap"
SITE = "https://greenserver.be"

# Chemins des pages, relatifs à docs/
def p_home(lang): return "sap/" if lang == "en" else "sap/fr/"
def p_lesson(lang, n): return f"sap/lesson-{n}/" if lang == "en" else f"sap/fr/lecon-{n}/"
def p_quiz(lang): return "sap/quiz/" if lang == "en" else "sap/fr/qcm/"
def p_annex(lang): return "sap/annex/" if lang == "en" else "sap/fr/annexe/"

def rel(from_path, to_path):
    """Lien relatif entre deux dossiers de docs/ (chemins qui finissent par /)."""
    depth = from_path.count("/")
    return "../" * depth + to_path

E = html.escape


def diagram_levels(lang):
    rows = {
        "en": [("Level 4 · ERP (SAP S/4HANA)", "Orders, materials, stock, costs", "days, hours"),
               ("Level 3 · MES", "Execution, tracking, quality on the floor", "minutes"),
               ("Level 2 · SCADA and HMI", "Supervision of lines and machines", "seconds"),
               ("Level 1 · PLCs", "Control of the process", "milliseconds"),
               ("Level 0 · Sensors and actuators", "The physical process", "real time")],
        "fr": [("Niveau 4 · ERP (SAP S/4HANA)", "Ordres, articles, stocks, coûts", "jours, heures"),
               ("Niveau 3 · MES", "Exécution, suivi, qualité en atelier", "minutes"),
               ("Niveau 2 · SCADA et IHM", "Supervision des lignes et des machines", "secondes"),
               ("Niveau 1 · Automates", "Contrôle-commande du procédé", "millisecondes"),
               ("Niveau 0 · Capteurs et actionneurs", "Le procédé physique", "temps réel")],
    }[lang]
    title = {"en": "The five levels of a factory, from sensors to ERP, with their time scales",
             "fr": "Les cinq niveaux d'une usine, des capteurs à l'ERP, avec leurs échelles de temps"}[lang]
    cap = {"en": "The higher the level, the slower the rhythm: SAP plans in days and hours, a PLC reacts in milliseconds.",
           "fr": "Plus le niveau est haut, plus le rythme est lent : SAP planifie en jours et en heures, un automate réagit en millisecondes."}[lang]
    parts = []
    for i, (t, sub, time) in enumerate(rows):
        y = 1 + i * 66
        cls = "hot" if i == 0 else "box"
        parts.append(f'<rect class="{cls}" x="1" y="{y}" width="480" height="52" rx="4"/>'
                     f'<text class="t" x="16" y="{y + 24}">{E(t)}</text>'
                     f'<text class="lab" x="16" y="{y + 43}">{E(sub)}</text>'
                     f'<text class="lab" x="500" y="{y + 31}">{E(time)}</text>')
    return (f'<figure class="diagram"><svg viewBox="0 0 660 320" role="img" aria-label="{E(title)}">'
            + "".join(parts) + f'</svg><figcaption>{E(cap)}</figcaption></figure>')


def diagram_flow(lang):
    t = {
        "en": dict(title="Data flow between the PLC, the MES and SAP",
                   b1=("PLC and SCADA", "tags, counters, events"),
                   b2=("MES or gateway", "translates"),
                   b3=("SAP S/4HANA", "orders, confirmations"),
                   a1="OPC UA", a2="IDoc · RFC · OData",
                   cap="SAP sends orders down to the MES; the MES sends confirmations and goods movements up. SAP never talks to the PLC."),
        "fr": dict(title="Flux de données entre l'automate, le MES et SAP",
                   b1=("Automate et SCADA", "variables, compteurs"),
                   b2=("MES ou passerelle", "traduit"),
                   b3=("SAP S/4HANA", "ordres, confirmations"),
                   a1="OPC UA", a2="IDoc · RFC · OData",
                   cap="SAP descend les ordres vers le MES ; le MES remonte confirmations et mouvements de stock. SAP ne parle jamais à l'automate."),
    }[lang]
    def box(x, cls, head, sub):
        return (f'<rect class="{cls}" x="{x}" y="30" width="190" height="70" rx="4"/>'
                f'<text class="t" x="{x + 95}" y="60" text-anchor="middle">{E(head)}</text>'
                f'<text class="lab" x="{x + 95}" y="82" text-anchor="middle">{E(sub)}</text>')
    svg = (f'<figure class="diagram"><svg viewBox="0 0 700 130" role="img" aria-label="{E(t["title"])}">'
           '<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>'
           + box(1, "box", *t["b1"]) + box(255, "box", *t["b2"]) + box(509, "hot", *t["b3"])
           + '<g style="color:var(--muted)" stroke="currentColor" stroke-width="2" fill="none">'
           '<line x1="193" y1="65" x2="253" y2="65" marker-start="url(#fl)" marker-end="url(#fl)"/>'
           '<line x1="447" y1="65" x2="507" y2="65" marker-start="url(#fl)" marker-end="url(#fl)"/></g>'
           f'<text class="lab" x="223" y="122" text-anchor="middle">{E(t["a1"])}</text>'
           f'<text class="lab" x="477" y="122" text-anchor="middle">{E(t["a2"])}</text>'
           f'</svg><figcaption>{E(t["cap"])}</figcaption></figure>')
    return svg


def page(lang, path, other_path, title, description, body, scripts=False):
    L = EN.LANG if lang == "en" else FR.LANG
    tools = "Tools" if lang == "en" else "Outils"
    root = rel(path, "")
    # L'accueil existe en anglais (/) et en français (/fr/)
    home = root if lang == "en" else root + "fr/"
    tools_anchor = "#tools" if lang == "en" else "#outils"
    other_lang = "fr" if lang == "en" else "en"
    head_alt = (f'<link rel="alternate" hreflang="{lang}" href="{SITE}/{path}">\n'
                f'<link rel="alternate" hreflang="{other_lang}" href="{SITE}/{other_path}">')
    js = ""
    if scripts:
        js = (f'<script src="{root}assets/sap-questions.js"></script>\n'
              f'<script src="{root}assets/sap-course.js"></script>\n')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE}/{path}">
<link rel="canonical" href="{SITE}/{path}">
{head_alt}
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#f3f4f0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1f2427" media="(prefers-color-scheme: dark)">
<link rel="preload" href="{root}assets/fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/site.css">
<link rel="stylesheet" href="{root}assets/sap-course.css">
</head>
<body>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{home}"><span class="led on" aria-hidden="true"></span><span>greenserver<span class="tld">.be</span></span></a>
    <nav aria-label="{'Main navigation' if lang == 'en' else 'Navigation principale'}">
      <a href="{home}{tools_anchor}">{tools}</a>
      <a href="{rel(path, other_path)}" hreflang="{other_lang}" lang="{other_lang}" onclick="try{{localStorage.setItem('langue','{other_lang}')}}catch(e){{}}">{L['switch']}</a>
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <span>greenserver.be, 2026</span>
    <span>{'No cookies, no visitor tracking, fonts served from this site.' if lang == 'en' else 'Pas de cookies, pas de pistage, polices servies par ce site.'}</span>
  </div>
</footer>
{js}</body>
</html>
"""


def write(path, text):
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print("écrit", out.relative_to(DOCS.parent))


def build_lesson(lang, n, les, check_ids, annex=False):
    C = EN if lang == "en" else FR
    L = C.LANG
    other = "fr" if lang == "en" else "en"
    if annex:
        path, other_path = p_annex(lang), p_annex(other)
    else:
        path, other_path = p_lesson(lang, n), p_lesson(other, n)
    meta = C.HOME_ANNEX["label"] if annex else f"{L['lesson_word']} {n} {L['of']} 10"
    body = les["body"].replace("{DIAGRAM_LEVELS}", diagram_levels(lang)).replace("{DIAGRAM_FLOW}", diagram_flow(lang))
    goals = "".join(f"<li>{E(g)}</li>" for g in les["goals"])
    keys = "".join(f"<li>{E(k)}</li>" for k in les["keys"])
    prev_link = (f'<a class="btn ghost" href="{rel(path, p_lesson(lang, n - 1))}">← {L["prev"]}</a>' if (n or 0) > 1 else "<span></span>")
    if annex:
        prev_link = f'<a class="btn ghost" href="{rel(path, p_lesson(lang, 10))}">← {L["prev"]}</a>'
        nxt = f'<a class="btn" href="{rel(path, p_quiz(lang))}">{L["quiz"]} →</a>'
    elif n < 10:
        nxt = f'<a class="btn" href="{rel(path, p_lesson(lang, n + 1))}">{L["next"]} →</a>'
    else:
        nxt = f'<a class="btn" href="{rel(path, p_quiz(lang))}">{L["quiz"]} →</a>'
    html_body = f"""
<article class="article wrap course">
  <p class="meta"><a href="{rel(path, p_home(lang))}">{E(L['course_title'])}</a> · {meta}</p>
  <h1>{E(les['title'])}</h1>
  <p class="lead">{E(les['lead'])}</p>
  <div class="prose">
    <div class="goals"><p><strong>{L['goals']}</strong></p><ul>{goals}</ul></div>
    {body}
    <aside class="example"><h2>{L['example']}</h2><p>{E(les['example'])}</p></aside>
    <h2>{L['keys']}</h2>
    <ul class="keys">{keys}</ul>
    <h2 id="check">{L['check']}</h2>
    <p>{L['check_intro_annex'] if annex else L['check_intro']}</p>
    <div class="qcheck" data-ids="{','.join(map(str, check_ids))}" data-lang="{lang}"></div>
    <nav class="lesson-nav" aria-label="{L['contents']}">
      {prev_link}
      <a href="{rel(path, p_home(lang))}">{L['contents']}</a>
      {nxt}
    </nav>
  </div>
</article>"""
    title = f"{les['title']} · {L['course_title']}"
    write(path, page(lang, path, other_path, title, les["lead"], html_body, scripts=True))


def build_home(lang):
    C = EN if lang == "en" else FR
    L, H = C.LANG, C.HOME
    other = "fr" if lang == "en" else "en"
    path, other_path = p_home(lang), p_home(other)
    items = []
    for n, les in enumerate(C.LESSONS, 1):
        items.append(f'<li><a href="{rel(path, p_lesson(lang, n))}">{E(les["title"])}</a><span class="muted">{E(les["lead"])}</span></li>')
    how = "".join(f"<li>{E(h)}</li>" for h in H["how"])
    more = "".join(f'<li><a href="{u}">{E(t)}</a>{E(rest)}</li>' for u, t, rest in H["more"])
    tag = f'{L["course_tag"]} · 10 {"lessons" if lang == "en" else "leçons"} · {"final quiz" if lang == "en" else "QCM final"}'
    html_body = f"""
<section class="page-head wrap course">
  <span class="state"><span class="led on" aria-hidden="true"></span>{E(tag)}</span>
  <h1>{E(L['course_title'])}</h1>
  <p class="lead">{E(H['lead'])}</p>
  <div class="actions">
    <a class="btn" href="{rel(path, p_lesson(lang, 1))}">{E(H['start_btn'])}</a>
    <a class="btn ghost" href="{rel(path, p_quiz(lang))}">{E(H['quiz_btn'])}</a>
  </div>
</section>
<section class="wrap">
  <div class="prose">
    <p class="note-box">{E(H['disclaimer'])}</p>
    <h2>{E(H['who_h'])}</h2>
    <p>{E(H['who'])}</p>
    <h2>{E(H['how_h'])}</h2>
    <ul>{how}</ul>
    <h2>{E(H['lessons_h'])}</h2>
    <ol class="lesson-list">{''.join(items)}</ol>
    <h2>{E(C.HOME_ANNEX['h'])}</h2>
    <p>{E(C.HOME_ANNEX['p'])}</p>
    <p><a href="{rel(path, p_annex(lang))}">{E(C.ANNEX['title'])} →</a></p>
    <h2>{E(H['quiz_h'])}</h2>
    <p>{E(H['quiz_p'])}</p>
    <p><a class="btn" href="{rel(path, p_quiz(lang))}">{E(H['quiz_btn'])}</a></p>
    <h2>{E(H['more_h'])}</h2>
    <ul>{more}</ul>
    <p class="small muted">{E(H['updated'])}</p>
  </div>
</section>"""
    write(path, page(lang, path, other_path, H["title"], H["description"], html_body))


def build_quiz(lang):
    C = EN if lang == "en" else FR
    L, QZ = C.LANG, C.QUIZ
    other = "fr" if lang == "en" else "en"
    path, other_path = p_quiz(lang), p_quiz(other)
    labels = {k: QZ[k] for k in ("submit", "again", "answered", "score", "pass", "fail", "missing", "from_lesson")}
    labels.update(right=L["right"], wrong=L["wrong"], answer_is=L["answer_is"])
    html_body = f"""
<article class="article wrap course">
  <p class="meta"><a href="{rel(path, p_home(lang))}">{E(L['course_title'])}</a> · {E(QZ['h1'])}</p>
  <h1>{E(QZ['h1'])}</h1>
  <p class="lead">{E(QZ['lead'])}</p>
  <div class="prose">
    <div id="quiz" data-lang="{lang}" data-labels='{E(json.dumps(labels, ensure_ascii=False))}'></div>
    <noscript><p class="note-box">{'The quiz needs JavaScript.' if lang == 'en' else 'Le QCM a besoin de JavaScript.'}</p></noscript>
    <nav class="lesson-nav" aria-label="{L['contents']}">
      <a class="btn ghost" href="{rel(path, p_lesson(lang, 10))}">← {L['prev']}</a>
      <a href="{rel(path, p_home(lang))}">{L['contents']}</a>
      <span></span>
    </nav>
  </div>
</article>"""
    write(path, page(lang, path, other_path, QZ["title"], QZ["lead"], html_body, scripts=True))


def build_questions_js():
    data = []
    for i, (lesson, en, fr) in enumerate(Q):
        data.append({"id": i, "l": lesson,
                     "en": {"q": en[0], "o": en[1], "e": en[2]},
                     "fr": {"q": fr[0], "o": fr[1], "e": fr[2]}})
    js = ("/* Banque de questions de la formation SAP from the shop floor / SAP vu de l'atelier.\n"
          "   Générée par outils/sap_course/build.py : ne pas modifier à la main.\n"
          "   La première option est la bonne réponse ; la page mélange l'ordre. */\n"
          "window.SAP_Q = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (DOCS / "assets" / "sap-questions.js").write_text(js, encoding="utf-8")
    print("écrit docs/assets/sap-questions.js")


def main():
    assert len(EN.LESSONS) == 10 and len(FR.LESSONS) == 10
    build_questions_js()
    for lang in ("en", "fr"):
        build_home(lang)
        build_quiz(lang)
        for n in range(1, 11):
            les = (EN if lang == "en" else FR).LESSONS[n - 1]
            check = [(n - 1) * 10 + k for k in EN.LESSONS[n - 1]["check"]]
            build_lesson(lang, n, les, check)
        annex_ids = [i for i, q in enumerate(Q) if q[0] == 11]
        build_lesson(lang, None, (EN if lang == "en" else FR).ANNEX, annex_ids, annex=True)


if __name__ == "__main__":
    main()
