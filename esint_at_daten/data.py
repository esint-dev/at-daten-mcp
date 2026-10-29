"""Amtliche AT-Daten. Quellen siehe README. Unverbindlich, keine Steuer-/Rechtsberatung."""
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

def _r(x): return float(Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP))

BUNDESLAENDER = ["Burgenland","Kärnten","Niederösterreich","Oberösterreich","Salzburg","Steiermark","Tirol","Vorarlberg","Wien"]

def easter(y):
    a=y%19;b=y//100;c=y%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3
    h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7;m=(a+11*h+22*l)//451
    mo=(h+l-7*m+114)//31;da=(h+l-7*m+114)%31+1
    return date(y,mo,da)

def feiertage(year):
    """Gesetzliche Feiertage AT (Feiertagsruhegesetz 1957 §7 / ARG §7 Abs 2)."""
    if not 1900 <= year <= 2200: raise ValueError("year out of range")
    o=easter(year)
    f=[(date(year,1,1),"Neujahr"),(date(year,1,6),"Heilige Drei Könige"),
       (o+timedelta(1),"Ostermontag"),(date(year,5,1),"Staatsfeiertag"),
       (o+timedelta(39),"Christi Himmelfahrt"),(o+timedelta(50),"Pfingstmontag"),
       (o+timedelta(60),"Fronleichnam"),(date(year,8,15),"Mariä Himmelfahrt"),
       (date(year,10,26),"Nationalfeiertag"),(date(year,11,1),"Allerheiligen"),
       (date(year,12,8),"Mariä Empfängnis"),(date(year,12,25),"Christtag"),(date(year,12,26),"Stefanitag")]
    return [{"datum":d.isoformat(),"name":n} for d,n in sorted(f)]

_ALL = BUNDESLAENDER
_A = ["Niederösterreich","Wien"]; _B=["Burgenland","Kärnten"]
_C = ["Oberösterreich","Salzburg","Steiermark","Tirol","Vorarlberg"]
# bmb.gv.at ferientermine_26_27 (a: mittlere/höhere Schulen; Pflichtschulen üblicherweise gleich)
SCHULFERIEN = {"2026/27":[
 ("Herbstferien","2026-10-27","2026-10-31",_ALL),
 ("Weihnachtsferien","2026-12-24","2027-01-06",_ALL),
 ("Semesterferien","2027-02-01","2027-02-06",_A),
 ("Semesterferien","2027-02-08","2027-02-13",_B),
 ("Semesterferien","2027-02-15","2027-02-20",_C),
 ("Osterferien","2027-03-20","2027-03-29",_ALL),
 ("Pfingstferien","2027-05-15","2027-05-17",_ALL),
 ("Sommerferien","2027-07-03","2027-09-05",["Burgenland","Niederösterreich","Wien"]),
 ("Sommerferien","2027-07-10","2027-09-12",["Kärnten","Oberösterreich","Salzburg","Steiermark","Tirol","Vorarlberg"]),
]}

def schulferien(bundesland, schuljahr="2026/27"):
    bl = next((b for b in BUNDESLAENDER if b.lower()==bundesland.strip().lower()), None)
    if not bl: raise ValueError(f"Unbekanntes Bundesland. Erlaubt: {', '.join(BUNDESLAENDER)}")
    if schuljahr not in SCHULFERIEN: raise ValueError(f"Schuljahr nicht vorhanden: {list(SCHULFERIEN)}")
    return [{"name":n,"von":v,"bis":b} for n,v,b,l in SCHULFERIEN[schuljahr] if bl in l]

KLEINUNTERNEHMER_2026 = {"umsatzgrenze_brutto_eur":55000,"toleranz_prozent":10,"toleranzgrenze_eur":60500,
  "hinweis":"Grenze darf weder im laufenden noch im vorangegangenen Jahr überschritten sein (Brutto, seit 1.1.2025).",
  "quelle":"https://www.usp.gv.at/themen/steuern-finanzen/umsatzsteuer-ueberblick/weitere-informationen-zur-umsatzsteuer/weitere-steuertatbestaende-und-befreiungen/kleinunternehmen.html"}

SVS_2026 = {"pv_satz_prozent":18.5,"pv_satz_fsvg_prozent":20.0,"kv_satz_prozent":6.8,
  "mindestbeitragsgrundlage_monat_eur":551.10,"hoechstbeitragsgrundlage_monat_eur":8085.00,
  "uv_beitrag_monat_eur":12.95,"versicherungsgrenze_neue_selbstaendige_jahr_eur":6613.20,
  "quelle":"https://www.svs.at/cdscontent/load?contentid=10008.763406"}

def svs_schaetzung(jahresgewinn_eur):
    """Grobe Richtwert-Schätzung GSVG PV+KV+UV 2026 (ohne Selbständigenvorsorge, ohne Sonderfälle)."""
    if jahresgewinn_eur < 0: raise ValueError("Gewinn muss >= 0 sein")
    s=SVS_2026; bg=min(max(jahresgewinn_eur/12, s["mindestbeitragsgrundlage_monat_eur"]), s["hoechstbeitragsgrundlage_monat_eur"])
    pv=_r(Decimal(str(round(bg,2)))*Decimal(str(s["pv_satz_prozent"]))/100); kv=_r(Decimal(str(round(bg,2)))*Decimal(str(s["kv_satz_prozent"]))/100); uv=s["uv_beitrag_monat_eur"]
    m=round(pv+kv+uv,2)
    return {"beitragsgrundlage_monat":round(bg,2),"pv_monat":pv,"kv_monat":kv,"uv_monat":uv,"summe_monat":m,"summe_jahr":round(m*12,2),
            "hinweis":"Unverbindlicher Richtwert. Gewinn ohne hinzugerechnete SV-Beiträge; offizieller Rechner: https://www.svs.at/sva-beitrag"}
