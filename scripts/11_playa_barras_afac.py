#!/usr/bin/env python3
"""Barras horizontales divergentes del cambio de pasajeros por destino de playa,
ene-may 2026 vs 2025, en absolutos, ordenado de mayor pérdida (arriba) a mayor
ganancia (abajo). 13 destinos, con la Riviera = Cancún + Tulum agregados.

Tres versiones, mismo estilo y orden, cada una ordenada por su propia métrica:
  TOTAL          (doméstico + internacional)  -> gráfico principal + OG
  DOMÉSTICO      -> sección "los grandes pierden y los medianos ganan"
  INTERNACIONAL  -> sección "el patrón es otro"

Paleta Pulse: navy #0A1628 base, cian #36C6D3 para ganancias, rojo #D97A6C para
pérdidas. El signo se codifica por posición (izq/der del cero) Y por color, más
la etiqueta numérica en cada barra: la identidad no depende solo del color, así
que es legible en daltonismo.

Salida por versión: PNG 800px, PNG 1600px y SVG. Más OG 1200x630 (jpg) del total.
Fuente: AFAC, Estadística Operativa de Aeropuertos. Pivot-cache ya extraído."""
import zipfile, xml.etree.ElementTree as ET, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from PIL import Image
import os

XLSX = "data/afac_aeropuertos_2006_2026.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

INK="#0A1628"; PULSE="#36C6D3"; SAND="#E0AE4E"; MUTE="#9FB0C6"
SOFT="#5C6B80"; LINE="#1B2A44"; RED="#D97A6C"

RIVIERA = ["CANCUN", "TULÚM"]
OTROS = {
    "SAN JOSE DEL CABO": "Los Cabos", "PUERTO VALLARTA": "Puerto Vallarta",
    "MAZATLAN": "Mazatlán", "COZUMEL": "Cozumel", "LA PAZ": "La Paz",
    "ACAPULCO": "Acapulco", "HUATULCO": "Huatulco", "LORETO": "Loreto",
    "MANZANILLO": "Manzanillo", "PUERTO ESCONDIDO": "Puerto Escondido",
    "PUERTO PEÑASCO": "Puerto Peñasco", "ZIHUATANEJO": "Zihuatanejo",
}
YTD = range(1, 6)  # ene-may
# tipos por métrica: 0 = NACIONAL, 1 = INTERNACIONAL (cacheField 1)
METRICS = {
    "total": ((0, 1), "La Riviera concentra la caída",
              "Cambio total de pasajeros por destino de playa, enero a mayo 2026 vs 2025",
              "La Riviera (Cancún + Tulum) es la mayor pérdida del país de playa y explica el 61% del total."),
    "dom":   ((0,), "El mexicano voló menos a la playa",
              "Cambio en pasajeros nacionales por destino de playa, enero a mayo 2026 vs 2025",
              "La caída se concentra en la Riviera; el reacomodo hacia otras playas es marginal."),
    "intl":  ((1,), "El extranjero voló menos",
              "Cambio en pasajeros internacionales por destino de playa, enero a mayo 2026 vs 2025",
              "Casi toda la playa cae; Puerto Vallarta explica el 80% de la pérdida de las doce."),
}


def contrast(a, b):
    def lum(h):
        h=h.lstrip("#"); rgb=[int(h[i:i+2],16)/255 for i in (0,2,4)]
        rgb=[c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4 for c in rgb]
        return 0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2]
    L1,L2=sorted([lum(a),lum(b)],reverse=True)
    return (L1+0.05)/(L2+0.05)


def load():
    z=zipfile.ZipFile(XLSX)
    dfn=ET.fromstring(z.read("xl/pivotCache/pivotCacheDefinition1.xml"))
    SH={i:([it.get("v") for it in list(cf.find("m:sharedItems",NS))] if cf.find("m:sharedItems",NS) is not None else []) for i,cf in enumerate(dfn.findall(".//m:cacheField",NS))}
    rec=ET.fromstring(z.read("xl/pivotCache/pivotCacheRecords1.xml"))
    OPC,YR,APT=SH[0],SH[2],SH[4]
    pax=OPC.index("PASAJEROS/PASSENGERS")
    def cv(c):
        t=tag(c)
        if t=="x": return int(c.get("v"))
        if t=="n": return float(c.get("v"))
        if t=="m": return 0.0
        return c.get("v")
    d=collections.defaultdict(int)  # (apto, tipo, anio) -> pax ene-may
    for r in rec.findall("m:r",NS):
        cs=[cv(c) for c in list(r)]
        if cs[0]!=pax: continue
        apto=APT[cs[4]]; tipo=cs[1]; y=int(YR[cs[2]])
        if y not in (2025,2026): continue
        for mi in YTD:
            v=cs[5+mi-1]
            if v: d[(apto,tipo,y)]+=int(v)
    return d


def rows_for(d, tipos):
    dif=lambda codes: sum(d[(a,t,2026)]-d[(a,t,2025)] for a in codes for t in tipos)
    rows=[("Riviera (Cancún + Tulum)", dif(RIVIERA), True)]
    for code,name in OTROS.items():
        rows.append((name, dif([code]), False))
    rows.sort(key=lambda r: r[1])   # ascendente: mayor pérdida arriba
    return rows


def draw(ax, rows, name_fs, val_fs):
    n=len(rows)
    ys=list(range(n))[::-1]
    maxabs=max(abs(v) for _,v,_ in rows)
    lab_pad=maxabs*0.035
    for y,(name,val,hl) in zip(ys,rows):
        col = RED if val<0 else PULSE
        ax.barh(y, val, height=0.62, color=col, edgecolor=INK, linewidth=0.8, zorder=3)
        if val<0:
            ax.text(lab_pad, y, name, ha="left", va="center",
                    color="#FFFFFF" if hl else MUTE, fontsize=name_fs,
                    fontweight="bold" if hl else "normal", zorder=5)
        else:
            ax.text(-lab_pad, y, name, ha="right", va="center",
                    color=MUTE, fontsize=name_fs, zorder=5)
        txt=f"{val:+,}".replace("-","−")
        off=maxabs*0.012
        if val<0:
            ax.text(val-off, y, txt, ha="right", va="center", color=RED,
                    fontsize=val_fs, fontweight="bold", zorder=5,
                    path_effects=[pe.withStroke(linewidth=2.4,foreground=INK)])
        else:
            ax.text(val+off, y, txt, ha="left", va="center", color=PULSE,
                    fontsize=val_fs, fontweight="bold", zorder=5,
                    path_effects=[pe.withStroke(linewidth=2.4,foreground=INK)])
    ax.axvline(0, color=SOFT, lw=1.1, zorder=4)
    ax.set_xlim(-maxabs*1.30, maxabs*0.70)
    ax.set_ylim(-0.7, n-0.3)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)


def build_main(rows, title, subtitle, note):
    fig,ax=plt.subplots(figsize=(10,7.0))
    fig.patch.set_facecolor(INK); ax.set_facecolor(INK)
    fig.subplots_adjust(left=0.045,right=0.965,top=0.80,bottom=0.075)
    draw(ax, rows, name_fs=10.5, val_fs=9.5)
    fig.text(0.045,0.955,title,color="#FFFFFF",fontsize=17,fontweight="bold",ha="left",va="top")
    fig.text(0.045,0.90,subtitle,color=MUTE,fontsize=10.3,ha="left",va="top")
    fig.text(0.045,0.855,note,color=SAND,fontsize=9.2,ha="left",va="top")
    fig.text(0.045,0.028,"Fuente: AFAC, Estadística Operativa de Aeropuertos. Riviera = Cancún + Tulum. Cálculo y gráfico: Riviera Maya Economic Pulse.",
             color=SOFT,fontsize=7.6,ha="left",va="bottom")
    return fig


def build_og(rows, title, subtitle):
    fig,ax=plt.subplots(figsize=(12,6.30))
    fig.patch.set_facecolor(INK); ax.set_facecolor(INK)
    fig.subplots_adjust(left=0.04,right=0.97,top=0.74,bottom=0.075)
    draw(ax, rows, name_fs=11, val_fs=9.5)
    fig.text(0.04,0.945,title,color="#FFFFFF",fontsize=25,fontweight="bold",ha="left",va="top")
    fig.text(0.04,0.845,subtitle,color=MUTE,fontsize=12.5,ha="left",va="top")
    fig.text(0.04,0.030,"Fuente: AFAC · Riviera Maya Economic Pulse",color=SOFT,fontsize=9.5,ha="left",va="bottom")
    return fig


def main():
    print(f"Contraste rojo/navy: {contrast(RED,INK):.2f}:1 | cian/navy: {contrast(PULSE,INK):.2f}:1 | mute/navy: {contrast(MUTE,INK):.2f}:1")
    d=load()
    for key,(tipos,title,subtitle,note) in METRICS.items():
        rows=rows_for(d,tipos)
        tot=sum(v for _,v,_ in rows)
        print(f"\n== {key.upper()} (orden gráfico) ==  suma 13 = {tot:+,}")
        for name,val,_ in rows: print(f"  {name:<26}{val:>+10,}")
        fig=build_main(rows,title,subtitle,note)
        fig.savefig(f"output/playa_{key}_1600.png",dpi=160,facecolor=INK)
        fig.savefig(f"output/playa_{key}_800.png",dpi=80,facecolor=INK)
        fig.savefig(f"output/playa_{key}.svg",facecolor=INK)
        plt.close(fig)
    # OG del total
    tipos,title,subtitle,_=METRICS["total"]
    rows=rows_for(d,tipos)
    og=build_og(rows,title,subtitle)
    og.savefig("output/_og_tmp.png",dpi=100,facecolor=INK); plt.close(og)
    im=Image.open("output/_og_tmp.png").convert("RGB").resize((1200,630),Image.LANCZOS)
    im.save("output/pulse-og-riviera.jpg",quality=86,optimize=True,progressive=True)
    os.remove("output/_og_tmp.png")
    print(f"\nOG total 1200x630: {os.path.getsize('output/pulse-og-riviera.jpg')//1024}KB")
    print("Escritos: playa_{total,dom,intl}_{1600,800}.png + .svg  +  pulse-og-riviera.jpg")


if __name__=="__main__":
    main()
