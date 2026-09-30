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


def build_index(items, syntheses) -> str:
    body = []
    for day, block in group_by_day(items, syntheses, MD_DAYS):
        body.append(f'<section id="{day}"><h2>{day}</h2>')
        if block["resume"].strip():
            body.append(f'<p class="resume">{escape(block["resume"])}</p>')
        for i in block["items"]:
            body.append(
                f'<article><h3><span class="tag">{escape(THEMES[i["theme"]])}</span> '
                f'<a href="{escape(i["url"])}">{escape(i["titre"])}</a></h3>{item_html(i)}</article>'
            )
        body.append("</section>")
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(FEED_TITLE)}</title>"
        f'<link rel="alternate" type="application/rss+xml" href="{SITE_URL}/feed.xml">'
        "<style>body{font:16px/1.5 system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem}"
        "h3{margin:1.2rem 0 .2rem}.tag{font-size:.7em;background:#e8eefc;border-radius:4px;padding:.1em .5em}"
        ".resume{background:#f5f5f5;padding:.6rem .8rem;border-radius:6px}article{margin-bottom:1rem}"
        "@media(prefers-color-scheme:dark){body{background:#111;color:#ddd}a{color:#8ab4f8}"
        ".resume{background:#1e1e1e}.tag{background:#26324d}}</style></head><body>"
        f'<h1>{escape(FEED_TITLE)}</h1><p><a href="feed.xml">Flux RSS</a></p>'
        + "".join(body)
        + "</body></html>\n"
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
