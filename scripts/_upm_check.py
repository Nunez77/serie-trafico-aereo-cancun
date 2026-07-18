#!/usr/bin/env python3
"""Valida un .xls del Cuadro 1.3.1 de UPM y deriva su periodo (año, último mes).
Uso: python3 _upm_check.py <ruta.xls>
Imprime "OK <YYYY> <MM>" si es válido, o "INVALID <motivo>" si no.
El script de archivo (archive_upm_1.3.1.sh) usa esta salida para nombrar sin
sobrescribir: c131_YYYY_MM.xls."""
import sys, re
try:
    import xlrd
except ImportError:
    print("INVALID falta_xlrd"); sys.exit(0)

MES={"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,"julio":7,
     "agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}

def main():
    if len(sys.argv)<2:
        print("INVALID sin_ruta"); return
    try:
        wb=xlrd.open_workbook(sys.argv[1]); sh=wb.sheet_by_index(0)
    except Exception as e:
        print(f"INVALID no_abre_{type(e).__name__}"); return
    if sh.nrows<100:
        print(f"INVALID pocas_filas_{sh.nrows}"); return
    # título en las primeras filas
    title=""
    for r in range(min(4,sh.nrows)):
        for c in range(min(4,sh.ncols)):
            v=str(sh.cell_value(r,c))
            if "1.3.1" in v and "ntradas" in v: title=v
    if not title:
        print("INVALID sin_titulo_1.3.1"); return
    # validar que la hoja trae la columna Cancún (estructura esperada)
    has_cun=False
    for r in range(min(7,sh.nrows)):
        if any("ancún" in str(sh.cell_value(r,c)) or "ancun" in str(sh.cell_value(r,c))
               for c in range(sh.ncols)):
            has_cun=True; break
    if not has_cun:
        print("INVALID sin_columna_cancun"); return
    m=re.search(r"enero\s*[-a]\s*([a-záéíóú]+)\s+de\s+(\d{4})", title.lower())
    if not m:
        print(f"INVALID periodo_no_parseado"); return
    mes=MES.get(m.group(1))
    if not mes:
        print(f"INVALID mes_desconocido_{m.group(1)}"); return
    print(f"OK {m.group(2)} {mes:02d}")

if __name__=="__main__":
    main()
