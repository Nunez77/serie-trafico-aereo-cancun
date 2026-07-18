#!/usr/bin/env python3
"""¿Cae Cancún o cae México? Compara la serie anual de PASAJEROS de Cancún
contra los demás destinos de playa (Los Cabos, Puerto Vallarta, Mazatlán,
Huatulco, Acapulco) y contra el TOTAL NACIONAL (suma de los 68 aeropuertos),
2019-2026, a partir del pivot-cache del Excel oficial de AFAC.

Salida (solo datos):
  output/afac_playa_anual.csv      totales anuales por aeropuerto + nacional
  output/afac_playa_pico.csv       año pico, valor pico, variación desde el pico
  output/afac_playa_2026vs2025.csv YTD ene-may 2026 vs ene-may 2025 (comparable)

Nota: 2026 en AFAC llega a MAYO (ene-may). Los totales anuales 2026 son
parciales; el 2026-vs-2025 se hace YTD sobre meses comunes (ene-may).

Fuente: AFAC, Estadística Operativa de Aeropuertos (gob.mx/afac)."""
import zipfile, xml.etree.ElementTree as ET, csv, collections

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

# etiqueta AFAC -> nombre de reporte
PLAYA = {
    "CANCUN": "Cancún",
    "SAN JOSE DEL CABO": "Los Cabos",
    "PUERTO VALLARTA": "Puerto Vallarta",
    "MAZATLAN": "Mazatlán",
    "HUATULCO": "Huatulco",
    "ACAPULCO": "Acapulco",
}
YTD_MONTHS = range(1, 6)   # ene-may (último mes disponible en 2026)

def load():
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

def main():
    SH, rec = load()
    OPC, YR, APT = SH[0], SH[2], SH[4]
    pax = OPC.index("PASAJEROS/PASSENGERS")

    # (apto, anio, mes) -> pasajeros totales ; y NACIONAL (suma de todos los aptos)
    mmes = collections.defaultdict(int)     # (apto,anio,mes)
    nac_mes = collections.defaultdict(int)  # (anio,mes) total nacional
    for r in rec.findall("m:r",NS):
        cs = [cellval(c) for c in list(r)]
        if cs[0]!=pax: continue
        apto = APT[cs[4]]; year = int(YR[cs[2]])
        for mi in range(12):
            v = cs[5+mi]
            if v:
                mmes[(apto,year,mi+1)] += int(v)
                nac_mes[(year,mi+1)] += int(v)

    years = list(range(2019, 2027))

    def annual(apto):   # None => nacional
        out = {}
        for y in years:
            if apto is None:
                out[y] = sum(nac_mes[(y,m)] for m in range(1,13))
            else:
                out[y] = sum(mmes[(apto,y,m)] for m in range(1,13))
        return out

    labels = list(PLAYA.values()) + ["TOTAL NACIONAL"]
    aptos  = list(PLAYA.keys()) + [None]
    ann = {lab: annual(ap) for lab,ap in zip(labels, aptos)}

    # ---- 1) totales anuales ----
    with open("output/afac_playa_anual.csv","w",newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto"]+[str(y) for y in years]+["nota_2026"])
        for lab in labels:
            w.writerow([lab]+[ann[lab][y] for y in years]+["parcial ene-may"])

    # ---- 2) pico y variación desde el pico (años COMPLETOS 2019-2025) ----
    complete = [y for y in years if y != 2026]
    with open("output/afac_playa_pico.csv","w",newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto","anio_pico","valor_pico",
                    "valor_2025","var_2025_vs_pico_pct","valor_2019","var_2025_vs_2019_pct"])
        for lab in labels:
            peak_y = max(complete, key=lambda y: ann[lab][y])
            peak_v = ann[lab][peak_y]
            v25 = ann[lab][2025]; v19 = ann[lab][2019]
            w.writerow([lab, peak_y, peak_v, v25,
                        f"{(v25/peak_v-1)*100:+.1f}", v19, f"{(v25/v19-1)*100:+.1f}"])

    # ---- 3) 2026 vs 2025 YTD (ene-may) ----
    def ytd(apto, y):
        if apto is None:
            return sum(nac_mes[(y,m)] for m in YTD_MONTHS)
        return sum(mmes[(apto,y,m)] for m in YTD_MONTHS)
    with open("output/afac_playa_2026vs2025.csv","w",newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aeropuerto","ytd_ene_may_2025","ytd_ene_may_2026","var_pct"])
        for lab,ap in zip(labels, aptos):
            a = ytd(ap,2025); b = ytd(ap,2026)
            w.writerow([lab, a, b, f"{(b/a-1)*100:+.1f}"])

    # ---- consola: mesas legibles ----
    def fmt(n): return f"{n:,}"
    print("== TOTALES ANUALES DE PASAJEROS (AFAC) ==  [2026 = parcial ene-may]")
    hdr = f"{'aeropuerto':<16}" + "".join(f"{y:>13}" for y in years)
    print(hdr); print("-"*len(hdr))
    for lab in labels:
        print(f"{lab:<16}" + "".join(f"{ann[lab][y]:>13,}" for y in years))

    print("\n== PICO PROPIO Y VARIACIÓN (años completos 2019-2025) ==")
    print(f"{'aeropuerto':<16}{'pico':>6}{'valor_pico':>15}{'2025':>15}{'2025 vs pico':>14}{'2025 vs 2019':>14}")
    for lab in labels:
        peak_y = max(complete, key=lambda y: ann[lab][y]); peak_v = ann[lab][peak_y]
        v25=ann[lab][2025]; v19=ann[lab][2019]
        print(f"{lab:<16}{peak_y:>6}{peak_v:>15,}{v25:>15,}{(v25/peak_v-1)*100:>+13.1f}%{(v25/v19-1)*100:>+13.1f}%")

    print("\n== 2026 vs 2025, YTD ene-may (comparable) ==")
    print(f"{'aeropuerto':<16}{'2025 ene-may':>15}{'2026 ene-may':>15}{'var':>10}")
    for lab,ap in zip(labels, aptos):
        a=ytd(ap,2025); b=ytd(ap,2026)
        print(f"{lab:<16}{a:>15,}{b:>15,}{(b/a-1)*100:>+9.1f}%")

    # ---- validación Cancún AFAC vs ASUR ----
    d = {}
    try:
        for r in csv.DictReader(open("output/asur_pax_tidy.csv")):
            if r["aeropuerto"]=="CUN": d[(int(r["anio"]),int(r["mes"]))]=int(r["total"])
        print("\n== VALIDACIÓN Cancún AFAC vs ASUR (total anual) ==")
        for y in (2019,2020,2021,2022,2023,2024,2025):
            afac = ann["Cancún"][y]
            asur = sum(d[(y,m)] for m in range(1,13) if (y,m) in d)
            if asur:
                print(f"  {y}: AFAC={afac:>12,}  ASUR={asur:>12,}  dif={(afac/asur-1)*100:+.3f}%")
        # YTD 2026 ene-may
        afac26 = ytd("CANCUN",2026)
        asur26 = sum(d[(2026,m)] for m in YTD_MONTHS if (2026,m) in d)
        if asur26:
            print(f"  2026 ene-may: AFAC={afac26:>12,}  ASUR={asur26:>12,}  dif={(afac26/asur26-1)*100:+.3f}%")
    except FileNotFoundError:
        print("\n(asur_pax_tidy.csv no encontrado; corre 01_extract.py para la validación)")

if __name__=="__main__":
    main()
