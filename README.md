# ESINT AT-Daten (MCP-Server)

Österreich-Daten für KI-Assistenten über das Model Context Protocol (stdio, ohne Abhängigkeiten, Python ≥ 3.9).

| Tool | Inhalt |
|---|---|
| `feiertage` | gesetzliche Feiertage AT für ein Jahr |
| `schulferien` | Schulferien je Bundesland, Schuljahr 2026/27 |
| `kleinunternehmergrenze` | USt-Kleinunternehmergrenze 2026 (55.000 € brutto, 10 % Toleranz) |
| `svs_werte` | GSVG-Beitragssätze, Mindest-/Höchstbeitragsgrundlage 2026 |
| `svs_schaetzung` | grobe SVS-Beitragsschätzung aus Jahresgewinn |

## Installation
```bash
pip install git+https://github.com/esint-dev/at-daten-mcp
```
Claude Desktop / Cursor `mcpServers`:
```json
{"esint-at-daten": {"command": "esint-at-daten"}}
```
Tests: `python -m unittest`

## Quellen (je doppelt geprüft, Stand 29.10.2026)
- Schulferien: bmb.gv.at – https://www.bmb.gv.at/Themen/schule/schulpraxis/termine/ferientermine_26_27.html, gegengeprüft mit oesterreich.gv.at Ferienkalender 2026/27 (https://www.oesterreich.gv.at/de/themen/bildung_und_ausbildung/schulen/Seite.1100114)
- Feiertage: Feiertagsruhegesetz/ARG §7; Termine 2026/27 gegengeprüft mit oesterreich.gv.at (s. o.)
- Kleinunternehmergrenze: USP – https://www.usp.gv.at/themen/steuern-finanzen/umsatzsteuer-ueberblick/weitere-informationen-zur-umsatzsteuer/weitere-steuertatbestaende-und-befreiungen/kleinunternehmen.html, gegengeprüft mit https://www.usp.gv.at/aktuelles/newsliste/kleinunternehmerregelung-ab-2025.html
- SVS: https://www.svs.at/cdscontent/load?contentid=10008.763406 und https://www.svs.at/cdscontent/?contentid=10007.816718, gegengeprüft mit WKO Sozialversicherungswerte 2026

Hinweise: Schulferien gelten für mittlere/höhere Schulen, Pflichtschulen üblicherweise gleich; schulautonome Tage und Landespatrone nicht enthalten. Alle Werte unverbindlich, keine Steuer- oder Rechtsberatung.

Auch als Apify-Actor (pro Abruf 0,005 $): https://apify.com/esint/at-daten

Docker: `docker run -i --rm ghcr.io/esint-dev/at-daten-mcp:0.1.0`

<!-- mcp-name: io.github.esint-dev/at-daten-mcp -->

## Werbung
Anzeige (eigenes Produkt): Einnahmen-Ausgaben-Paket für Kleinunternehmer AT – https://gumroad.com/l/hipixo (gratis Lite)

Lizenz: MIT · © ESINT
