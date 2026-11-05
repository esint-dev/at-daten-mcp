"""ESINT AT-Daten – MCP-Server (stdio, JSON-RPC 2.0, ohne Abhängigkeiten)."""
import json, sys
from . import data

TOOLS = {
 "feiertage": ({
   "type":"object",
   "properties":{
     "jahr":{"type":"integer","description":"Kalenderjahr als vierstellige Zahl, z. B. 2026 oder 2027 (1900–2200)."}
   },
   "required":["jahr"]},
   "Gibt die 13 gesetzlichen Feiertage Österreichs (Feiertagsruhegesetz/ARG) für ein Kalenderjahr zurück: Liste von {datum ISO-YYYY-MM-DD, name}. Österreichweit, nicht je Bundesland. Read-only, keine Auth. Bei ungültigem Jahr: Fehler. Für Schulferien statt Feiertagen schulferien nutzen.",
   lambda a: data.feiertage(int(a["jahr"]))),
 "schulferien": ({
   "type":"object",
   "properties":{
     "bundesland":{"type":"string","enum":data.BUNDESLAENDER,"description":"Österreichisches Bundesland (exakter Name aus der Enum, Groß/Klein egal)."},
     "schuljahr":{"type":"string","default":"2026/27","description":"Schuljahr im Format YYYY/YY; aktuell nur 2026/27."}
   },
   "required":["bundesland"]},
   "Gibt Schulferien (Herbst, Weihnachten, Semester, Ostern, Pfingsten, Sommer) für ein Bundesland zurück: Liste von {name, von, bis} (ISO-Daten). Quelle bmb.gv.at, Schuljahr 2026/27 (mittlere/höhere Schulen). Read-only. Nicht für gesetzliche Feiertage – dafür feiertage. Unbekanntes Bundesland oder Schuljahr → Fehler.",
   lambda a: data.schulferien(a["bundesland"], a.get("schuljahr","2026/27"))),
 "kleinunternehmergrenze": ({"type":"object","properties":{}},
   "Liefert die USt-Kleinunternehmergrenze AT 2026 als Objekt: umsatzgrenze_brutto_eur (55000), toleranz_prozent (10), toleranzgrenze_eur (60500), hinweis, quelle (USP). Read-only, keine Parameter, keine Auth. Unverbindlich, keine Steuerberatung.",
   lambda a: data.KLEINUNTERNEHMER_2026),
 "svs_werte": ({"type":"object","properties":{}},
   "Liefert die amtlichen SVS/GSVG-Referenzwerte 2026 (Beitragssätze PV/KV, Mindest-/Höchstbeitragsgrundlage, UV-Beitrag, Versicherungsgrenze neue Selbständige) als Objekt mit Quelle. Read-only, keine Berechnung. Für eine grobe Monats-/Jahresschätzung aus Gewinn svs_schaetzung nutzen. Unverbindlich.",
   lambda a: data.SVS_2026),
 "svs_schaetzung": ({
   "type":"object",
   "properties":{
     "jahresgewinn_eur":{"type":"number","description":"Jahresgewinn in Euro ≥ 0 (vor SV-Beiträgen; grober Richtwert, keine Steuerbemessung)."}
   },
   "required":["jahresgewinn_eur"]},
   "Schätzt grob monatliche/jährliche SVS-Beiträge 2026 (PV+KV+UV) aus Jahresgewinn: Objekt mit beitragsgrundlage_monat, pv_monat, kv_monat, uv_monat, summe_monat, summe_jahr, hinweis. Unverbindlicher Richtwert, keine Auth. Für reine Tabellenwerte (Sätze/Grenzen) svs_werte nutzen. Negativer Gewinn → Fehler.",
   lambda a: data.svs_schaetzung(float(a["jahresgewinn_eur"]))),
}

def handle(msg):
    m, i = msg.get("method"), msg.get("id")
    if i is None: return None
    if m == "initialize":
        r = {"protocolVersion":msg.get("params",{}).get("protocolVersion","2025-06-18"),"capabilities":{"tools":{}},
             "serverInfo":{"name":"esint-at-daten","version":"0.1.1"}}
    elif m == "ping": r = {}
    elif m == "tools/list":
        r = {"tools":[{"name":n,"description":d,"inputSchema":s} for n,(s,d,_) in TOOLS.items()]}
    elif m == "tools/call":
        p = msg.get("params",{}); t = TOOLS.get(p.get("name"))
        if not t: return {"jsonrpc":"2.0","id":i,"error":{"code":-32602,"message":"Unknown tool"}}
        try: r = {"content":[{"type":"text","text":json.dumps(t[2](p.get("arguments") or {}),ensure_ascii=False)}]}
        except (ValueError,KeyError,TypeError) as e: r = {"content":[{"type":"text","text":str(e)}],"isError":True}
    else: return {"jsonrpc":"2.0","id":i,"error":{"code":-32601,"message":"Method not found"}}
    return {"jsonrpc":"2.0","id":i,"result":r}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try: out = handle(json.loads(line))
        except json.JSONDecodeError: out = {"jsonrpc":"2.0","id":None,"error":{"code":-32700,"message":"Parse error"}}
        if out: sys.stdout.write(json.dumps(out, ensure_ascii=False)+"\n"); sys.stdout.flush()

if __name__ == "__main__": main()
