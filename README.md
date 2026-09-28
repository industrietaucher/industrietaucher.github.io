# industrietaucher.ch

Statische Website, ausgeliefert über GitHub Pages (Domain in `CNAME`).

## Aufbau

- `src/*.html`: Inhalt jeder Seite. Erste Zeile ist ein JSON-Kommentar mit Titel und Beschreibung.
- `tools/build.py`: setzt Kopf, Navigation und Fusszeile um den Inhalt und schreibt die fertigen Seiten ins Hauptverzeichnis. Erzeugt auch `sitemap.xml`.
- `site.css`, `site.js`: gemeinsames Design (hell und dunkel) und Script.
- `img/`: Bilder. Dateien mit `eigen-` sind eigene Einsatzfotos, die übrigen Stockfotos von Pexels.
- `tools/flyer.html` und `tools/build_flyer.ps1`: Firmenflyer, wird mit Edge als `industrietaucher-flyer.pdf` gedruckt.

## Ändern

1. Text in `src/<seite>.html` anpassen (nicht in der Datei im Hauptverzeichnis, die wird überschrieben).
2. `python tools/build.py`
3. Flyer bei Bedarf: lokalen Server starten (`python -m http.server 8765`), dann `tools/build_flyer.ps1`.
4. Commit und Push.
