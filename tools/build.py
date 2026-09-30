# -*- coding: utf-8 -*-
"""Baut die Seiten von industrietaucher.ch.

Inhalt jeder Seite liegt in src/<name>.html. Die erste Zeile ist ein
JSON-Kommentar mit Metadaten, z.B.:
  <!--{"title": "...", "description": "...", "nav": "leistungen"}-->
Dieses Script setzt Kopf, Navigation und Fusszeile drumherum und schreibt
<name>.html ins Repo-Root (das GitHub Pages ausliefert).

Aufruf:  python tools/build.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
BASE_URL = "https://industrietaucher.ch/"
PHONE = "+41 77 921 71 36"
PHONE_TEL = "+41779217136"
MAIL = "info@industrietaucher.ch"
FLYER = "industrietaucher-flyer.pdf?v=20260928b"

LEISTUNGEN = [
    ("inspektion.html", "Inspektion und Zustandsaufnahme"),
    ("suche-bergung.html", "Suche und Bergung"),
    ("unterwasserarbeiten.html", "Unterwasserarbeiten"),
    ("sprengtechnik.html", "Gefahrstoffe und Sprengtechnik"),
    ("dokumentation.html", "Dokumentation und Gutachten"),
    ("engineering.html", "Engineering und Entwicklung"),
    ("projektleitung.html", "Projektleitung"),
    ("notfall.html", "Notfall und Eilaufträge"),
]
LEISTUNG_FILES = {f for f, _ in LEISTUNGEN}

MAIN_NAV = [
    ("behoerden.html", "Öffentliche Hand"),
    ("referenzen.html", "Referenzen"),
    ("firma.html", "Firma"),
    ("jobs.html", "Jobs"),
    ("kontakt.html", "Kontakt"),
]

GOOGLE_URL = "https://maps.google.com/?cid=7272441535974230158"

# Auftraggeber: (Logo-Datei oder None, Name, Zusatz)
# Auftraggeber: (Logo-Datei oder None, Name, Anzeigebreite in px)
# Breiten gleichen die sichtbare Fläche an (breite Logos breiter, hohe schmaler).
CLIENTS = [
    ("img/logos/stadt-zuerich.svg", "Stadt Zürich", 195),
    ("img/logos/stadt-luzern.svg", "Stadt Luzern", 123),
    ("img/logos/stadt-thun.svg", "Stadt Thun", 131),
    (None, "RIMO AG", 0),
    ("img/logos/hotel-vitznauerhof.svg", "Hotel Vitznauerhof", 117),
]

GOOGLE_G = ('<svg class="g" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/>'
            '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
            '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
            '<path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>')


def clients_block():
    tiles = []
    for logo, name, width in CLIENTS:
        if logo:
            tiles.append(f'      <div class="logo-tile"><img src="{logo}" alt="{name}" style="width:{width}px" loading="lazy"></div>')
        else:
            tiles.append(f'      <div class="logo-tile"><span class="wordmark">{name}</span></div>')
    return ('    <div class="logo-wall">\n' + "\n".join(tiles) + '\n    </div>')


def rating_block():
    return (f'<a class="rating" href="{GOOGLE_URL}" target="_blank" rel="noopener">{GOOGLE_G}'
            '<span class="score">5,0</span><span><span class="stars" aria-label="5 von 5 Sternen">★★★★★</span>'
            '<small>10 Google-Rezensionen ansehen</small></span></a>')


FLAG_SVG = ('<svg viewBox="0 0 30 20" aria-hidden="true"><rect class="fl-w" x="0.5" y="0.5" '
            'width="15" height="19" stroke-width="1"/><path class="fl-b" d="M15 0H30L23 10L30 20H15Z"/></svg>')


def cur(page, target):
    return ' aria-current="page"' if page == target else ""


def header(page):
    sub = "\n".join(
        f'            <a href="{f}"{cur(page, f)}>{label}</a>' for f, label in LEISTUNGEN)
    leist_cur = ' aria-current="page"' if page in LEISTUNG_FILES else ""
    main = "\n".join(
        f'      <li><a href="{f}"{cur(page, f)}>{label}</a></li>' for f, label in MAIN_NAV)
    return f'''<div class="util">
  <div class="wrap">
    <span>Unterwasserarbeiten und Engineering · schweizweit</span>
    <div class="u-r">
      <a href="tel:{PHONE_TEL}">{PHONE}</a>
      <a class="u-mail" href="mailto:{MAIL}">{MAIL}</a>
      <a class="u-notfall" href="notfall.html">24/7 Notfall</a>
    </div>
  </div>
</div>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Industrietaucher.ch, Startseite">
      {FLAG_SVG}
      <span class="brand-name">Industrietaucher.ch<small>Unterwasserarbeiten und Engineering</small></span>
    </a>
    <ul class="menu" id="menu">
      <li class="has-sub"><a href="index.html#leistungen"{leist_cur}>Leistungen</a>
        <div class="submenu"><div class="submenu-inner">
{sub}
        </div></div>
      </li>
{main}
      <li><a class="btn-notfall-nav" href="https://notfalltaucher.ch" target="_blank" rel="noopener">Notfall</a></li>
    </ul>
    <div class="nav-actions">
      <a class="icon-btn flyer-link" href="{FLYER}" target="_blank" rel="noopener" title="Firmenflyer (PDF)" aria-label="Firmenflyer herunterladen (PDF)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 21h16"/></svg>
      </a>
      <button class="icon-btn theme-btn" id="themeToggle" aria-label="Hell- oder Dunkelmodus wechseln" title="Hell / Dunkel">
        <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>
      <button class="icon-btn burger" id="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>'''


def footer():
    leist = "\n".join(f'          <li><a href="{f}">{label}</a></li>' for f, label in LEISTUNGEN)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <h4>Industrietaucher.ch</h4>
        <p>Unterwasserarbeiten, Inspektion und Engineering für Behörden, Gemeinden, Werke und Industrie. Sitz in Luzern, Einsätze schweizweit.</p>
      </div>
      <div>
        <h4>Leistungen</h4>
        <ul>
{leist}
        </ul>
      </div>
      <div>
        <h4>Unternehmen</h4>
        <ul>
          <li><a href="behoerden.html">Öffentliche Hand</a></li>
          <li><a href="referenzen.html">Referenzen</a></li>
          <li><a href="firma.html">Firma</a></li>
          <li><a href="jobs.html">Jobs</a></li>
          <li><a href="{FLYER}" target="_blank" rel="noopener">Firmenflyer (PDF)</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontakt</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li><a href="kontakt.html">Offerte anfordern</a></li>
          <li><a href="https://notfalltaucher.ch" target="_blank" rel="noopener">notfalltaucher.ch</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© 2026 Industrietaucher.ch</span>
      <span><a href="impressum.html">Impressum und Datenschutz</a> · <a href="agb.html">AGB</a></span>
    </div>
  </div>
</footer>'''


def page(name, meta, body):
    canonical = BASE_URL if name == "index.html" else BASE_URL + name
    og_image = BASE_URL + meta.get("image", "img/taucher-gesichert-oberflaeche.jpg")
    extra_head = meta.get("head", "")
    robots = meta.get("robots", "index, follow")
    return f'''<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{meta["title"]}</title>
<meta name="description" content="{meta["description"]}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Industrietaucher.ch">
<meta property="og:locale" content="de_CH">
<meta property="og:title" content="{meta["title"]}">
<meta property="og:description" content="{meta["description"]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="site.css?v=9">
{extra_head}</head>
<body>

<!-- Diese Datei wird von tools/build.py erzeugt. Inhalt bearbeiten in src/{name} -->
{header(name)}

<main>
{body.strip()}
</main>

{footer()}

<div class="lightbox" id="lightbox" onclick="closeLightbox()"><img src="" alt=""></div>
<script src="site.js?v=6"></script>
</body>
</html>
'''


def main():
    built = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, fn), encoding="utf-8").read()
        m = re.match(r"\s*<!--(\{.*?\})-->\s*", raw, re.S)
        if not m:
            raise SystemExit(f"{fn}: Metadaten-Kommentar fehlt")
        meta = json.loads(m.group(1))
        body = raw[m.end():].replace("<!--#clients-->", clients_block()).replace("<!--#rating-->", rating_block())
        out = page(fn, meta, body)
        with open(os.path.join(ROOT, fn), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out)
        built.append(fn)

    # Sitemap
    urls = []
    for fn in built:
        loc = BASE_URL if fn == "index.html" else BASE_URL + fn
        prio = "1.0" if fn == "index.html" else ("0.3" if fn in ("agb.html", "impressum.html") else "0.8")
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-28</lastmod>\n    <priority>{prio}</priority>\n  </url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + "\n".join(urls) + "\n</urlset>\n")
    print("Gebaut:", ", ".join(built))


if __name__ == "__main__":
    main()
