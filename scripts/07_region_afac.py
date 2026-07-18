#!/usr/bin/env python3
"""Cozumel y Chetumal (con Cancún de referencia) desde el pivot-cache de AFAC,
CON split NACIONAL/INTERNACIONAL. Serie anual 2019-2025 + acumulado ene-may 2026.

Motivación de la pieza (no se escribe aquí, solo se generan datos):
  - Chetumal = contrafactual (mismo estado, misma macro/gobierno, no es destino
    turístico) frente a la Riviera aérea (Cancún).
  - Cozumel = decidir si entra en la definición de región o queda aparte.
  - Cancún con split = validar si AFAC reproduce el −6.0% nacional / −2.3%
    internacional (ene-may 2026) que reporta ASUR, para usar una sola fuente.

El pivot-cache trae la dimensión TIPO (cacheField 1: NACIONAL/INTERNACIONAL),
que el script 06 sumaba. Aquí se conserva.

Salidas (solo datos):
  output/afac_region_anual.csv       anual por aeropuerto x tipo (nac/intl/total)
  output/afac_region_pico.csv        año pico, var desde pico, 2025 vs 2019
  output/afac_region_2026vs2025.csv  YTD ene-may 2026 vs 2025 por tipo
  output/afac_region_validacion.csv  AFAC vs ASUR (Cancún y Cozumel) por tipo

Nota: 2026 en AFAC llega a MAYO. Anual 2026 es parcial; el 2026-vs-2025 se hace
YTD sobre meses comunes (ene-may). Chetumal es aeropuerto ASA, no está en el
workbook de ASUR: no hay cruce posible (solo Cancún y Cozumel se validan).

Fuente: AFAC, Estadística Operativa de Aeropuertos (gob.mx/afac). Pivot-cache ya
extraído en data/afac_aeropuertos_2006_2026.xlsx; NO se re-descarga."""
import zipfile, xml.etree.ElementTree as ET, csv, collections

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

AIRPORTS = {"CANCUN": "Cancún", "COZUMEL": "Cozumel", "CHETUMAL": "Chetumal"}
TIPOS = ["nacional", "internacional", "total"]
YEARS = list(range(2019, 2027))        # 2026 = parcial ene-may
COMPLETE = [y for y in YEARS if y != 2026]
YTD_MONTHS = range(1, 6)               # ene-may (último mes disponible en 2026)
# mapeo AFAC-code de tipo -> etiqueta interna (por índice de sharedItems)
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

    # (apto_code, tipo_label, anio, mes) -> pasajeros
    mmes = collections.defaultdict(int)
    for r in rec.findall("m:r", NS):
        cs = [cellval(c) for c in list(r)]
        if cs[0] != pax: continue
        apto = APT[cs[4]]
        if apto not in AIRPORTS: continue
        tipo = TIPO_IDX[cs[1]]
        year = int(YR[cs[2]])
        for mi in range(12):
            v = cs[5 + mi]
            if v:
                mmes[(apto, tipo, year, mi + 1)] += int(v)

    def val(apto, tipo, year, months):
        """suma de pasajeros de un aeropuerto/tipo/año sobre un rango de meses.
        tipo='total' => nacional+internacional."""
        tt = ["nacional", "internacional"] if tipo == "total" else [tipo]
        return sum(mmes[(apto, t, year, m)] for t in tt for m in months)

    def annual(apto, tipo, year):
        return val(apto, tipo, year, range(1, 13))

    def ytd(apto, tipo, year):
        return val(apto, tipo, year, YTD_MONTHS)

    # ---- 1) totales anuales por aeropuerto x tipo ----
    with open("output/afac_region_anual.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto", "tipo"] + [str(y) for y in YEARS] + ["nota_2026"])
        for code, name in AIRPORTS.items():
            for tipo in TIPOS:
                w.writerow([name, tipo]
                           + [annual(code, tipo, y) for y in YEARS]
                           + ["parcial ene-may"])

    # ---- 2) pico propio y variación (años completos 2019-2025) ----
    with open("output/afac_region_pico.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto", "tipo", "anio_pico", "valor_pico",
                    "valor_2025", "var_2025_vs_pico_pct",
                    "valor_2019", "var_2025_vs_2019_pct"])
        for code, name in AIRPORTS.items():
            for tipo in TIPOS:
                serie = {y: annual(code, tipo, y) for y in COMPLETE}
                peak_y = max(COMPLETE, key=lambda y: serie[y])
                peak_v = serie[peak_y]
                v25, v19 = serie[2025], serie[2019]
                w.writerow([name, tipo, peak_y, peak_v, v25,
                            f"{(v25/peak_v-1)*100:+.1f}" if peak_v else "n/a",
                            v19,
                            f"{(v25/v19-1)*100:+.1f}" if v19 else "n/a"])

    # ---- 3) 2026 vs 2025 YTD ene-may por tipo ----
    with open("output/afac_region_2026vs2025.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto", "tipo", "ytd_ene_may_2025",
                    "ytd_ene_may_2026", "var_pct"])
        for code, name in AIRPORTS.items():
            for tipo in TIPOS:
                a, b = ytd(code, tipo, 2025), ytd(code, tipo, 2026)
                w.writerow([name, tipo, a, b,
                            f"{(b/a-1)*100:+.1f}" if a else "n/a"])

    # ---- 4) validación AFAC vs ASUR (Cancún y Cozumel) por tipo ----
    #   ASUR tidy trae columnas nacional/internacional/total por (anio,mes).
    asur = {}   # (code_asur, tipo, anio, mes) -> pax
    ASUR_MAP = {"CUN": "CANCUN", "CZM": "COZUMEL"}
    try:
        for r in csv.DictReader(open("output/asur_pax_tidy.csv")):
            code = r["aeropuerto"]
            if code not in ASUR_MAP: continue
            y, m = int(r["anio"]), int(r["mes"])
            asur[(code, "nacional", y, m)] = int(r["nacional"])
            asur[(code, "internacional", y, m)] = int(r["internacional"])
            asur[(code, "total", y, m)] = int(r["total"])
    except FileNotFoundError:
        asur = {}

    def asur_sum(code, tipo, year, months):
        vals = [asur.get((code, tipo, year, m)) for m in months]
        if any(v is None for v in vals): return None
        return sum(vals)

    with open("output/afac_region_validacion.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto", "tipo", "periodo", "afac", "asur", "dif_pct"])
        for asur_code, afac_code in ASUR_MAP.items():
            for tipo in TIPOS:
                for y in COMPLETE:
                    af = annual(afac_code, tipo, y)
                    asu = asur_sum(asur_code, tipo, y, range(1, 13))
                    if asu:
                        w.writerow([AIRPORTS[afac_code], tipo, str(y), af, asu,
                                    f"{(af/asu-1)*100:+.3f}"])
                # YTD ene-may 2026 y 2025
                for y in (2025, 2026):
                    af = ytd(afac_code, tipo, y)
                    asu = asur_sum(asur_code, tipo, y, YTD_MONTHS)
                    if asu:
                        w.writerow([AIRPORTS[afac_code], tipo,
                                    f"{y} ene-may", af, asu,
                                    f"{(af/asu-1)*100:+.3f}"])

    # ================= consola =================
    print("== SERIE ANUAL DE PASAJEROS (AFAC) ==  [2026 = parcial ene-may]")
    hdr = f"{'aeropuerto':<10}{'tipo':<15}" + "".join(f"{y:>12}" for y in YEARS)
    print(hdr); print("-" * len(hdr))
    for code, name in AIRPORTS.items():
        for tipo in TIPOS:
            print(f"{name:<10}{tipo:<15}"
                  + "".join(f"{annual(code,tipo,y):>12,}" for y in YEARS))
        print()

    print("== PICO PROPIO Y VARIACIÓN (años completos 2019-2025) ==")
    print(f"{'aeropuerto':<10}{'tipo':<15}{'pico':>6}{'valor_pico':>13}"
          f"{'2025':>13}{'25 vs pico':>12}{'25 vs 19':>11}")
    for code, name in AIRPORTS.items():
        for tipo in TIPOS:
            serie = {y: annual(code, tipo, y) for y in COMPLETE}
            py = max(COMPLETE, key=lambda y: serie[y]); pv = serie[py]
            v25, v19 = serie[2025], serie[2019]
            vp = f"{(v25/pv-1)*100:+.1f}%" if pv else "n/a"
            v9 = f"{(v25/v19-1)*100:+.1f}%" if v19 else "n/a"
            print(f"{name:<10}{tipo:<15}{py:>6}{pv:>13,}{v25:>13,}{vp:>12}{v9:>11}")
    print()

    print("== 2026 vs 2025, YTD ene-may (comparable) ==")
    print(f"{'aeropuerto':<10}{'tipo':<15}{'2025':>13}{'2026':>13}{'var':>10}")
    for code, name in AIRPORTS.items():
        for tipo in TIPOS:
            a, b = ytd(code, tipo, 2025), ytd(code, tipo, 2026)
            vr = f"{(b/a-1)*100:+.1f}%" if a else "n/a"
            print(f"{name:<10}{tipo:<15}{a:>13,}{b:>13,}{vr:>10}")
    print()

    print("== VALIDACIÓN AFAC vs ASUR (dif = AFAC/ASUR-1) ==")
    print("   Chetumal no está en ASUR (aeropuerto ASA): sin cruce.")
    print(f"{'aeropuerto':<10}{'tipo':<15}{'periodo':>12}{'afac':>13}{'asur':>13}{'dif':>10}")
    for asur_code, afac_code in ASUR_MAP.items():
        for tipo in TIPOS:
            for y in COMPLETE:
                af = annual(afac_code, tipo, y)
                asu = asur_sum(asur_code, tipo, y, range(1, 13))
                if asu:
                    print(f"{AIRPORTS[afac_code]:<10}{tipo:<15}{str(y):>12}"
                          f"{af:>13,}{asu:>13,}{(af/asu-1)*100:>+9.3f}%")
            for y in (2025, 2026):
                af = ytd(afac_code, tipo, y)
                asu = asur_sum(asur_code, tipo, y, YTD_MONTHS)
                if asu:
                    print(f"{AIRPORTS[afac_code]:<10}{tipo:<15}"
                          f"{str(y)+' e-may':>12}{af:>13,}{asu:>13,}"
                          f"{(af/asu-1)*100:>+9.3f}%")
        print()


if __name__ == "__main__":
    main()
