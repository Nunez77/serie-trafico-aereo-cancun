#!/usr/bin/env python3
"""Grafico de la serie de pasajeros del Aeropuerto de Cancun (ASUR),
ene 2019 - jun 2026. Paleta Pulse: navy #0A1628 base, cian #36C6D3 de acento.

Hallazgo central: el maximo ANUAL fue 2023 (32.75 M) y el trafico lleva dos anios
consecutivos a la baja (2024 -7.1%, 2025 -3.5%), con 2026 camino al tercero.
El grafico lo cuenta con una escalera del promedio mensual por anio (sand) sobre
el mismo eje que la serie mensual (cian), evitando el doble eje.

Se conservan la linea base 2019 (punteada) y la banda del cierre 2020.
No confundir el pico ANUAL (2023) con el pico MENSUAL (mar 2024, 3.07 M): ambos
van etiquetados por separado.
Salida: PNG 800px, PNG 1600px y SVG."""
import csv, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

# --- paleta Pulse ---
INK="#0A1628"; PANEL="#0C1D34"; PULSE="#36C6D3"; SAND="#E0AE4E"
MUTE="#9FB0C6"; SOFT="#5C6B80"; LINE="#1B2A44"; RED="#D97A6C"

def contrast(a,b):
    def lum(h):
        h=h.lstrip("#"); rgb=[int(h[i:i+2],16)/255 for i in (0,2,4)]
        rgb=[c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4 for c in rgb]
        return 0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2]
    L1,L2=sorted([lum(a),lum(b)],reverse=True)
    return (L1+0.05)/(L2+0.05)

def load():
    rows=[r for r in csv.DictReader(open("output/asur_pax_tidy.csv")) if r["aeropuerto"]=="CUN"]
    data={(int(r["anio"]),int(r["mes"])):int(r["total"]) for r in rows}
    xs,ys=[],[]
    for y in range(2019,2027):
        for m in range(1,13):
            if (y,m) in data:
                xs.append(dt.date(y,m,15)); ys.append(data[(y,m)]/1e6)
    # totales y promedios mensuales por anio (solo anios COMPLETOS: 2019-2025)
    annual={}
    for y in range(2019,2026):
        tot=sum(data[(y,m)] for m in range(1,13))
        annual[y]={"total":tot,"avg":tot/12/1e6}
    base2019=annual[2019]["avg"]
    peak=max(((y,m) for (y,m) in data if y>=2019), key=lambda k:data[k])
    floor=min(((y,m) for (y,m) in data if y>=2019), key=lambda k:data[k])
    return xs,ys,base2019,annual,(dt.date(*peak,15),data[peak]/1e6),(dt.date(*floor,15),data[floor]/1e6)

def build(xs,ys,base2019,annual,peak,floor):
    fig,ax=plt.subplots(figsize=(10,5.4))
    fig.patch.set_facecolor(INK); ax.set_facecolor(INK)

    # sombra suave del tramo de descenso 2023 -> 2026
    ax.axvspan(dt.date(2023,1,1),dt.date(2026,6,30),color=SAND,alpha=0.055,zorder=0)

    # hueco 2020: banda del cierre
    ax.axvspan(dt.date(2020,3,1),dt.date(2020,8,31),color="#12233d",zorder=0)
    ax.annotate("Cierre 2020",xy=(dt.date(2020,5,20),0.70),
                color=MUTE,fontsize=8.5,ha="center",va="bottom")

    # linea base 2019
    ax.axhline(base2019,color=SOFT,lw=1,ls=(0,(5,4)),zorder=1)
    ax.annotate(f"Base 2019 · {base2019:.2f} M/mes",
                xy=(dt.date(2019,3,1),base2019),xytext=(0,5),textcoords="offset points",
                color=MUTE,fontsize=8,ha="left",va="bottom")

    # serie mensual (hero)
    ax.plot(xs,ys,color=PULSE,lw=1.9,zorder=3,solid_capstyle="round")

    # escalera del promedio mensual por anio (narrativa anual)
    stroke=[pe.withStroke(linewidth=3.4,foreground=INK)]
    for y,d in annual.items():
        ax.hlines(d["avg"],dt.date(y,1,12),dt.date(y,12,20),
                  color=SAND,lw=2.6,zorder=4,path_effects=stroke,
                  capstyle="round")
    # variaciones anuales en cada escalon de bajada
    def dpct(a,b): return (annual[a]["total"]/annual[b]["total"]-1)*100
    for (yv,ylab) in [(2024,"−7.1%"),(2025,"−3.5%")]:
        ax.annotate(f"{dpct(yv,yv-1):+.1f}%".replace("+","").replace("-","−"),
                    xy=(dt.date(yv,7,1),annual[yv]["avg"]),xytext=(0,-13),
                    textcoords="offset points",color=RED,fontsize=8.5,ha="center",
                    va="top",fontweight="bold")

    # marca del PICO ANUAL 2023 (texto en area abierta arriba-izquierda, flecha al escalon)
    ax.annotate(f"Máximo anual: 2023 · {annual[2023]['total']/1e6:.2f} M pax",
                xy=(dt.date(2023,7,1),annual[2023]["avg"]),
                xytext=(dt.date(2021,3,1),3.48),textcoords="data",
                color=SAND,fontsize=9.5,ha="left",va="center",fontweight="bold",
                arrowprops=dict(arrowstyle="-",color=SAND,lw=1,alpha=0.6,shrinkA=2,shrinkB=6))

    # 2026 en curso: baja el tercer anio (acumulado ene-jun, con junio incluido)
    ax.annotate("2026 va al 3er año\n−4.7% a/a (ene–jun)",
                xy=(dt.date(2026,3,15),1.15),color=RED,fontsize=8,ha="center",
                va="top",fontweight="bold")

    # PICO MENSUAL (distinto del anual)
    dp,vp=peak
    ax.scatter([dp],[vp],s=26,color=PULSE,zorder=5,edgecolor=INK,linewidth=1.5)
    ax.annotate(f"Máx. mensual: mar 2024 ({vp:.2f} M)",xy=(dp,vp),
                xytext=(dt.date(2023,11,1),3.30),textcoords="data",
                color="#BFE0E5",fontsize=8,ha="left",va="center",
                arrowprops=dict(arrowstyle="-",color="#6F8197",lw=0.8,alpha=0.7,shrinkA=2,shrinkB=4))

    # piso
    df,vf=floor
    ax.scatter([df],[vf],s=26,color=MUTE,zorder=5,edgecolor=INK,linewidth=1.5)
    ax.annotate(f"Piso · {vf*1000:.0f} mil (may 2020)",xy=(df,vf),xytext=(30,30),
                textcoords="offset points",color=MUTE,fontsize=8,ha="left",va="bottom",
                arrowprops=dict(arrowstyle="-",color=SOFT,lw=0.8,shrinkA=0,shrinkB=3))

    # ultimo punto
    ax.scatter([xs[-1]],[ys[-1]],s=24,color=PULSE,zorder=5,edgecolor=INK,linewidth=1.5)
    ax.annotate(f"{ys[-1]:.2f} M",xy=(xs[-1],ys[-1]),xytext=(4,-2),textcoords="offset points",
                color=PULSE,fontsize=8,ha="left",va="top",fontweight="bold")

    # ejes
    ax.set_ylim(0,3.55); ax.set_xlim(dt.date(2018,10,1),dt.date(2026,10,1))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{v:.0f} M"))
    ax.set_yticks([0,1,2,3])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(colors=MUTE,labelsize=9,length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.spines["bottom"].set_visible(True); ax.spines["bottom"].set_color(LINE)
    ax.grid(axis="y",color=LINE,lw=0.8,zorder=0); ax.set_axisbelow(True)

    # leyenda (2 series -> identidad no depende solo del color)
    leg=[Line2D([0],[0],color=PULSE,lw=2,label="Pasajeros por mes"),
         Line2D([0],[0],color=SAND,lw=2.6,label="Promedio mensual del año")]
    lg=ax.legend(handles=leg,loc="lower right",bbox_to_anchor=(1.0,0.02),
                 frameon=False,fontsize=8.5,labelcolor=MUTE,handlelength=1.6,
                 borderpad=0.2,labelspacing=0.35)

    # titulo y fuente
    fig.text(0.062,0.955,"Aeropuerto de Cancún: el techo fue 2023",
             color="#FFFFFF",fontsize=15.5,fontweight="bold",ha="left",va="top")
    fig.text(0.062,0.905,"Pasajeros del Aeropuerto de Cancún (ASUR), ene 2019 – jun 2026",
             color=MUTE,fontsize=10,ha="left",va="top")
    fig.text(0.062,0.045,"Fuente: ASUR, Tráfico de pasajeros. Serie mensual; promedio = total anual ÷ 12. Cálculo y gráfico: Riviera Maya Economic Pulse.",
             color=SOFT,fontsize=7.6,ha="left",va="bottom")
    fig.subplots_adjust(left=0.062,right=0.972,top=0.83,bottom=0.10)
    return fig

def main():
    print(f"Contraste cian/navy: {contrast(PULSE,INK):.2f}:1 | sand/navy: {contrast(SAND,INK):.2f}:1")
    xs,ys,base2019,annual,peak,floor=load()
    for y,d in annual.items():
        print(f"  {y}: total {d['total']:>10,}  prom {d['avg']:.3f} M/mes")
    fig=build(xs,ys,base2019,annual,peak,floor)
    fig.savefig("output/trafico_cancun_1600.png",dpi=160,facecolor=INK)
    fig.savefig("output/trafico_cancun_800.png",dpi=80,facecolor=INK)
    fig.savefig("output/trafico_cancun.svg",facecolor=INK)
    print("PNG 1600/800 + SVG escritos en output/")

if __name__=="__main__":
    main()
