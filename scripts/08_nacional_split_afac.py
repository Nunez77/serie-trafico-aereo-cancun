#!/usr/bin/env python3
"""Split NACIONAL/INTERNACIONAL del TOTAL NACIONAL (los 68 aeropuertos) y de los
destinos de playa comparables (Los Cabos, Puerto Vallarta, Mazatlán), desde el
pivot-cache de AFAC. Serie anual 2019-2025 + acumulado ene-may 2026.

Motivación de la pieza (no se escribe aquí, solo se generan datos):
  - ¿El doméstico de México cae como el de Quintana Roo/Riviera, o no? El TOTAL
    NACIONAL con split es el contrafactual macro.
  - ¿El doméstico de otros destinos de playa crece mientras el de Cancún cae, o
    caen todos parejo? (Los Cabos, Puerto Vallarta, Mazatlán con split.)

Reutiliza la dimensión TIPO (cacheField 1) igual que 07_region_afac.py.

Salidas (solo datos):
  output/afac_nacsplit_anual.csv       anual por serie x tipo (nac/intl/total)
  output/afac_nacsplit_pico.csv        año pico, var desde pico, 2025 vs 2019
  output/afac_nacsplit_2026vs2025.csv  YTD ene-may 2026 vs 2025 por tipo

Nota: 2026 en AFAC llega a MAYO. El 2026-vs-2025 es YTD ene-may (comparable).
Fuente: AFAC, Estadística Operativa de Aeropuertos. Pivot-cache ya extraído; NO
se re-descarga."""
import zipfile, xml.etree.ElementTree as ET, csv, collections

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

# etiqueta AFAC -> nombre de reporte. None especial = TOTAL NACIONAL (68 aptos).
PLAYA = {
    "SAN JOSE DEL CABO": "Los Cabos",
    "PUERTO VALLARTA": "Puerto Vallarta",
    "MAZATLAN": "Mazatlán",
}
NACIONAL_LABEL = "TOTAL NACIONAL"
TIPOS = ["nacional", "internacional", "total"]
YEARS = list(range(2019, 2027))        # 2026 = parcial ene-may
COMPLETE = [y for y in YEARS if y != 2026]
YTD_MONTHS = range(1, 6)               # ene-may
TIPO_IDX = {0: "nacional", 1: "internacional"}


def load():
    z = zipfile.ZipFile(XLSX)
    dfn = ET.fromstring(z.read("xl/pivotCache/pivotCacheDefinition1.xml"))
    SH = {}
    for i, cf in enumerate(dfn.findall(".//m:cacheField", NS)):
        si = cf.find("m:sharedItems", NS)
        SH[i] = [it.get("v") for it in list(si)] if si is not None else []
    rec = ET.fromstring(z.read("xl/pivotCache/pivotCacheRecords1.xml"))
    return SH, rec


def cellval(c):
    t = tag(c)
    if t == "x": return int(c.get("v"))
    if t == "n": return float(c.get("v"))
    if t == "m": return 0.0
    return c.get("v")


def main():
    SH, rec = load()
    OPC, TYP, YR, APT = SH[0], SH[1], SH[2], SH[4]
    pax = OPC.index("PASAJEROS/PASSENGERS")

    # por aeropuerto: (apto, tipo, anio, mes) ; y NACIONAL: (tipo, anio, mes)
    mmes = collections.defaultdict(int)
    nac = collections.defaultdict(int)
    for r in rec.findall("m:r", NS):
        cs = [cellval(c) for c in list(r)]
        if cs[0] != pax: continue
        apto = APT[cs[4]]
        tipo = TIPO_IDX[cs[1]]
        year = int(YR[cs[2]])
        for mi in range(12):
            v = cs[5 + mi]
            if v:
                nac[(tipo, year, mi + 1)] += int(v)
                if apto in PLAYA:
                    mmes[(apto, tipo, year, mi + 1)] += int(v)

    SERIES = [(NACIONAL_LABEL, None)] + [(name, code) for code, name in PLAYA.items()]

    def val(code, tipo, year, months):
        tt = ["nacional", "internacional"] if tipo == "total" else [tipo]
        if code is None:
            return sum(nac[(t, year, m)] for t in tt for m in months)
        return sum(mmes[(code, t, year, m)] for t in tt for m in months)

    annual = lambda code, tipo, y: val(code, tipo, y, range(1, 13))
    ytd = lambda code, tipo, y: val(code, tipo, y, YTD_MONTHS)

    # ---- 1) anual ----
    with open("output/afac_nacsplit_anual.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["serie", "tipo"] + [str(y) for y in YEARS] + ["nota_2026"])
        for name, code in SERIES:
            for tipo in TIPOS:
                w.writerow([name, tipo]
                           + [annual(code, tipo, y) for y in YEARS]
                           + ["parcial ene-may"])

    # ---- 2) pico ----
    with open("output/afac_nacsplit_pico.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["serie", "tipo", "anio_pico", "valor_pico",
                    "valor_2025", "var_2025_vs_pico_pct",
                    "valor_2019", "var_2025_vs_2019_pct"])
        for name, code in SERIES:
            for tipo in TIPOS:
                serie = {y: annual(code, tipo, y) for y in COMPLETE}
                py = max(COMPLETE, key=lambda y: serie[y]); pv = serie[py]
                v25, v19 = serie[2025], serie[2019]
                w.writerow([name, tipo, py, pv, v25,
                            f"{(v25/pv-1)*100:+.1f}" if pv else "n/a",
                            v19, f"{(v25/v19-1)*100:+.1f}" if v19 else "n/a"])

    # ---- 3) 2026 vs 2025 YTD ----
    with open("output/afac_nacsplit_2026vs2025.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["serie", "tipo", "ytd_ene_may_2025",
                    "ytd_ene_may_2026", "var_pct"])
        for name, code in SERIES:
            for tipo in TIPOS:
                a, b = ytd(code, tipo, 2025), ytd(code, tipo, 2026)
                w.writerow([name, tipo, a, b, f"{(b/a-1)*100:+.1f}" if a else "n/a"])

    # ================= consola =================
    print("== SERIE ANUAL DE PASAJEROS (AFAC) ==  [2026 = parcial ene-may]")
    hdr = f"{'serie':<16}{'tipo':<15}" + "".join(f"{y:>13}" for y in YEARS)
    print(hdr); print("-" * len(hdr))
    for name, code in SERIES:
        for tipo in TIPOS:
            print(f"{name:<16}{tipo:<15}"
                  + "".join(f"{annual(code,tipo,y):>13,}" for y in YEARS))
        print()

    print("== PICO PROPIO Y VARIACIÓN (años completos 2019-2025) ==")
    print(f"{'serie':<16}{'tipo':<15}{'pico':>6}{'valor_pico':>14}"
          f"{'2025':>14}{'25 vs pico':>12}{'25 vs 19':>11}")
    for name, code in SERIES:
        for tipo in TIPOS:
            serie = {y: annual(code, tipo, y) for y in COMPLETE}
            py = max(COMPLETE, key=lambda y: serie[y]); pv = serie[py]
            v25, v19 = serie[2025], serie[2019]
            vp = f"{(v25/pv-1)*100:+.1f}%" if pv else "n/a"
            v9 = f"{(v25/v19-1)*100:+.1f}%" if v19 else "n/a"
            print(f"{name:<16}{tipo:<15}{py:>6}{pv:>14,}{v25:>14,}{vp:>12}{v9:>11}")
    print()

    print("== 2026 vs 2025, YTD ene-may (comparable) ==")
    print(f"{'serie':<16}{'tipo':<15}{'2025':>14}{'2026':>14}{'var':>10}")
    for name, code in SERIES:
        for tipo in TIPOS:
            a, b = ytd(code, tipo, 2025), ytd(code, tipo, 2026)
            vr = f"{(b/a-1)*100:+.1f}%" if a else "n/a"
            print(f"{name:<16}{tipo:<15}{a:>14,}{b:>14,}{vr:>10}")
    print()

    # sanity: TOTAL NACIONAL total anual debe coincidir con 06 (afac_playa_anual)
    try:
        for r in csv.DictReader(open("output/afac_playa_anual.csv")):
            if r["aeropuerto"] == "TOTAL NACIONAL":
                ok = all(int(r[str(y)]) == annual(None, "total", y) for y in YEARS)
                print(f"[check] TOTAL NACIONAL total vs 06_playa_afac: "
                      f"{'OK, idéntico' if ok else 'DIFIERE'}")
                break
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    main()
