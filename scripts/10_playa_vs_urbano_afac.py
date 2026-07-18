#!/usr/bin/env python3
"""Clasifica los 68 aeropuertos AFAC en PLAYA (sol y playa / resort de ocio
costero) vs NO PLAYA (urbanos, capitales, negocios, fronterizos, industriales,
regionales y ciudades costeras cuyo tráfico es de negocios/gobierno/cultura).
Agrega cada grupo por tipo (nacional/internacional), ene-may 2026 vs 2025, en
absolutos y porcentaje. Imprime la lista completa por grupo para la nota
metodológica y aísla los casos dudosos.

CRITERIO (declarable): "PLAYA" = aeropuerto cuyo mercado dominante es el turismo
de ocio sol-y-playa (destino de resort costero). Una ciudad costera cuyo
aeropuerto sirve principalmente negocios/gobierno/cultura NO es playa (Mérida,
Veracruz, Tijuana, Campeche, Cd. del Carmen, Villahermosa...).

Fuente: AFAC. Pivot-cache ya extraído; NO se re-descarga.
Salida: output/afac_playa_vs_urbano_ytd.csv"""
import zipfile, xml.etree.ElementTree as ET, csv, collections

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]
YTD = range(1, 6)  # ene-may
TIPO_IDX = {0: "nac", 1: "intl"}

# --- clasificación: exactamente las etiquetas AFAC del pivot-cache ---
PLAYA = {
    "CANCUN", "COZUMEL", "HUATULCO", "ACAPULCO", "ZIHUATANEJO", "MANZANILLO",
    "LA PAZ", "PUERTO VALLARTA", "SAN JOSE DEL CABO", "LORETO",
    "PUERTO ESCONDIDO", "MAZATLAN", "TULÚM", "PUERTO PEÑASCO",
}
# dudosos que el usuario pidió marcar explícitamente -> mi criterio = NO PLAYA
DUDOSOS = {
    "MERIDA": "urbano/cultural, capital de Yucatán; tráfico de negocios y ciudad, no resort -> NO PLAYA",
    "TIJUANA": "fronterizo/urbano, hub CBX a San Diego; no es destino de ocio de playa -> NO PLAYA",
    "VILLAHERMOSA": "urbano/petrolero (Tabasco); sin componente de resort -> NO PLAYA",
    # dudosos propios que agrego por transparencia (quedan en PLAYA):
    "LA PAZ": "capital de BCS PERO tráfico dominado por turismo marino/playa -> PLAYA (frágil)",
    "MANZANILLO": "puerto de carga grande PERO pasaje es resort (Las Hadas) -> PLAYA (frágil)",
    "ACAPULCO": "playa clásica, deprimida por huracán Otis (oct-2023) -> PLAYA",
}


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
    OPC, YR, APT = SH[0], SH[2], SH[4]
    pax = OPC.index("PASAJEROS/PASSENGERS")
    allaptos = list(APT)

    # (apto, tipo, anio) -> pax YTD ene-may
    ytd = collections.defaultdict(int)
    for r in rec.findall("m:r", NS):
        cs = [cellval(c) for c in list(r)]
        if cs[0] != pax: continue
        apto = APT[cs[4]]; tipo = TIPO_IDX[cs[1]]; y = int(YR[cs[2]])
        if y not in (2025, 2026): continue
        for mi in YTD:
            v = cs[5 + (mi - 1)]
            if v: ytd[(apto, tipo, y)] += int(v)

    def grp(apto):  # None => usa PLAYA set
        return "PLAYA" if apto in PLAYA else "NO PLAYA"

    # agregados por grupo y tipo
    agg = collections.defaultdict(int)  # (grupo, tipo, anio)
    for apto in allaptos:
        g = grp(apto)
        for tipo in ("nac", "intl"):
            for y in (2025, 2026):
                agg[(g, tipo, y)] += ytd[(apto, tipo, y)]

    def line(g, tipo):
        a = agg[(g, tipo, 2025)]; b = agg[(g, tipo, 2026)]
        return a, b, b - a, (b / a - 1) * 100 if a else float("nan")

    # ---------- consola ----------
    print("== AGREGADO POR GRUPO — YTD ene-may 2026 vs 2025 ==")
    print(f"{'grupo':<10}{'tipo':<6}{'2025':>15}{'2026':>15}{'dif abs':>13}{'var %':>12}")
    for g in ("PLAYA", "NO PLAYA"):
        for tipo in ("nac", "intl"):
            a, b, d, v = line(g, tipo)
            print(f"{g:<10}{tipo:<6}{a:>15,}{b:>15,}{d:>+13,}{v:>+11.4f}%")
        # total del grupo
        a = agg[(g,'nac',2025)]+agg[(g,'intl',2025)]
        b = agg[(g,'nac',2026)]+agg[(g,'intl',2026)]
        print(f"{g:<10}{'TOT':<6}{a:>15,}{b:>15,}{b-a:>+13,}{(b/a-1)*100:>+11.4f}%")
        print()

    # nacional de control (suma de ambos grupos, nac)
    na = agg[('PLAYA','nac',2025)]+agg[('NO PLAYA','nac',2025)]
    nb = agg[('PLAYA','nac',2026)]+agg[('NO PLAYA','nac',2026)]
    ia = agg[('PLAYA','intl',2025)]+agg[('NO PLAYA','intl',2025)]
    ib = agg[('PLAYA','intl',2026)]+agg[('NO PLAYA','intl',2026)]
    print("== CONTROL: suma de los dos grupos = TOTAL NACIONAL 68 aptos ==")
    print(f"  nac  2025={na:,}  2026={nb:,}  dif={nb-na:+,}  ({(nb/na-1)*100:+.4f}%)")
    print(f"  intl 2025={ia:,}  2026={ib:,}  dif={ib-ia:+,}  ({(ib/ia-1)*100:+.4f}%)")

    # ---------- dudosos aislados ----------
    print("\n== CASOS DUDOSOS (contribución individual, nac ene-may) ==")
    print("   Para mover un aeropuerto de grupo, réstalo/súmalo aquí.")
    for apto in sorted(DUDOSOS):
        if apto not in allaptos: continue
        a = ytd[(apto,'nac',2025)]; b = ytd[(apto,'nac',2026)]
        ai= ytd[(apto,'intl',2025)]; bi= ytd[(apto,'intl',2026)]
        print(f"  {apto:<18} [{grp(apto)}] nac {a:>9,}->{b:>9,} ({b-a:+,})"
              f" | intl {ai:>9,}->{bi:>9,} ({bi-ai:+,})")
        print(f"      criterio: {DUDOSOS[apto]}")

    # ---------- listas completas ----------
    playa = sorted([a for a in allaptos if grp(a)=="PLAYA"])
    noplaya = sorted([a for a in allaptos if grp(a)=="NO PLAYA"])
    print(f"\n== LISTA GRUPO PLAYA ({len(playa)}) ==")
    print("  " + ", ".join(playa))
    print(f"\n== LISTA GRUPO NO PLAYA ({len(noplaya)}) ==")
    print("  " + ", ".join(noplaya))

    # ---------- CSV ----------
    with open("output/afac_playa_vs_urbano_ytd.csv","w",newline="") as fh:
        w=csv.writer(fh)
        w.writerow(["grupo","tipo","ytd_2025","ytd_2026","dif_abs","var_pct"])
        for g in ("PLAYA","NO PLAYA"):
            for tipo in ("nac","intl"):
                a,b,d,v=line(g,tipo)
                w.writerow([g,tipo,a,b,d,f"{v:+.4f}"])
            a=agg[(g,'nac',2025)]+agg[(g,'intl',2025)]
            b=agg[(g,'nac',2026)]+agg[(g,'intl',2026)]
            w.writerow([g,"total",a,b,b-a,f"{(b/a-1)*100:+.4f}"])
        w.writerow([])
        w.writerow(["aeropuerto","grupo","nac_2025","nac_2026","intl_2025","intl_2026"])
        for apto in sorted(allaptos):
            w.writerow([apto, grp(apto),
                        ytd[(apto,'nac',2025)], ytd[(apto,'nac',2026)],
                        ytd[(apto,'intl',2025)], ytd[(apto,'intl',2026)]])


if __name__ == "__main__":
    main()
