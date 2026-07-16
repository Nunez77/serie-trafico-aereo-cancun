#!/usr/bin/env python3
"""Reporte analitico y verificacion cruzada de la serie ASUR (Cancun).
Verificacion obligatoria contra la edicion de junio 2026 del Pulse:
  - 12.64 M pasajeros ene-may 2026
  - -3.4% a/a (ene-may 2026 vs ene-may 2025)
  - +14.6% vs 2019 (ene-may 2026 vs ene-may 2019)
Si no cuadra, se imprime STOP."""
import csv

MES = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

def load(code):
    d={}
    for r in csv.DictReader(open("output/asur_pax_tidy.csv")):
        if r["aeropuerto"]!=code: continue
        d[(int(r["anio"]),int(r["mes"]))]={
            "nac":int(r["nacional"]),"int":int(r["internacional"]),"tot":int(r["total"])}
    return d

def pct(new,old): return (new/old-1)*100

def main():
    cun=load("CUN")
    keys=sorted(cun)
    print("="*66)
    print("(a) RANGO DISPONIBLE (Cancun)")
    print(f"    {MES[keys[0][1]]} {keys[0][0]}  ->  {MES[keys[-1][1]]} {keys[-1][0]}")
    print(f"    ultimo mes con dato: {MES[keys[-1][1]]} {keys[-1][0]}")

    print("\n"+"="*66)
    print("(b) TOTALES ANUALES  (total | nacional | internacional)")
    for y in range(2019,2027):
        ms=[cun[(y,m)] for m in range(1,13) if (y,m) in cun]
        t=sum(x["tot"] for x in ms); n=sum(x["nac"] for x in ms); i=sum(x["int"] for x in ms)
        etq="(parcial ene-jun)" if y==2026 else ""
        print(f"    {y}: {t:>10,}  | nac {n:>9,} | int {i:>9,}   {etq}")

    print("\n"+"="*66)
    print("(c) 2026 VARIACION INTERANUAL POR MES (2026 vs 2025)")
    for m in range(1,13):
        if (2026,m) not in cun: break
        a=cun[(2026,m)]["tot"]; b=cun[(2025,m)]["tot"]
        print(f"    {MES[m]}: {a:>9,} vs {b:>9,}  ->  {pct(a,b):+6.1f}%")

    print("\n"+"="*66)
    print("(d) 2026 CADA MES vs SU EQUIVALENTE DE 2019")
    for m in range(1,13):
        if (2026,m) not in cun: break
        a=cun[(2026,m)]["tot"]; b=cun[(2019,m)]["tot"]
        print(f"    {MES[m]}: {a:>9,} vs {b:>9,}  ->  {pct(a,b):+6.1f}%")

    print("\n"+"="*66)
    print("(e) PICO Y PISO HISTORICOS (toda la serie limpia, Cancun)")
    pico=max(cun,key=lambda k:cun[k]["tot"])
    piso=min(cun,key=lambda k:cun[k]["tot"])
    print(f"    PICO: {MES[pico[1]]} {pico[0]} = {cun[pico]['tot']:,}")
    print(f"    PISO: {MES[piso[1]]} {piso[0]} = {cun[piso]['tot']:,}")

    print("\n"+"#"*66)
    print("VERIFICACION CRUZADA vs edicion junio 2026 del Pulse")
    print("#"*66)
    ene_may=lambda y: sum(cun[(y,m)]["tot"] for m in range(1,6))
    v2026=ene_may(2026); v2025=ene_may(2025); v2019=ene_may(2019)
    yoy=pct(v2026,v2025); vs19=pct(v2026,v2019)
    print(f"  ene-may 2026 (nuestro dato): {v2026:,}  ({v2026/1e6:.2f} M)")
    print(f"     publicado: 12.64 M                -> {'CUADRA' if abs(v2026/1e6-12.64)<0.02 else 'NO CUADRA'}")
    print(f"  a/a ene-may 2026 vs 2025: {yoy:+.1f}%")
    print(f"     publicado: -3.4%                  -> {'CUADRA' if abs(yoy-(-3.4))<0.15 else 'NO CUADRA'}")
    print(f"  vs 2019 ene-may: {vs19:+.1f}%")
    print(f"     publicado: +14.6%                 -> {'CUADRA' if abs(vs19-14.6)<0.15 else 'NO CUADRA'}")
    ok = abs(v2026/1e6-12.64)<0.02 and abs(yoy-(-3.4))<0.15 and abs(vs19-14.6)<0.15
    print("\n  RESULTADO:", "TODO CUADRA — extraccion validada." if ok else "!!! STOP: NO CUADRA, revisar antes de seguir.")

if __name__=="__main__":
    main()
