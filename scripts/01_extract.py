#!/usr/bin/env python3
"""Extrae la serie mensual de pasajeros de ASUR (Cancun y Cozumel) del workbook
oficial, con parseo bloque-por-bloque y validacion de integridad.

El workbook trae una region corrupta en la zona 2006-2008 (bloques duplicados y
etiquetas de anio desalineadas). El parseo por bloques delimitados por
"AÑO ... Total AÑO" mas la verificacion suma_mensual == Total aisla esa basura:
cada bloque que no cuadra se marca INVALIDO y no entra al CSV limpio.

Fuente: asur.com.mx > Inversionistas > Trafico de pasajeros (workbook .xlsx).
Salida: CSV tidy aeropuerto, anio, mes, nacional, internacional, total."""
import openpyxl, csv

WB = "data/Trafico_de_pasajeros_ASUR.xlsx"
SHEETS = {"CUN": "PAX CUN", "CZM": "PAX CZM"}
MONTHS = {"ene":1,"feb":2,"mar":3,"abr":4,"may":5,"jun":6,
          "jul":7,"ago":8,"sep":9,"oct":10,"nov":11,"dic":12}

def month_num(s):
    if not s: return None
    return MONTHS.get(str(s).strip().lower()[:3])

def to_int(v):
    if v is None: return None
    if isinstance(v,(int,float)): return int(round(v))
    s=str(v).replace(",","").replace(" ","").strip()
    if s in ("","-"): return None
    try: return int(round(float(s)))
    except ValueError: return None

def parse_sheet(ws):
    """Devuelve (rows_validos, informe_bloques). Un bloque = anio.
    rows_validos solo de bloques cuya suma mensual cuadra con Total AÑO."""
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    blocks = []          # (anio, [months], total_reportado, row_ini)
    cur = None
    for i,row in enumerate(rows):
        b,c,d,e,f = row[1],row[2],row[3],row[4],row[5]
        bs = str(b).strip() if b is not None else ""
        if bs.isdigit() and len(bs)==4:                 # etiqueta de AÑO
            if cur: blocks.append(cur)
            cur = {"anio":int(bs),"months":[],"total":None,"row":i}
            m = month_num(c)                            # la fila AÑO trae enero
            if m and cur:
                cur["months"].append((m,to_int(d),to_int(e),to_int(f)))
            continue
        if bs.lower().startswith("total"):              # cierra bloque
            if cur:
                cur["total"] = to_int(f)
                blocks.append(cur); cur=None
            continue
        m = month_num(c)
        if m and cur is not None:
            cur["months"].append((m,to_int(d),to_int(e),to_int(f)))
    if cur: blocks.append(cur)

    valid, report = [], []
    seen_years = set()
    for blk in blocks:
        yr = blk["anio"]
        mm = [x for x in blk["months"] if x[3] is not None]  # meses con total
        suma = sum(x[3] for x in mm)
        rep  = blk["total"]
        ok = (rep is not None and suma == rep and len(set(x[0] for x in mm))==len(mm))
        dup = yr in seen_years
        status = "OK" if (ok and not dup) else ("DUP" if dup else "MISMATCH")
        report.append((yr, len(mm), suma, rep, status, blk["row"]))
        if ok and not dup:
            seen_years.add(yr)
            for (m,nac,intl,tot) in mm:
                valid.append({"anio":yr,"mes":m,"nacional":nac,
                              "internacional":intl,"total":tot})
    return valid, report

def main():
    wb = openpyxl.load_workbook(WB, read_only=True, data_only=True)
    allout=[]
    for code,sheet in SHEETS.items():
        valid, report = parse_sheet(wb[sheet])
        print(f"\n===== {code} =====")
        for yr,n,suma,rep,st,r in report:
            flag = "" if st=="OK" else f"  <<< {st}"
            print(f"  {yr}: {n:2d} meses  suma={suma:>10} total_rep={str(rep):>10}  [{st}]{flag}")
        for r in valid:
            allout.append({"aeropuerto":code,**r})
    allout.sort(key=lambda r:(r["aeropuerto"],r["anio"],r["mes"]))
    cols=["aeropuerto","anio","mes","nacional","internacional","total"]
    with open("output/asur_pax_tidy.csv","w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=cols); w.writeheader()
        for r in allout: w.writerow(r)
    out19=[r for r in allout if r["anio"]>=2019]
    with open("output/asur_pax_2019plus.csv","w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=cols); w.writeheader()
        for r in out19: w.writerow(r)
    print(f"\nCSV tidy: {len(allout)} filas | 2019+: {len(out19)} filas")

if __name__=="__main__":
    main()
