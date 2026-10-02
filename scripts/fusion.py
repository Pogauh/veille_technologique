#!/usr/bin/env python3
"""Fusionne data/nouveautes.json dans data/veille.json et régénère les sorties.

Usage :
    python3 scripts/fusion.py            # valide, fusionne, régénère docs/
    python3 scripts/fusion.py --urls     # affiche les URLs déjà connues (60 derniers jours)
    python3 scripts/fusion.py --check    # valide nouveautes.json sans rien écrire

Codes de sortie : 0 = OK, 2 = nouveautes.json invalide (rien n'est modifié).

Bibliothèque standard uniquement. Idempotent : relancer le script deux fois de
suite ne crée aucun doublon.
"""
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, time, timedelta, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
BASE_FILE = ROOT / "data" / "veille.json"
NEW_FILE = ROOT / "data" / "nouveautes.json"
DOCS = ROOT / "docs"

# URL publique GitHub Pages (surchargeable : FEED_BASE_URL=... python3 scripts/fusion.py)
SITE_URL = os.environ.get("FEED_BASE_URL", "https://pogauh.github.io/veille_technologique").rstrip("/")
FEED_TITLE = "Veille Java / Architecture hexagonale / C4"
FEED_DESC = "Veille technologique quotidienne : développement Java, architecture hexagonale, diagrammes C4."
FEED_MAX_ITEMS = 100
MD_DAYS = 60
DEDUP_DAYS = 60

THEMES = {"java": "Java", "hexagonal": "Hexagonal", "c4": "C4", "securite": "Sécurité"}
CONFIANCE = {"elevee": "élevée", "moyenne": "moyenne", "faible": "faible"}
ACTIONS = {"migrer", "tester", "lire", "surveiller", "corriger"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TRACKING = ("utm_", "fbclid", "gclid", "mc_", "ref", "ref_src")


# ---------- utilitaires ----------
def normalize_url(url: str) -> str:
    s = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(s.query) if not k.lower().startswith(TRACKING)]
    path = s.path.rstrip("/") or "/"
    return urlunsplit((s.scheme.lower(), s.netloc.lower(), path, urlencode(query), ""))


def url_id(url: str) -> str:
    return hashlib.sha1(normalize_url(url).encode("utf-8")).hexdigest()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    os.replace(tmp, path)


def load_json(path: Path, default):
    if not path.exists() or path.stat().st_size == 0:
        return default
    return json.loads(path.read_text("utf-8"))


def valid_date(value) -> bool:
    if not isinstance(value, str) or not DATE_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def rfc822(day: str, hour: int, minute: int = 0) -> str:
    dt = datetime.combine(date.fromisoformat(day), time(hour, minute), tzinfo=timezone.utc)
    return format_datetime(dt)


# ---------- validation ----------
def validate(new) -> list:
    err = []
    if not isinstance(new, dict):
        return ["La racine doit être un objet JSON."]
    for k in ("date", "resume_du_jour", "items"):
        if k not in new:
            err.append(f"Champ obligatoire manquant : {k}")
    extra = set(new) - {"date", "resume_du_jour", "items"}
    if extra:
        err.append(f"Champs inconnus à la racine : {sorted(extra)}")
    if err:
        return err
    if not valid_date(new["date"]):
        err.append("date : format AAAA-MM-JJ valide attendu.")
    if not isinstance(new["resume_du_jour"], str) or len(new["resume_du_jour"]) > 1200:
        err.append("resume_du_jour : chaîne de 1200 caractères maximum.")
    if not isinstance(new["items"], list) or len(new["items"]) > 12:
        err.append("items : liste de 12 éléments maximum.")
        return err

    required = ("titre", "url", "source", "date_publication", "theme", "resume", "importance", "confiance")
    allowed = set(required) | {"action"}
    limits = {"titre": (5, 200), "source": (2, 80), "resume": (20, 700), "importance": (10, 300)}
    for n, it in enumerate(new["items"], 1):
        p = f"items[{n}]"
        if not isinstance(it, dict):
            err.append(f"{p} : objet attendu.")
            continue
        for k in required:
            if k not in it:
                err.append(f"{p} : champ manquant « {k} ».")
        if set(it) - allowed:
            err.append(f"{p} : champs inconnus {sorted(set(it) - allowed)}.")
        for k, (lo, hi) in limits.items():
            v = it.get(k)
            if k in it and (not isinstance(v, str) or not lo <= len(v.strip()) <= hi):
                err.append(f"{p}.{k} : texte de {lo} à {hi} caractères attendu.")
        if "url" in it and not (isinstance(it["url"], str) and re.match(r"^https?://\S+$", it["url"])):
            err.append(f"{p}.url : URL http(s) attendue.")
        if "date_publication" in it and not valid_date(it["date_publication"]):
            err.append(f"{p}.date_publication : format AAAA-MM-JJ valide attendu.")
        if "theme" in it and it["theme"] not in THEMES:
            err.append(f"{p}.theme : parmi {sorted(THEMES)}.")
        if "confiance" in it and it["confiance"] not in CONFIANCE:
            err.append(f"{p}.confiance : parmi {sorted(CONFIANCE)}.")
        if "action" in it and it["action"] not in ACTIONS:
            err.append(f"{p}.action : parmi {sorted(ACTIONS)}.")
    return err


# ---------- rendu ----------
def item_html(i: dict) -> str:
    parts = [
        f"<p>{escape(i['resume'])}</p>",
        f"<p><strong>Pourquoi c'est important :</strong> {escape(i['importance'])}</p>",
    ]
    meta = [f"Source : {escape(i['source'])}", f"Publié le {i['date_publication']}",
            f"Confiance : {CONFIANCE[i['confiance']]}"]
    if i.get("action"):
        meta.insert(0, f"Action suggérée : <strong>{escape(i['action'])}</strong>")
    parts.append(f"<p><em>{' · '.join(meta)}</em></p>")
    return "".join(parts)


def build_feed(items, syntheses) -> str:
    entries = []
    # Synthèses du jour (publiées légèrement après les articles pour apparaître en tête)
    for s in syntheses[:30]:
        if not s["resume"].strip():
            continue
        entries.append(
            "<item>"
            f"<title>Synthèse du {s['date']}</title>"
            f"<link>{SITE_URL}/#{s['date']}</link>"
            f"<guid isPermaLink=\"false\">synthese-{s['date']}</guid>"
            f"<pubDate>{rfc822(s['date'], 5, 30)}</pubDate>"
            "<category>Synthèse</category>"
            f"<description>{escape('<p>' + escape(s['resume']) + '</p>')}</description>"
            "</item>"
        )
    for i in items[:FEED_MAX_ITEMS]:
        entries.append(
            "<item>"
            f"<title>{escape('[' + THEMES[i['theme']] + '] ' + i['titre'])}</title>"
            f"<link>{escape(i['url'])}</link>"
            f"<guid isPermaLink=\"false\">{i['id']}</guid>"
            f"<pubDate>{rfc822(i['date_ajout'], 5, 0)}</pubDate>"
            f"<category>{escape(THEMES[i['theme']])}</category>"
            f"<category>{escape(i['source'])}</category>"
            f"<description>{escape(item_html(i))}</description>"
            "</item>"
        )
    latest = max([i["date_ajout"] for i in items] + [s["date"] for s in syntheses] + ["1970-01-01"])
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
        f"<title>{escape(FEED_TITLE)}</title>\n"
        f"<link>{SITE_URL}/</link>\n"
        f"<description>{escape(FEED_DESC)}</description>\n"
        "<language>fr</language>\n"
        f'<atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        f"<lastBuildDate>{rfc822(latest, 5, 30)}</lastBuildDate>\n"
        + "\n".join(entries)
        + "\n</channel>\n</rss>\n"
    )


def group_by_day(items, syntheses, days):
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    by_day = {}
    for i in items:
        if i["date_ajout"] >= cutoff:
            by_day.setdefault(i["date_ajout"], {"items": [], "resume": ""})["items"].append(i)
    for s in syntheses:
        if s["date"] >= cutoff:
            by_day.setdefault(s["date"], {"items": [], "resume": ""})["resume"] = s["resume"]
    return sorted(by_day.items(), reverse=True)


def build_markdown(items, syntheses) -> str:
    out = [f"# {FEED_TITLE}\n", f"> Flux RSS : {SITE_URL}/feed.xml\n"]
    for day, block in group_by_day(items, syntheses, MD_DAYS):
        out.append(f"\n## {day}\n")
        if block["resume"].strip():
            out.append(f"**Résumé du jour.** {block['resume']}\n")
        for theme in THEMES:
            group = [i for i in block["items"] if i["theme"] == theme]
            if not group:
                continue
            out.append(f"\n### {THEMES[theme]}\n")
            for i in group:
                action = f" · action : {i['action']}" if i.get("action") else ""
                out.append(
                    f"#### [{i['titre']}]({i['url']})\n"
                    f"*{i['source']} · publié le {i['date_publication']} · confiance : "
                    f"{CONFIANCE[i['confiance']]}{action}*\n\n"
                    f"{i['resume']}\n\n**Pourquoi c'est important :** {i['importance']}\n"
                )
    return "\n".join(out) + "\n"


JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
THEME_ICON = {"java": "☕", "hexagonal": "⬡", "c4": "◫", "securite": "🛡"}

INDEX_CSS = """
:root{color-scheme:light dark;--bg:#f6f8fa;--card:#fff;--soft:#eef1f5;--border:#d8dee4;--text:#1f2328;--muted:#656d76;
--accent:#0969da;--c-java:#d9730d;--c-hexagonal:#8250df;--c-c4:#0a8ea6;--c-securite:#d1242f;--ok:#1a7f37;--warn:#bf8700}
:root[data-theme=dark]{--bg:#0d1117;--card:#161b22;--soft:#21262d;--border:#30363d;--text:#e6edf3;--muted:#8b949e;
--accent:#58a6ff;--c-java:#f0883e;--c-hexagonal:#a371f7;--c-c4:#39c5cf;--c-securite:#ff7b72;--ok:#3fb950;--warn:#d29922}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0d1117;--card:#161b22;--soft:#21262d;--border:#30363d;
--text:#e6edf3;--muted:#8b949e;--accent:#58a6ff;--c-java:#f0883e;--c-hexagonal:#a371f7;--c-c4:#39c5cf;--c-securite:#ff7b72;
--ok:#3fb950;--warn:#d29922}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
-webkit-font-smoothing:antialiased}
main{max-width:800px;margin:0 auto;padding:2.5rem 1rem 4rem}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
header.top{display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;justify-content:space-between;margin-bottom:1.5rem}
h1{margin:0;font-size:clamp(1.7rem,4.5vw,2.4rem);line-height:1.15;letter-spacing:-.025em;
background:linear-gradient(90deg,var(--accent),var(--c-hexagonal) 60%,var(--c-securite));
-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin:.4rem 0 0;color:var(--muted);font-size:.9rem}
.actions{display:flex;gap:.5rem;align-items:center}
.btn{display:inline-flex;align-items:center;gap:.4rem;border:1px solid var(--border);background:var(--card);color:var(--text);
padding:.4rem .8rem;border-radius:8px;font:inherit;font-size:.85rem;text-decoration:none;cursor:pointer;
transition:border-color .15s,transform .15s}
.btn:hover{border-color:var(--accent);transform:translateY(-1px)}
.filters{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 2rem;position:sticky;top:0;z-index:5;padding:.7rem 0;
background:linear-gradient(var(--bg) 75%,transparent)}
.chip{border:1px solid var(--border);background:var(--card);color:var(--muted);padding:.25rem .8rem;border-radius:999px;
font:inherit;font-size:.82rem;cursor:pointer;transition:all .15s}
.chip:hover{color:var(--text);border-color:var(--muted)}
.chip[aria-pressed=true]{color:#fff;background:var(--c,var(--accent));border-color:var(--c,var(--accent))}
.chip .n{opacity:.7;margin-left:.3rem;font-size:.75rem}
.timeline{position:relative;margin-left:.5rem;padding-left:1.6rem;border-left:2px solid var(--border)}
section.day{position:relative;margin-bottom:2.6rem}
section.day::before{content:"";position:absolute;left:calc(-1.6rem - 7px);top:.55rem;width:12px;height:12px;border-radius:50%;
background:var(--accent);box-shadow:0 0 0 4px var(--bg),0 0 12px var(--accent)}
section.day>h2{margin:0;font-size:1.25rem;letter-spacing:-.01em}
section.day>h2::first-letter{text-transform:uppercase}
section.day>h2 small{display:block;font:500 .75rem ui-monospace,monospace;color:var(--muted);text-transform:none;letter-spacing:.03em}
.resume{margin:.9rem 0 1.1rem;padding:.8rem 1rem;background:var(--soft);border-radius:10px;color:var(--text);font-size:.95rem}
article.card{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--c);border-radius:12px;
padding:1.1rem 1.3rem;margin:1rem 0;transition:transform .15s,box-shadow .15s,border-color .15s}
article.card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.18)}
.t-java{--c:var(--c-java)}.t-hexagonal{--c:var(--c-hexagonal)}.t-c4{--c:var(--c-c4)}.t-securite{--c:var(--c-securite)}
.head{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;margin-bottom:.45rem}
.badge{display:inline-flex;align-items:center;gap:.3rem;font-size:.68rem;font-weight:700;text-transform:uppercase;
letter-spacing:.06em;padding:.15rem .6rem;border-radius:999px;color:var(--c);
background:color-mix(in srgb,var(--c) 16%,transparent);border:1px solid color-mix(in srgb,var(--c) 35%,transparent)}
.badge.cvss{--c:var(--warn);font-family:ui-monospace,monospace}
.badge.cvss.crit{--c:var(--c-securite)}
article h3{margin:0 0 .5rem;font-size:1.08rem;line-height:1.35;letter-spacing:-.01em}
article h3 a{color:var(--text);text-decoration:none;background:linear-gradient(var(--c),var(--c)) 0 100%/0 2px no-repeat;
transition:background-size .2s,color .15s}
article h3 a:hover{color:var(--c);background-size:100% 2px}
article p{margin:.5rem 0;color:color-mix(in srgb,var(--text) 88%,transparent);font-size:.95rem}
code{background:var(--soft);padding:.08rem .35rem;border-radius:5px;font-size:.84em}
.why{margin:.8rem 0;padding:.6rem .9rem;border-left:3px solid var(--c);border-radius:0 8px 8px 0;
background:color-mix(in srgb,var(--c) 8%,transparent);font-size:.92rem}
.why strong{color:var(--c)}
.meta{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.8rem;font-size:.76rem;color:var(--muted)}
.meta span{background:var(--soft);padding:.12rem .55rem;border-radius:6px}
.meta .act{background:var(--accent);color:#fff;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.dot{display:inline-block;width:.5rem;height:.5rem;border-radius:50%;margin-right:.35rem;background:var(--ok)}
.dot.moyenne{background:var(--warn)}.dot.faible{background:var(--c-securite)}
.hidden{display:none!important}
footer{margin-top:3rem;color:var(--muted);font-size:.8rem;text-align:center}
@media(max-width:560px){.timeline{padding-left:1.1rem;margin-left:.3rem}section.day::before{left:calc(-1.1rem - 7px)}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

INDEX_JS = """
(function(){
var root=document.documentElement,store;
try{store=window.localStorage}catch(e){}
try{var s=store&&store.getItem('theme');if(s)root.dataset.theme=s}catch(e){}
var tb=document.getElementById('theme');
if(tb)tb.addEventListener('click',function(){
 var dark=root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
 root.dataset.theme=dark?'light':'dark';
 try{store&&store.setItem('theme',root.dataset.theme)}catch(e){}});
var chips=[].slice.call(document.querySelectorAll('.chip')),cards=[].slice.call(document.querySelectorAll('article.card'));
function apply(f){
 chips.forEach(function(c){c.setAttribute('aria-pressed',String(c.dataset.f===f))});
 cards.forEach(function(a){a.classList.toggle('hidden',f!=='all'&&!a.classList.contains('t-'+f))});
 [].forEach.call(document.querySelectorAll('section.day'),function(d){
  d.classList.toggle('hidden',!d.querySelector('article.card:not(.hidden)')&&f!=='all')});
}
chips.forEach(function(c){c.addEventListener('click',function(){apply(c.dataset.f)})});
})();
"""


def fr_date(day: str) -> str:
    d = date.fromisoformat(day)
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]} {d.year}"


def decorate(text: str) -> str:
    """Échappe puis met en <code> les identifiants CVE/GHSA et numéros de version."""
    t = escape(text)
    t = re.sub(r"\b(CVE-\d{4}-\d{4,7}|GHSA(?:-[a-z0-9]{4}){3})\b", r"<code>\1</code>", t)
    t = re.sub(r"(?<![\w.-])(\d+\.\d+(?:\.\d+)+)(?![\w-])", r"<code>\1</code>", t)
    return t


def card_html(i: dict) -> str:
    theme = i["theme"]
    badges = [f'<span class="badge">{THEME_ICON[theme]} {escape(THEMES[theme])}</span>']
    m = re.search(r"CVSS\s*(\d+(?:\.\d+)?)", i["resume"])
    if m:
        score = float(m.group(1))
        crit = " crit" if score >= 9 else ""
        badges.append(f'<span class="badge cvss{crit}">CVSS {m.group(1)}</span>')
    meta = []
    if i.get("action"):
        meta.append(f'<span class="act">{escape(i["action"])}</span>')
    meta.append(f'<span>{escape(i["source"])}</span>')
    meta.append(f'<span class="mono">{i["date_publication"]}</span>')
    meta.append(f'<span><i class="dot {i["confiance"]}"></i>confiance {CONFIANCE[i["confiance"]]}</span>')
    return (
        f'<article class="card t-{theme}">'
        f'<div class="head">{"".join(badges)}</div>'
        f'<h3><a href="{escape(i["url"])}" target="_blank" rel="noopener">{escape(i["titre"])}</a></h3>'
        f'<p>{decorate(i["resume"])}</p>'
        f'<div class="why"><strong>Pourquoi c\'est important</strong> · {decorate(i["importance"])}</div>'
        f'<div class="meta">{"".join(meta)}</div></article>'
    )


def build_index(items, syntheses) -> str:
    days = group_by_day(items, syntheses, MD_DAYS)
    counts = {t: sum(1 for _, b in days for i in b["items"] if i["theme"] == t) for t in THEMES}
    total = sum(counts.values())
    chips = [f'<button class="chip" data-f="all" aria-pressed="true">Tout<span class="n">{total}</span></button>']
    for t, label in THEMES.items():
        if counts[t]:
            chips.append(
                f'<button class="chip t-{t}" style="--c:var(--c-{t})" data-f="{t}" aria-pressed="false">'
                f'{THEME_ICON[t]} {escape(label)}<span class="n">{counts[t]}</span></button>'
            )
    body = []
    for day, block in days:
        body.append(f'<section class="day" id="{day}"><h2>{fr_date(day)}<small>{day}</small></h2>')
        if block["resume"].strip():
            body.append(f'<p class="resume">{escape(block["resume"])}</p>')
        body.extend(card_html(i) for i in block["items"])
        body.append("</section>")
    latest = days[0][0] if days else ""
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(FEED_TITLE)}</title>"
        f'<meta name="description" content="{escape(FEED_DESC)}">'
        f'<link rel="alternate" type="application/rss+xml" href="{SITE_URL}/feed.xml">'
        f"<style>{INDEX_CSS}</style></head><body><main>"
        f'<header class="top"><div><h1>{escape(FEED_TITLE)}</h1>'
        f'<p class="sub">{total} articles · dernière mise à jour : {fr_date(latest) if latest else "—"}</p></div>'
        '<div class="actions"><a class="btn" href="feed.xml">◉ Flux RSS</a>'
        '<button class="btn" id="theme" type="button" aria-label="Changer de thème">◐ Thème</button></div></header>'
        f'<nav class="filters" aria-label="Filtrer par thème">{"".join(chips)}</nav>'
        f'<div class="timeline">{"".join(body)}</div>'
        '<footer>Généré automatiquement · veille quotidienne</footer>'
        f"</main><script>{INDEX_JS}</script></body></html>\n"
    )


# ---------- programme principal ----------
def main(argv) -> int:
    base = load_json(BASE_FILE, {"version": 1, "items": [], "syntheses": []})
    base.setdefault("items", [])
    base.setdefault("syntheses", [])

    if "--urls" in argv:
        cutoff = (date.today() - timedelta(days=DEDUP_DAYS)).isoformat()
        for i in base["items"]:
            if i["date_ajout"] >= cutoff:
                print(i["url"])
        return 0

    try:
        new = load_json(NEW_FILE, None)
    except json.JSONDecodeError as e:
        print(f"ERREUR : nouveautes.json n'est pas un JSON valide ({e}). Rien n'a été modifié.", file=sys.stderr)
        return 2
    if new is None:
        print("ERREUR : data/nouveautes.json est vide ou absent. Rien n'a été modifié.", file=sys.stderr)
        return 2
    errors = validate(new)
    if errors:
        print("ERREUR : nouveautes.json invalide. Rien n'a été modifié :", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2
    if "--check" in argv:
        print(f"OK : {len(new['items'])} élément(s) valide(s) pour le {new['date']}.")
        return 0

    known = {url_id(i["url"]) for i in base["items"]}
    added = duplicates = 0
    for it in new["items"]:
        uid = url_id(it["url"])
        if uid in known:
            duplicates += 1
            continue
        known.add(uid)
        it = dict(it, id=uid, date_ajout=new["date"])
        base["items"].append(it)
        added += 1

    base["syntheses"] = [s for s in base["syntheses"] if s["date"] != new["date"]]
    if new["resume_du_jour"].strip():
        base["syntheses"].append({"date": new["date"], "resume": new["resume_du_jour"].strip()})

    base["items"].sort(key=lambda i: (i["date_ajout"], i["date_publication"]), reverse=True)
    base["syntheses"].sort(key=lambda s: s["date"], reverse=True)

    atomic_write(BASE_FILE, json.dumps(base, ensure_ascii=False, indent=2) + "\n")
    atomic_write(DOCS / "feed.xml", build_feed(base["items"], base["syntheses"]))
    atomic_write(DOCS / "veille.md", build_markdown(base["items"], base["syntheses"]))
    atomic_write(DOCS / "index.html", build_index(base["items"], base["syntheses"]))
    (DOCS / ".nojekyll").touch()

    print(f"AJOUTES={added} DOUBLONS={duplicates} TOTAL={len(base['items'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
