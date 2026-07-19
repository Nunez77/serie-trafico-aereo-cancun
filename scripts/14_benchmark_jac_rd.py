#!/usr/bin/env python3
"""Benchmark Caribe: República Dominicana (JAC), acumulado ene-may 2026 vs 2025.

Fuente: Junta de Aviación Civil, "Reporte Histórico 2005 - jun. 2026", hoja
"5. Pasajeros por Aeropuertos". Archivado en data/benchmark/ con checksum.

UNIVERSO: pasajeros comerciales de ENTRADA MAS SALIDA por aeropuerto dominicano.
Es un conteo de movimiento de terminal, no de turistas. NO se suma ni se resta
con las llegadas de visitantes del Banco Central de RD (universo distinto), ni
con AFAC o ASUR de México (otra autoridad, otro país). Sirve para comparar
tendencias lado a lado, declarando siempre que son dos fuentes nacionales.

Validación incorporada: la suma de las filas de aeropuerto se contrasta contra
la fila "Total <año>" de la propia hoja. Si no cuadra, aborta.

Salida: output/benchmark_jac_rd_2026vs2025.csv
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
import sys

XLSX = "data/benchmark/Reporte-Historico-2005-jun.-2026.xlsx"
HOJA = "5. Pasajeros por Aeropuertos"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
T = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
MESES = range(1, 6)          # enero a mayo
ANIOS = ("2025", "2026")


def col_idx(ref):
    s = "".join(c for c in ref if c.isalpha())
    n = 0
    for c in s:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def leer_hoja():
    z = zipfile.ZipFile(XLSX)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    mapa = {r.get("Id"): r.get("Target") for r in rels}
    destino = next((mapa[s.get(R)] for s in wb.findall(".//m:sheet", NS)
                    if s.get("name") == HOJA), None)
    if not destino:
        sys.exit(f"FALLO: no existe la hoja {HOJA}")
    if not destino.startswith("xl/"):
        destino = "xl/" + destino.lstrip("/")

    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
        shared = ["".join(t.text or "" for t in si.iter(T)) for si in ss.findall("m:si", NS)]

    filas = []
    for row in ET.fromstring(z.read(destino)).findall(".//m:row", NS):
        celdas = {}
        for c in row.findall("m:c", NS):
            v = c.find("m:v", NS)
            if v is None or v.text is None:
                continue
            if c.get("t") == "s":
                val = shared[int(v.text)]
            elif c.get("t") == "inlineStr":
                val = "".join(t.text or "" for t in c.iter(T))
            else:
                val = v.text
            celdas[col_idx(c.get("r"))] = val
        if celdas:
            filas.append((int(row.get("r")), celdas))
    return filas


def bloques(filas):
    """{anio: fila_inicial} para las cabeceras de año buscadas."""
    out = {}
    for r, c in filas:
        vals = [str(x).strip() for x in c.values()]
        if len(vals) == 1 and vals[0] in ANIOS:
            out[vals[0]] = r
    return out


def leer_anio(filas, rini):
    """Devuelve ({aeropuerto: [12 meses]}, fila_total_de_la_hoja)."""
    aptos, actual, total_hoja = {}, None, None
    for r, c in filas:
        if r <= rini:
            continue
        etq = str(c.get(1, "")).strip()
        tipo = str(c.get(2, "")).strip()
        if etq.lower().startswith("total 20"):
            total_hoja = [c.get(i) for i in range(3, 15)]
            break
        if etq and etq.lower() != "aeropuertos":
            actual = etq
        if tipo == "Total" and actual:
            aptos[actual] = [c.get(i) for i in range(3, 15)]
    return aptos, total_hoja


def suma(serie, meses):
    return sum(int(float(serie[i - 1])) for i in meses
               if serie[i - 1] not in (None, ""))


if __name__ == "__main__":
    filas = leer_hoja()
    bl = bloques(filas)
    faltan = [a for a in ANIOS if a not in bl]
    if faltan:
        sys.exit(f"FALLO: no se encontraron los bloques {faltan}")

    datos, filas_total = {}, {}
    for a in ANIOS:
        datos[a], filas_total[a] = leer_anio(filas, bl[a])

    # validación: la suma de aeropuertos debe cuadrar con la fila Total de la hoja
    for a in ANIOS:
        mia = suma([str(sum(int(float(datos[a][k][i - 1] or 0)) for k in datos[a]))
                    for i in range(1, 13)], MESES)
        hoja = suma(filas_total[a], MESES)
        if mia != hoja:
            sys.exit(f"FALLO validación {a}: suma propia {mia:,} contra fila de la hoja {hoja:,}")
        print(f"validación {a} ene-may: {mia:,} cuadra con la fila Total de la hoja")

    filas_out = []
    for apt in sorted(set(datos["2025"]) | set(datos["2026"])):
        a = suma(datos["2025"].get(apt, [None] * 12), MESES)
        b = suma(datos["2026"].get(apt, [None] * 12), MESES)
        if a or b:
            var = round((b - a) / a * 100, 1) if a else ""
            filas_out.append([apt, a, b, var])
    ta = suma(filas_total["2025"], MESES)
    tb = suma(filas_total["2026"], MESES)
    filas_out.append(["TOTAL PAIS", ta, tb, round((tb - ta) / ta * 100, 1)])

    with open("output/benchmark_jac_rd_2026vs2025.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["aeropuerto", "pax_ene_may_2025", "pax_ene_may_2026", "var_pct"])
        w.writerows(filas_out)

    print()
    print(f'{"aeropuerto":<28}{"2025":>12}{"2026":>12}{"var":>9}')
    for r in filas_out:
        print(f"{r[0][:28]:<28}{r[1]:>12,}{r[2]:>12,}{str(r[3])+'%':>9}")
