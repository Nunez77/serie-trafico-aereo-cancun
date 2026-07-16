#!/usr/bin/env python3
"""Small-multiple Cancún vs Tulum, a la MISMA escala (paneles apilados, eje Y
compartido 0-3.5 M). La escala compartida es el punto: muestra el tamaño real de
Tulum (~4% del tráfico regional), sin la distorsión que produciría indexar a base
100 o darle un eje propio. Doble eje: prohibido.

Cancún: ASUR (serie del operador). Tulum: AFAC (regulador). Dos fuentes oficiales
distintas; en Cancún, donde se traslapan, difieren ~0.5% en 2024-2025.
Salida: PNG 800/1600 + SVG."""
import csv, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

INK="#0A1628"; PULSE="#36C6D3"; MUTE="#9FB0C6"; SOFT="#5C6B80"; LINE="#1B2A44"

def load(f,code):
    d={}
    for r in csv.DictReader(open(f)):
        if r["aeropuerto"]==code: d[(int(r["anio"]),int(r["mes"]))]=int(r[ "total"])
    xs=[dt.date(y,m,15) for (y,m) in sorted(d)]
    ys=[d[(y,m)]/1e6 for (y,m) in sorted(d)]
    return xs,ys

def panel(ax,xs,ys,fill=False):
    if fill:
        ax.fill_between(xs,ys,0,color=PULSE,alpha=0.16,zorder=2)
    ax.plot(xs,ys,color=PULSE,lw=1.9,zorder=3,solid_capstyle="round")
    ax.set_ylim(0,3.5); ax.set_yticks([0,1,2,3])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{v:.0f} M"))
    ax.set_facecolor(INK)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=MUTE,labelsize=9,length=0)
    ax.grid(axis="y",color=LINE,lw=0.8,zorder=0); ax.set_axisbelow(True)

def main():
    cx,cy=load("output/asur_pax_tidy.csv","CUN")
    tx,ty=load("output/afac_tulum_tidy.csv","TQO")
    # recortar Cancun a 2019+ para emparejar la ventana
    cx2=[d for d in cx if d.year>=2019]; cy2=cy[len(cy)-len(cx2):]

    fig,(a1,a2)=plt.subplots(2,1,sharex=True,sharey=True,figsize=(10,6.6))
    fig.patch.set_facecolor(INK)
    panel(a1,cx2,cy2)
    panel(a2,tx,ty,fill=True)

    a1.set_xlim(dt.date(2018,10,1),dt.date(2026,10,1))
    a2.xaxis.set_major_locator(mdates.YearLocator())
    a2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # rotulos por panel
    a1.text(0.012,0.90,"Cancún (ASUR)",transform=a1.transAxes,color="#FFFFFF",
            fontsize=12,fontweight="bold",va="top")
    a1.text(0.012,0.72,"≈ 29 M pasajeros en 2025",transform=a1.transAxes,
            color=MUTE,fontsize=9,va="top")
    a2.text(0.012,0.90,"Tulum (AFAC)",transform=a2.transAxes,color="#FFFFFF",
            fontsize=12,fontweight="bold",va="top")
    a2.text(0.012,0.72,"Abrió dic 2023 · ≈ 1.2 M/año · 4% del tráfico regional",
            transform=a2.transAxes,color=MUTE,fontsize=9,va="top")
    a2.annotate("misma escala que arriba ↑",xy=(dt.date(2021,6,1),1.1),
                color=SOFT,fontsize=8.5,style="italic",ha="center")
    # ancla de dato en la astilla de Tulum (su pico mensual)
    tpk=max(range(len(ty)),key=lambda i:ty[i])
    a2.annotate(f"pico {ty[tpk]*1000:.0f} mil · dic 2024",xy=(tx[tpk],ty[tpk]),
                xytext=(0,26),textcoords="offset points",color=MUTE,fontsize=8,
                ha="center",va="bottom",
                arrowprops=dict(arrowstyle="-",color=SOFT,lw=0.8,shrinkA=1,shrinkB=2))

    # titulo y fuente
    fig.text(0.062,0.965,"Cancún y Tulum, a la misma escala",color="#FFFFFF",
             fontsize=15.5,fontweight="bold",ha="left",va="top")
    fig.text(0.062,0.928,"Pasajeros por mes. La escala compartida muestra el tamaño real de Tulum frente a Cancún.",
             color=MUTE,fontsize=10,ha="left",va="top")
    fig.text(0.062,0.028,"Cancún: ASUR. Tulum: AFAC (Estadística Operativa de Aeropuertos). Dos fuentes oficiales; en Cancún, donde se traslapan, difieren ~0.5% (2024–2025). Gráfico: Riviera Maya Economic Pulse.",
             color=SOFT,fontsize=7.4,ha="left",va="bottom")
    fig.subplots_adjust(left=0.062,right=0.972,top=0.885,bottom=0.075,hspace=0.14)

    fig.savefig("output/panel_cancun_tulum_1600.png",dpi=160,facecolor=INK)
    fig.savefig("output/panel_cancun_tulum_800.png",dpi=80,facecolor=INK)
    fig.savefig("output/panel_cancun_tulum.svg",facecolor=INK)
    print("panel_cancun_tulum PNG 1600/800 + SVG escritos")

if __name__=="__main__":
    main()
