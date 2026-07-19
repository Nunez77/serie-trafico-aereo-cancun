#!/usr/bin/env python3
"""Gráficos firma del benchmark Caribe (estilo serie Pulse, fondo navy).

  G1) Variación total por destino, ene-may 2026 vs 2025. Cada barra rotulada con
      su UNIVERSO, porque los cuatro destinos no miden lo mismo y la imposibilidad
      de restarlos tiene que ser visible en el gráfico, no en una nota al pie.
  G2) Agregado contra mercado de Estados Unidos, barras pareadas por destino.

Títulos provisionales; los definitivos van con el H2 editorial.

REGLA QUE GOBIERNA ESTOS GRÁFICOS: cada destino viene de una autoridad distinta y
mide un universo distinto (pasajeros de terminal, llegadas migratorias, stayover).
Las barras se leen lado a lado, NUNCA como una resta entre destinos.

Cancún aparece en G2 con tratamiento visual distinto: su cifra de mercado
estadounidense viene de BTS T-100 (pasajeros de segmento aéreo, ene-abr), que es
otro universo y otro corte que el resto de la fila. Va marcada.

Fuentes y cifras: PULSE_benchmark_caribe_scoping.md, secciones 1 a 9.
Salida por gráfico: PNG 800, PNG 1600 y SVG.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

INK = "#0A1628"; PULSE = "#36C6D3"; SAND = "#E0AE4E"; MUTE = "#9FB0C6"
SOFT = "#5C6B80"; LINE = "#1B2A44"; RED = "#D97A6C"

FIRMA = "Cálculo y gráfico: Riviera Maya Economic Pulse."

# destino, variación total, universo (etiqueta corta), fuente
G1 = [
    ("Cancún",             -3.4,  "pasajeros de terminal", "AFAC"),
    ("Curazao",             9.0,  "stayover",              "CTB"),
    ("Rep. Dominicana",    10.0,  "llegadas",              "Banco Central"),
    ("Aruba",              10.4,  "stayover",              "ATA"),
    ("Punta Cana",         10.6,  "llegadas",              "Banco Central"),
]

# destino, total, mercado EU, nota del universo del dato de EU
G2 = [
    ("Cancún",          -3.4, -6.4, True),   # True = universo distinto, va marcado
    ("Curazao",          9.0,  6.0, False),
    ("Rep. Dominicana", 10.0,  6.2, False),
    ("Aruba",           10.4,  4.4, False),
    ("Punta Cana",      10.6,  4.6, False),
]


def guardar(fig, nombre):
    fig.savefig(f"output/{nombre}_1600.png", dpi=160, facecolor=INK)
    fig.savefig(f"output/{nombre}_800.png", dpi=80, facecolor=INK)
    fig.savefig(f"output/{nombre}.svg", facecolor=INK)
    plt.close(fig)


def _ejes(ax):
    ax.set_facecolor(INK)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis="y", color=LINE, linewidth=1, zorder=0)
    ax.set_axisbelow(True)


# ---------- G1: variación total por destino ----------
def g1(fs_tick=9.2, fs_val=11, fs_uni=7.4):
    fig, ax = plt.subplots(figsize=(10, 5.9))
    fig.patch.set_facecolor(INK)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.76, bottom=0.30)
    _ejes(ax)

    x = range(len(G1))
    vals = [v for _, v, _, _ in G1]
    cols = [RED if v < 0 else PULSE for v in vals]
    ax.bar(x, vals, width=0.62, color=cols, zorder=3)
    ax.axhline(0, color=MUTE, linewidth=1.1, zorder=4)

    for i, (nom, v, uni, fte) in enumerate(G1):
        dy = 0.4 if v >= 0 else -0.4
        va = "bottom" if v >= 0 else "top"
        ax.text(i, v + dy, f"{v:+.1f}%", ha="center", va=va,
                color="#FFFFFF" if v >= 0 else RED,
                fontsize=fs_val, fontweight="bold", zorder=5)
        # nombre, universo y fuente van bajo el eje, en coordenadas de figura para
        # que no dependan de la escala: el universo tiene que verse pegado al dato
        for yy, txt, col, fs, st in (
            (-0.075, nom, MUTE, fs_tick, "normal"),
            (-0.135, uni, SAND, fs_uni, "italic"),
            (-0.185, fte, SOFT, fs_uni - 0.6, "normal"),
        ):
            ax.annotate(txt, xy=(i, yy), xycoords=("data", "axes fraction"),
                        ha="center", va="top", color=col, fontsize=fs, style=st,
                        annotation_clip=False)

    ax.set_xticks([])
    ax.set_ylim(-6.5, 13.5)
    ax.set_yticks([-5, 0, 5, 10])
    ax.set_yticklabels(["-5%", "0", "+5%", "+10%"], color=MUTE, fontsize=fs_tick - 0.7)
    ax.set_xlim(-0.62, len(G1) - 0.38)

    fig.text(0.075, 0.955, "El Caribe crece sin nosotros",
             color="#FFFFFF", fontsize=15.5, fontweight="bold", ha="left", va="top")
    fig.text(0.075, 0.905, "Variación del flujo de visitantes, enero-mayo 2026 contra 2025",
             color=MUTE, fontsize=9.8, ha="left", va="top")
    fig.text(0.075, 0.862,
             "Cada destino mide un universo distinto (en dorado). Se leen lado a lado, no se restan.",
             color=SAND, fontsize=9, ha="left", va="top")
    fig.text(0.075, 0.062,
             "Fuentes: AFAC (México), Banco Central de la República Dominicana, ATA (Aruba), CTB (Curazao).",
             color=SOFT, fontsize=7.4, ha="left", va="bottom")
    fig.text(0.075, 0.028,
             "Punta Cana está dentro de Rep. Dominicana; no se suman. " + FIRMA,
             color=SOFT, fontsize=7.4, ha="left", va="bottom")
    return fig


# ---------- G2: agregado contra mercado de Estados Unidos ----------
def g2(fs_tick=9.2, fs_val=9.4):
    fig, ax = plt.subplots(figsize=(10, 5.9))
    fig.patch.set_facecolor(INK)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.76, bottom=0.215)
    _ejes(ax)

    w = 0.34
    for i, (nom, tot, eu, distinto) in enumerate(G2):
        ax.bar(i - w / 2, tot, width=w, color=PULSE if tot >= 0 else RED, zorder=3)
        # el dato de EU de Cancún es de otro universo: se dibuja hueco, no sólido
        if distinto:
            ax.bar(i + w / 2, eu, width=w, facecolor="none", edgecolor=SAND,
                   linewidth=1.4, hatch="///", zorder=3)
        else:
            ax.bar(i + w / 2, eu, width=w, color=SAND, zorder=3)

        for xx, v in ((i - w / 2, tot), (i + w / 2, eu)):
            dy = 0.45 if v >= 0 else -0.45
            ax.text(xx, v + dy, f"{v:+.1f}", ha="center",
                    va="bottom" if v >= 0 else "top",
                    color=MUTE if v >= 0 else RED, fontsize=fs_val, zorder=5)

    ax.axhline(0, color=MUTE, linewidth=1.1, zorder=4)
    ax.set_xticks(range(len(G2)))
    ax.set_xticklabels([n for n, _, _, _ in G2], color=MUTE, fontsize=fs_tick)
    ax.set_ylim(-9.5, 17.5)
    ax.set_yticks([-5, 0, 5, 10])
    ax.set_yticklabels(["-5%", "0", "+5%", "+10%"], color=MUTE, fontsize=fs_tick - 0.7)
    ax.set_xlim(-0.62, len(G2) - 0.38)

    ax.legend(handles=[
        Patch(facecolor=PULSE, label="Total del destino"),
        Patch(facecolor=SAND, label="Mercado de Estados Unidos"),
        Patch(facecolor="none", edgecolor=SAND, hatch="///",
              label="Cancún, pata EU: otro universo (BTS, ene-abr)"),
    ], loc="upper left", frameon=False, fontsize=8.2, labelcolor=MUTE, handlelength=1.7,
       bbox_to_anchor=(0.0, 1.0))

    fig.text(0.075, 0.955, "El crecimiento no es estadounidense",
             color="#FFFFFF", fontsize=15.5, fontweight="bold", ha="left", va="top")
    fig.text(0.075, 0.905,
             "Variación del total contra la del mercado de Estados Unidos, enero-mayo 2026 contra 2025",
             color=MUTE, fontsize=9.8, ha="left", va="top")
    fig.text(0.075, 0.862,
             "En los cuatro destinos que crecen, el mercado estadounidense crece menos que el agregado.",
             color=SAND, fontsize=9, ha="left", va="top")
    fig.text(0.075, 0.062,
             "Fuentes: AFAC y BTS T-100 (Cancún), Banco Central de la República Dominicana, ATA (Aruba), CTB (Curazao).",
             color=SOFT, fontsize=7.4, ha="left", va="bottom")
    fig.text(0.075, 0.028,
             "La barra rayada es otro universo y otro corte: no se compara con las sólidas. " + FIRMA,
             color=SOFT, fontsize=7.4, ha="left", va="bottom")
    return fig


if __name__ == "__main__":
    guardar(g1(), "benchmark_g1_variacion_destino")
    guardar(g2(), "benchmark_g2_agregado_vs_eu")
    print("G1: benchmark_g1_variacion_destino (800/1600/SVG)")
    print("G2: benchmark_g2_agregado_vs_eu (800/1600/SVG)")
    print()
    print("Recordatorio: universos distintos por destino. Lado a lado, nunca restados.")
