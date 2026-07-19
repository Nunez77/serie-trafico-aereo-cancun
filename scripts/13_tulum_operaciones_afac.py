#!/usr/bin/env python3
"""Tulum (TQO): operaciones y pasajeros, acumulado ene-may 2026 vs 2025.

Pregunta que responde: la prensa reporta un recorte cercano al 30% de
frecuencias en Tulum. Operaciones es la variable que mide frecuencias;
pasajeros no. Aquí salen las dos, separadas, con su split nacional e
internacional.

Universo: AFAC, Estadística Operativa de Aeropuertos. Pasajeros de terminal en
ambos sentidos y todas las nacionalidades; operaciones son vuelos. NO se mezcla
con ASUR (que excluye tránsito y aviación general) ni con UPM (entradas de
extranjeros). Tulum no es aeropuerto de ASUR, así que AFAC es la única fuente.

2026 en AFAC llega a MAYO. El comparativo es YTD ene-may contra ene-may.

Salida: output/afac_tulum_operaciones_2026vs2025.csv
Fuente: pivot-cache ya extraído; NO se re-descarga."""
import zipfile, xml.etree.ElementTree as ET, collections, csv

AFAC = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]
MESES = range(1, 6)          # enero a mayo
APTS = {"TULÚM": "Tulum", "CANCUN": "Cancún"}


def leer():
    z = zipfile.ZipFile(AFAC)
    dfn = ET.fromstring(z.read("xl/pivotCache/pivotCacheDefinition1.xml"))
    SH = {}
    for i, cf in enumerate(dfn.findall(".//m:cacheField", NS)):
        si = cf.find("m:sharedItems", NS)
        SH[i] = [it.get("v") for it in list(si)] if si is not None else []
    rec = ET.fromstring(z.read("xl/pivotCache/pivotCacheRecords1.xml"))
    OPC, YR, APT = SH[0], SH[2], SH[4]
    OP = OPC.index("OPERACIONES/ FLIGHTS")
    PAX = OPC.index("PASAJEROS/PASSENGERS")

    def cv(c):
        t = tag(c)
        if t == "x": return int(c.get("v"))
        if t == "n": return float(c.get("v"))
        if t == "m": return 0.0
        return c.get("v")

    # (aeropuerto, metrica, tipo, anio) -> acumulado ene-may
    d = collections.defaultdict(int)
    for r in rec.findall("m:r", NS):
        cs = [cv(c) for c in list(r)]
        apt = APT[cs[4]]
        if apt not in APTS: continue
        if cs[0] not in (OP, PAX): continue
        tipo = "internacional" if cs[1] == 1 else "nacional"
        met = "operaciones" if cs[0] == OP else "pasajeros"
        y = int(YR[cs[2]])
        if y not in (2025, 2026): continue
        for mi in MESES:
            v = cs[5 + mi - 1]
            if v: d[(APTS[apt], met, tipo, y)] += int(v)
    return d


def var(a, b):
    return (b - a) / a * 100 if a else float("nan")


if __name__ == "__main__":
    d = leer()
    filas = []
    for apt in ("Tulum", "Cancún"):
        for met in ("operaciones", "pasajeros"):
            tot = {}
            for tipo in ("nacional", "internacional"):
                a, b = d[(apt, met, tipo, 2025)], d[(apt, met, tipo, 2026)]
                filas.append([apt, met, tipo, a, b, round(var(a, b), 1)])
                tot[tipo] = (a, b)
            a = sum(v[0] for v in tot.values()); b = sum(v[1] for v in tot.values())
            filas.append([apt, met, "total", a, b, round(var(a, b), 1)])

    with open("output/afac_tulum_operaciones_2026vs2025.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["aeropuerto", "metrica", "tipo", "ytd_ene_may_2025", "ytd_ene_may_2026", "var_pct"])
        w.writerows(filas)

    anch = max(len(r[0]) for r in filas)
    print(f'{"aeropuerto":<{anch}} {"metrica":<12} {"tipo":<14} {"2025":>10} {"2026":>10} {"var":>8}')
    for r in filas:
        print(f"{r[0]:<{anch}} {r[1]:<12} {r[2]:<14} {r[3]:>10,} {r[4]:>10,} {r[5]:>7.1f}%")

    # tamaño de avión implícito, para no confundir menos vuelos con menos gente
    print()
    for apt in ("Tulum", "Cancún"):
        for y in (2025, 2026):
            op = sum(d[(apt, "operaciones", t, y)] for t in ("nacional", "internacional"))
            px = sum(d[(apt, "pasajeros", t, y)] for t in ("nacional", "internacional"))
            if op: print(f"{apt} {y}: {px/op:.1f} pasajeros por operación")
