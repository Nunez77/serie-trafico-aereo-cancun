#!/usr/bin/env python3
"""Extrae la serie mensual de pasajeros del Aeropuerto de Tulum (TULÚM, grupo
GAFSACOMM) del workbook oficial de AFAC. La tabla dinámica del archivo solo
muestra un mes, pero el pivot-cache interno guarda los 12 meses x tipo
(nacional/internacional) x aeropuerto x 2006-2026. De ahí se extrae Tulum.

Como control de calidad, se valida el Cancún de AFAC contra el workbook de ASUR
(la misma métrica en dos fuentes oficiales distintas): coinciden al ~0.5% o mejor.

Fuente: AFAC, Estadística Operativa de Aeropuertos (gob.mx/afac), Excel por
aeropuerto. Salida: output/afac_tulum_tidy.csv (aeropuerto, anio, mes, nacional,
internacional, total)."""
import zipfile, xml.etree.ElementTree as ET, csv, sys

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

def load_cache():
    z = zipfile.ZipFile(XLSX)
    dfn = ET.fromstring(z.read("xl/pivotCache/pivotCacheDefinition1.xml"))
    SH = {}
    for i,cf in enumerate(dfn.findall(".//m:cacheField",NS)):
        si = cf.find("m:sharedItems",NS)
        SH[i] = [it.get("v") for it in list(si)] if si is not None else []
    rec = ET.fromstring(z.read("xl/pivotCache/pivotCacheRecords1.xml"))
    return SH, rec

def cellval(c):
    t = tag(c)
    if t=="x": return int(c.get("v"))
    if t=="n": return float(c.get("v"))
    if t=="m": return 0.0
    return c.get("v")

def series(SH, rec, apto_pred):
    OPC,TIP,YR,APT = SH[0],SH[1],SH[2],SH[4]
    pax = OPC.index("PASAJEROS/PASSENGERS")
    aidx = [i for i,v in enumerate(APT) if v and apto_pred(v)]
    out = {}   # (anio,mes) -> {nac,int}
    for r in rec.findall("m:r",NS):
        cs = [cellval(c) for c in list(r)]
        if cs[0]!=pax or cs[4] not in aidx: continue
        year = int(YR[cs[2]]); tipo = "nacional" if cs[1]==0 else "internacional"
        for mi in range(12):                       # cols 5..16 = ene..dic
            v = cs[5+mi]
            if v:                                  # 0/missing => no dato ese mes
                out.setdefault((year,mi+1),{"nacional":0,"internacional":0})
                out[(year,mi+1)][tipo] += int(v)
    return out

def main():
    SH, rec = load_cache()
    tul = series(SH, rec, lambda v: v.upper().startswith("TUL"))
    cun_afac = series(SH, rec, lambda v: v=="CANCUN")

    rows = []
    for (y,m) in sorted(tul):
        n = tul[(y,m)]["nacional"]; i = tul[(y,m)]["internacional"]
        rows.append({"aeropuerto":"TQO","anio":y,"mes":m,
                     "nacional":n,"internacional":i,"total":n+i})
    with open("output/afac_tulum_tidy.csv","w",newline="") as fh:
        w = csv.DictWriter(fh,fieldnames=["aeropuerto","anio","mes","nacional","internacional","total"])
        w.writeheader(); [w.writerow(r) for r in rows]

    print(f"Tulum: {len(rows)} meses  ({rows[0]['anio']}-{rows[0]['mes']:02d} a {rows[-1]['anio']}-{rows[-1]['mes']:02d})")
    print("Totales anuales Tulum (nac | int | total):")
    for y in sorted(set(r["anio"] for r in rows)):
        rs=[r for r in rows if r["anio"]==y]
        n=sum(r["nacional"] for r in rs); i=sum(r["internacional"] for r in rs)
        et="(parcial)" if len(rs)<12 else ""
        print(f"  {y}: {n:>9,} | {i:>9,} | {n+i:>10,}  {et}")

    # validacion Cancun AFAC vs ASUR
    d={}
    for r in csv.DictReader(open("output/asur_pax_tidy.csv")):
        if r["aeropuerto"]=="CUN": d[(int(r["anio"]),int(r["mes"]))]=int(r["total"])
    print("\nValidación Cancún AFAC vs ASUR (total anual):")
    for y in (2023,2024,2025):
        afac=sum(cun_afac[(y,m)]["nacional"]+cun_afac[(y,m)]["internacional"] for m in range(1,13) if (y,m) in cun_afac)
        asur=sum(d[(y,m)] for m in range(1,13))
        print(f"  {y}: AFAC={afac:,}  ASUR={asur:,}  dif={(afac/asur-1)*100:+.3f}%")

if __name__=="__main__":
    main()
