#!/usr/bin/env python3
"""Split NACIONAL/INTERNACIONAL de Tulum (TULÚM) y del combinado
"Riviera aérea" = Cancún + Tulum, desde el pivot-cache de AFAC.
Serie anual 2019-2025 + acumulado ene-may 2026 vs 2025.

Motivación (no se escribe aquí): la pieza define la Riviera aérea como
Cancún + Tulum; se necesita el doméstico de la región COMPLETA, no solo Cancún.
Tulum (Aeropuerto Internacional Felipe Carrillo Puerto) abrió dic-2023, así que
2019-2022 = 0 y 2023 es solo diciembre.

Salidas (solo datos):
  output/afac_tulum_split_anual.csv       anual por serie x tipo
  output/afac_tulum_split_pico.csv        año pico, var desde pico, 2025 vs 2019
  output/afac_tulum_split_2026vs2025.csv  YTD ene-may 2026 vs 2025 por tipo

2026 en AFAC llega a MAYO; el 2026-vs-2025 es YTD ene-may (comparable).
Fuente: AFAC. Pivot-cache ya extraído; NO se re-descarga."""
import zipfile, xml.etree.ElementTree as ET, csv, collections

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

# code AFAC -> componentes. "Riviera aérea" = Cancún + Tulum.
CANCUN, TULUM = "CANCUN", "TULÚM"
SERIES = [
    ("Tulum", [TULUM]),
    ("Cancún", [CANCUN]),
    ("Riviera aérea (CUN+TUL)", [CANCUN, TULUM]),
]
TIPOS = ["nacional", "internacional", "total"]
YEARS = list(range(2019, 2027))
COMPLETE = [y for y in YEARS if y != 2026]
YTD_MONTHS = range(1, 6)
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
    need = {CANCUN, TULUM}

    mmes = collections.defaultdict(int)   # (apto, tipo, anio, mes)
    for r in rec.findall("m:r", NS):
        cs = [cellval(c) for c in list(r)]
        if cs[0] != pax: continue
        apto = APT[cs[4]]
        if apto not in need: continue
        tipo = TIPO_IDX[cs[1]]
        year = int(YR[cs[2]])
        for mi in range(12):
            v = cs[5 + mi]
            if v:
                mmes[(apto, tipo, year, mi + 1)] += int(v)

    def val(codes, tipo, year, months):
        tt = ["nacional", "internacional"] if tipo == "total" else [tipo]
        return sum(mmes[(a, t, year, m)]
                   for a in codes for t in tt for m in months)

    annual = lambda codes, tipo, y: val(codes, tipo, y, range(1, 13))
    ytd = lambda codes, tipo, y: val(codes, tipo, y, YTD_MONTHS)

    with open("output/afac_tulum_split_anual.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["serie", "tipo"] + [str(y) for y in YEARS] + ["nota_2026"])
        for name, codes in SERIES:
            for tipo in TIPOS:
                w.writerow([name, tipo]
                           + [annual(codes, tipo, y) for y in YEARS]
                           + ["parcial ene-may"])

    with open("output/afac_tulum_split_pico.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["serie", "tipo", "anio_pico", "valor_pico",
                    "valor_2025", "var_2025_vs_pico_pct",
                    "valor_2019", "var_2025_vs_2019_pct"])
        for name, codes in SERIES:
            for tipo in TIPOS:
                serie = {y: annual(codes, tipo, y) for y in COMPLETE}
                py = max(COMPLETE, key=lambda y: serie[y]); pv = serie[py]
                v25, v19 = serie[2025], serie[2019]
                w.writerow([name, tipo, py, pv, v25,
                            f"{(v25/pv-1)*100:+.1f}" if pv else "n/a",
                            v19, f"{(v25/v19-1)*100:+.1f}" if v19 else "n/a"])

    with open("output/afac_tulum_split_2026vs2025.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["serie", "tipo", "ytd_ene_may_2025",
                    "ytd_ene_may_2026", "var_pct"])
        for name, codes in SERIES:
            for tipo in TIPOS:
                a, b = ytd(codes, tipo, 2025), ytd(codes, tipo, 2026)
                w.writerow([name, tipo, a, b, f"{(b/a-1)*100:+.1f}" if a else "n/a"])

    # ================= consola =================
    print("== SERIE ANUAL DE PASAJEROS (AFAC) ==  [2026 = parcial ene-may]")
    print("   Tulum abrió dic-2023: 2019-2022 = 0, 2023 = solo diciembre.")
    hdr = f"{'serie':<24}{'tipo':<15}" + "".join(f"{y:>13}" for y in YEARS)
    print(hdr); print("-" * len(hdr))
    for name, codes in SERIES:
        for tipo in TIPOS:
            print(f"{name:<24}{tipo:<15}"
                  + "".join(f"{annual(codes,tipo,y):>13,}" for y in YEARS))
        print()

    print("== PICO PROPIO Y VARIACIÓN (años completos 2019-2025) ==")
    print(f"{'serie':<24}{'tipo':<15}{'pico':>6}{'valor_pico':>14}"
          f"{'2025':>14}{'25 vs pico':>12}{'25 vs 19':>11}")
    for name, codes in SERIES:
        for tipo in TIPOS:
            serie = {y: annual(codes, tipo, y) for y in COMPLETE}
            py = max(COMPLETE, key=lambda y: serie[y]); pv = serie[py]
            v25, v19 = serie[2025], serie[2019]
            vp = f"{(v25/pv-1)*100:+.1f}%" if pv else "n/a"
            v9 = f"{(v25/v19-1)*100:+.1f}%" if v19 else "n/a"
            print(f"{name:<24}{tipo:<15}{py:>6}{pv:>14,}{v25:>14,}{vp:>12}{v9:>11}")
    print()

    print("== 2026 vs 2025, YTD ene-may (comparable) ==")
    print(f"{'serie':<24}{'tipo':<15}{'2025':>14}{'2026':>14}{'var':>10}")
    for name, codes in SERIES:
        for tipo in TIPOS:
            a, b = ytd(codes, tipo, 2025), ytd(codes, tipo, 2026)
            vr = f"{(b/a-1)*100:+.1f}%" if a else "n/a"
            print(f"{name:<24}{tipo:<15}{a:>14,}{b:>14,}{vr:>10}")


if __name__ == "__main__":
    main()
