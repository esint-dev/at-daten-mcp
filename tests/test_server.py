import json, subprocess, sys, unittest
from esint_at_daten import data
from esint_at_daten.server import handle

class T(unittest.TestCase):
    def test_feiertage_2027_match_oesterreich_gv_at(self):
        d={x["name"]:x["datum"] for x in data.feiertage(2027)}
        self.assertEqual(d["Ostermontag"],"2027-03-29"); self.assertEqual(d["Christi Himmelfahrt"],"2027-05-06")
        self.assertEqual(d["Pfingstmontag"],"2027-05-17"); self.assertEqual(d["Fronleichnam"],"2027-05-27")
        self.assertEqual(len(d),13)
    def test_ferien_wien_semester(self):
        f=[x for x in data.schulferien("wien") if x["name"]=="Semesterferien"]
        self.assertEqual(f,[{"name":"Semesterferien","von":"2027-02-01","bis":"2027-02-06"}])
    def test_ferien_tirol_sommer(self):
        self.assertIn({"name":"Sommerferien","von":"2027-07-10","bis":"2027-09-12"},data.schulferien("Tirol"))
    def test_bad_land(self):
        self.assertRaises(ValueError,data.schulferien,"Bayern")
    def test_svs_min(self):
        r=data.svs_schaetzung(0); self.assertEqual(r["pv_monat"],101.95); self.assertAlmostEqual(r["kv_monat"],37.48,delta=0.011)  # SVS-Tabelle rundet auf 37,48
    def test_svs_max(self):
        self.assertEqual(data.svs_schaetzung(10**7)["pv_monat"],1495.73)
    def test_stdio_roundtrip(self):
        inp="\n".join(json.dumps(m) for m in [{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}},
            {"jsonrpc":"2.0","method":"notifications/initialized"},{"jsonrpc":"2.0","id":2,"method":"tools/list"},
            {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"kleinunternehmergrenze","arguments":{}}}])
        out=subprocess.run([sys.executable,"-m","esint_at_daten.server"],input=inp,capture_output=True,text=True).stdout.splitlines()
        self.assertEqual(len(out),3); self.assertEqual(len(json.loads(out[1])["result"]["tools"]),5)
        self.assertIn("55000",json.loads(out[2])["result"]["content"][0]["text"])
if __name__=="__main__": unittest.main()
