#!/usr/bin/env python3
"""Gráficos de la pieza internacional (estilo serie Pulse, fondo navy):

  A) Pareto de composición: entradas aéreas de extranjeros a Cancún por
     nacionalidad, ene-may 2026, barras de participación + línea de % acumulado.
     Fuente: UPM (SEGOB), Cuadro 1.3.1 (data/upm/c131_2026_05.xls).
  B) Pasajeros por vuelo, Cancún internacional, ene-may, dos series 2025 vs 2026.
     Fuente: AFAC, Estadística Operativa de Aeropuertos (pivot-cache).

Títulos descriptivos provisionales (los finales van con el H2 editorial).
Universos NO se mezclan: A es entradas de extranjeros (UPM), B es pasajeros de
terminal (AFAC); van en gráficos separados.

Salida por gráfico: PNG 800px, PNG 1600px y SVG. Más CSV derivado de nacionalidad.
No se redistribuye el .xls crudo de UPM aquí; se archiva en data/upm/ (ver cron)."""
import zipfile, xml.etree.ElementTree as ET, collections, csv, os
import xlrd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from PIL import Image

AFAC = "data/afac_aeropuertos_2006_2026.xlsx"
UPM26 = "data/upm/c131_2026_05.xls"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
tag = lambda e: e.tag.split('}')[-1]

INK="#0A1628"; PULSE="#36C6D3"; SAND="#E0AE4E"; MUTE="#9FB0C6"
SOFT="#5C6B80"; LINE="#1B2A44"; RED="#D97A6C"

def contrast(a,b):
    def lum(h):
        h=h.lstrip("#"); rgb=[int(h[i:i+2],16)/255 for i in (0,2,4)]
        rgb=[c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4 for c in rgb]
        return 0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2]
    L1,L2=sorted([lum(a),lum(b)],reverse=True); return (L1+0.05)/(L2+0.05)

# ---------- datos ----------
AGG={"extranjeros","américa","america","américa del norte","america del norte",
 "américa central","america central","islas del caribe","américa del sur","america del sur",
 "europa","asia","áfrica","africa","oceanía","oceania","apátrida","apatrida","no especificado",
 "asia central","asia meridional","asia oriental","sudeste asiático","sudeste asiatico",
 "cercano oriente","medio oriente"}
def _noise(l):
    ll=l.lower(); return (not l or l[0].isdigit() or "significa" in ll or "notas" in ll
        or "continente" in ll or "cuadro" in ll or "total" in ll)

def upm_cancun(col=3):
    wb=xlrd.open_workbook(UPM26); sh=wb.sheet_by_index(0)
    er=next(r for r in range(sh.nrows) if str(sh.cell_value(r,2)).strip().lower()=="extranjeros")
    tot=int(round(float(sh.cell_value(er,col))))
    out=[]
    for r in range(er+1,sh.nrows):
        lab=str(sh.cell_value(r,2)).strip()
        if _noise(lab) or lab.lower() in AGG: continue
        try: v=int(round(float(sh.cell_value(r,col))))
        except: continue
        out.append((lab.replace(" 1",""),v))
    out.sort(key=lambda x:-x[1])
    return tot,out

def afac_cancun_intl_monthly():
    z=zipfile.ZipFile(AFAC)
    dfn=ET.fromstring(z.read("xl/pivotCache/pivotCacheDefinition1.xml"))
    SH={i:([it.get("v") for it in list(cf.find("m:sharedItems",NS))] if cf.find("m:sharedItems",NS) is not None else []) for i,cf in enumerate(dfn.findall(".//m:cacheField",NS))}
    rec=ET.fromstring(z.read("xl/pivotCache/pivotCacheRecords1.xml"))
    OPC,YR,APT=SH[0],SH[2],SH[4]
    OP=OPC.index("OPERACIONES/ FLIGHTS"); PAX=OPC.index("PASAJEROS/PASSENGERS")
    def cv(c):
        t=tag(c)
        if t=="x": return int(c.get("v"))
        if t=="n": return float(c.get("v"))
        if t=="m": return 0.0
        return c.get("v")
    d=collections.defaultdict(int)  # (met,anio,mes)
    for r in rec.findall("m:r",NS):
        cs=[cv(c) for c in list(r)]
        if cs[1]!=1: continue           # TIPO internacional
        if APT[cs[4]]!="CANCUN": continue
        if cs[0] not in (OP,PAX): continue
        y=int(YR[cs[2]]); met="op" if cs[0]==OP else "pax"
        for mi in range(12):
            v=cs[5+mi]
            if v: d[(met,y,mi+1)]+=int(v)
    return d

# ---------- A) Pareto composición ----------
def _draw_pareto(ax, top, resto, tot, pct_fs, tick_fs):
    labels=[l for l,_ in top]+["Resto"]
    vals=[v for _,v in top]+[resto]
    shares=[v/tot*100 for v in vals]
    cum=[]; acc=0
    for s in shares: acc+=s; cum.append(acc)
    x=range(len(labels))
    colors=[PULSE]*len(top)+[SOFT]   # la cola en gris para distinguir el agregado
    ax.bar(x,shares,color=colors,edgecolor=INK,linewidth=0.8,width=0.72,zorder=3)
    for i,s in enumerate(shares):
        ax.text(i,s+1.4,f"{s:.1f}%",ha="center",va="bottom",color=MUTE,fontsize=pct_fs,zorder=5)
    # línea de acumulado (mismo eje 0-100, sin doble eje)
    ax.plot(x,cum,color=SAND,lw=1.8,marker="o",ms=4,zorder=4,
            path_effects=[pe.withStroke(linewidth=3,foreground=INK)])
    for i,c in enumerate(cum):
        if i in (1,4,len(cum)-1):
            ax.annotate(f"{c:.1f}%",(i,c),textcoords="offset points",xytext=(0,8),
                        color=SAND,fontsize=pct_fs-0.5,ha="center",fontweight="bold")
    ax.set_ylim(0,100); ax.set_xticks(list(x))
    ax.set_xticklabels(labels,rotation=35,ha="right",color=MUTE,fontsize=tick_fs)
    ax.set_yticks([0,25,50,75,100]); ax.set_yticklabels(["0","25","50","75","100%"])
    ax.tick_params(colors=MUTE,labelsize=tick_fs,length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.grid(axis="y",color=LINE,lw=0.8,zorder=0); ax.set_axisbelow(True)
    leg=[plt.Rectangle((0,0),1,1,color=PULSE),Line2D([0],[0],color=SAND,lw=1.8,marker="o",ms=4)]
    ax.legend(leg,["Participación por país","% acumulado"],loc="center right",
              frameon=False,fontsize=tick_fs,labelcolor=MUTE)

def chart_pareto():
    tot,cs=upm_cancun(); top=cs[:10]; resto=tot-sum(v for _,v in top)
    fig,ax=plt.subplots(figsize=(10,5.6))
    fig.patch.set_facecolor(INK); ax.set_facecolor(INK)
    fig.subplots_adjust(left=0.065,right=0.975,top=0.80,bottom=0.16)
    _draw_pareto(ax, top, resto, tot, 8.5, 8.5)
    fig.text(0.065,0.955,"Tres de cada cuatro extranjeros, dos países",
             color="#FFFFFF",fontsize=15.5,fontweight="bold",ha="left",va="top")
    fig.text(0.065,0.905,"Entradas de extranjeros a Cancún por nacionalidad, ene-may 2026",
             color=MUTE,fontsize=9.8,ha="left",va="top")
    fig.text(0.065,0.86,"Ningún otro país supera 3.5%.",
             color=SAND,fontsize=9,ha="left",va="top")
    fig.text(0.065,0.03,"Fuente: UPM (SEGOB), Cuadro 1.3.1, entradas aéreas de extranjeros. Cálculo y gráfico: Riviera Maya Economic Pulse.",
             color=SOFT,fontsize=7.4,ha="left",va="bottom")
    return fig,(tot,top,resto)

def og_pareto(tot,top,resto):
    fig,ax=plt.subplots(figsize=(12,6.30))
    fig.patch.set_facecolor(INK); ax.set_facecolor(INK)
    fig.subplots_adjust(left=0.055,right=0.98,top=0.75,bottom=0.17)
    _draw_pareto(ax, top, resto, tot, 9.5, 9.5)
    fig.text(0.055,0.945,"Dos pasaportes sostienen la Riviera",
             color="#FFFFFF",fontsize=24,fontweight="bold",ha="left",va="top")
    fig.text(0.055,0.85,"Entradas de extranjeros a Cancún por nacionalidad, ene-may 2026",
             color=MUTE,fontsize=12,ha="left",va="top")
    fig.text(0.055,0.03,"Fuente: UPM (SEGOB), Cuadro 1.3.1 · Riviera Maya Economic Pulse",
             color=SOFT,fontsize=9.5,ha="left",va="bottom")
    return fig

# ---------- B) pax/vuelo mensual ----------
MES=["Ene","Feb","Mar","Abr","May"]
def chart_paxvuelo(d):
    def pv(y): return [d[("pax",y,m)]/d[("op",y,m)] for m in range(1,6)]
    y25,y26=pv(2025),pv(2026)
    fig,ax=plt.subplots(figsize=(10,5.4))
    fig.patch.set_facecolor(INK); ax.set_facecolor(INK)
    fig.subplots_adjust(left=0.07,right=0.975,top=0.80,bottom=0.12)
    x=range(5)
    ax.plot(x,y25,color=MUTE,lw=2,ls=(0,(5,3)),marker="o",ms=5,zorder=3,label="2025")
    ax.plot(x,y26,color=PULSE,lw=2.4,marker="o",ms=5,zorder=4,label="2026",
            path_effects=[pe.withStroke(linewidth=3.4,foreground=INK)])
    for i,(a,b) in enumerate(zip(y25,y26)):
        ax.annotate(f"{a:.0f}",(i,a),textcoords="offset points",xytext=(0,9),color=MUTE,fontsize=8,ha="center")
        ax.annotate(f"{b:.0f}",(i,b),textcoords="offset points",xytext=(0,-15),color=PULSE,fontsize=8.5,ha="center",fontweight="bold")
    ax.set_ylim(140,168); ax.set_xticks(list(x)); ax.set_xticklabels(MES)
    ax.set_yticks([140,150,160]); ax.set_yticklabels(["140","150","160"])
    ax.tick_params(colors=MUTE,labelsize=9,length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.grid(axis="y",color=LINE,lw=0.8,zorder=0); ax.set_axisbelow(True)
    ax.legend(loc="lower left",frameon=False,fontsize=9,labelcolor=MUTE,handlelength=1.8)
    fig.text(0.07,0.955,"Los aviones volaron más vacíos",
             color="#FFFFFF",fontsize=15.5,fontweight="bold",ha="left",va="top")
    fig.text(0.07,0.905,"Cancún internacional: pasajeros por vuelo, 2025 vs 2026",
             color=MUTE,fontsize=9.8,ha="left",va="top")
    fig.text(0.07,0.86,"Cada mes de 2026 queda por debajo de 2025.",
             color=SAND,fontsize=9,ha="left",va="top")
    fig.text(0.07,0.03,"Fuente: AFAC, Estadística Operativa de Aeropuertos (pasajeros y operaciones internacionales). Eje recortado a 140-168. Cálculo y gráfico: Riviera Maya Economic Pulse.",
             color=SOFT,fontsize=7.4,ha="left",va="bottom")
    return fig,(y25,y26)

def save(fig,name):
    fig.savefig(f"output/{name}_1600.png",dpi=160,facecolor=INK)
    fig.savefig(f"output/{name}_800.png",dpi=80,facecolor=INK)
    fig.savefig(f"output/{name}.svg",facecolor=INK)
    plt.close(fig)

def main():
    print(f"Contraste cian/navy {contrast(PULSE,INK):.2f} | sand/navy {contrast(SAND,INK):.2f} | mute/navy {contrast(MUTE,INK):.2f}")
    figA,(tot,top,resto)=chart_pareto(); save(figA,"intl_pareto_nacionalidad")
    # CSV derivado (tidy) de la composición
    with open("output/upm_cancun_nacionalidad_2026_ene-may.csv","w",newline="") as fh:
        w=csv.writer(fh); w.writerow(["pais","entradas_extranjeros_2026_ene_may","pct_del_total","pct_acumulado"])
        acc=0
        for lab,v in top:
            acc+=v; w.writerow([lab,v,f"{v/tot*100:.2f}",f"{acc/tot*100:.2f}"])
        w.writerow(["Resto",resto,f"{resto/tot*100:.2f}","100.00"])
        w.writerow(["TOTAL extranjeros",tot,"100.00","100.00"])
    print(f"Pareto: total {tot:,}; top2 {(top[0][1]+top[1][1])/tot*100:.1f}%; CSV escrito.")
    d=afac_cancun_intl_monthly()
    figB,(y25,y26)=chart_paxvuelo(d); save(figB,"intl_paxvuelo_mensual")
    print("pax/vuelo 2025:", [f"{v:.1f}" for v in y25])
    print("pax/vuelo 2026:", [f"{v:.1f}" for v in y26])
    # OG de la pieza, a partir del Pareto (gráfico firma), 1200x630
    og=og_pareto(tot,top,resto)
    og.savefig("output/_og_tmp.png",dpi=100,facecolor=INK); plt.close(og)
    Image.open("output/_og_tmp.png").convert("RGB").resize((1200,630),Image.LANCZOS)\
        .save("output/pulse-og-dos-pasaportes.jpg",quality=86,optimize=True,progressive=True)
    os.remove("output/_og_tmp.png")
    print(f"OG: pulse-og-dos-pasaportes.jpg ({os.path.getsize('output/pulse-og-dos-pasaportes.jpg')//1024}KB)")
    print("Gráficos: intl_pareto_nacionalidad y intl_paxvuelo_mensual (800/1600/SVG) + OG.")

if __name__=="__main__":
    main()
