"""ESINT AT-Daten – MCP-Server (stdio, JSON-RPC 2.0, ohne Abhängigkeiten)."""
import json, sys
from . import data

TOOLS = {
 "feiertage": ({"type":"object","properties":{"jahr":{"type":"integer"}},"required":["jahr"]},
   "Gesetzliche Feiertage in Österreich für ein Jahr.", lambda a: data.feiertage(int(a["jahr"]))),
 "schulferien": ({"type":"object","properties":{"bundesland":{"type":"string","enum":data.BUNDESLAENDER},"schuljahr":{"type":"string","default":"2026/27"}},"required":["bundesland"]},
   "Schulferien je Bundesland (Schuljahr 2026/27, Quelle bmb.gv.at).", lambda a: data.schulferien(a["bundesland"], a.get("schuljahr","2026/27"))),
 "kleinunternehmergrenze": ({"type":"object","properties":{}},
   "Kleinunternehmergrenze Umsatzsteuer AT 2026.", lambda a: data.KLEINUNTERNEHMER_2026),
 "svs_werte": ({"type":"object","properties":{}},
   "SVS/GSVG-Werte 2026 (Beitragssätze, Mindest-/Höchstbeitragsgrundlage).", lambda a: data.SVS_2026),
 "svs_schaetzung": ({"type":"object","properties":{"jahresgewinn_eur":{"type":"number"}},"required":["jahresgewinn_eur"]},
   "Grobe SVS-Beitragsschätzung 2026 aus Jahresgewinn (unverbindlich).", lambda a: data.svs_schaetzung(float(a["jahresgewinn_eur"]))),
}

def handle(msg):
    m, i = msg.get("method"), msg.get("id")
    if i is None: return None
    if m == "initialize":
        r = {"protocolVersion":msg.get("params",{}).get("protocolVersion","2025-06-18"),"capabilities":{"tools":{}},
             "serverInfo":{"name":"esint-at-daten","version":"0.1.0"}}
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
