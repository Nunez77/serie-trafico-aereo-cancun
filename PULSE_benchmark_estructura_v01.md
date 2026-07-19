# Benchmark Caribe: estructura v01

## Encabezados aprobados por Fernando

**H1:** El Caribe crece sin nosotros

**Dek:** Cuatro destinos comparables del Caribe crecieron entre 9 y 10.6% mientras
Cancún cayó. Y no crecieron por el estadounidense: crecieron porque no dependen de él.

| Sección | H2 |
|---|---|
| S1 | (apertura, sin H2, va bajo el dek) |
| S2 | Cuatro suben, uno baja |
| S3 | El crecimiento no es estadounidense |
| S4 | La diversificación, en una cifra |
| Recuadro metodológico | Lo que se puede comparar y lo que no |

Aquí van el esqueleto, las asignaciones de tabla y gráfico, y los bullets de datos.
**Sin prosa editorial:** el cuerpo todavía no está redactado.

Fuente de todas las cifras: `PULSE_benchmark_caribe_scoping.md`, secciones 1 a 10.
Evidencia archivada con checksums en `data/benchmark/`.

**FRENO TOTAL AL SITIO.** Nada de esto toca `rivieramaya-pulse-site`.

---

## Assets generados

| Asset | Archivo | Tamaños |
|---|---|---|
| G1 | `output/benchmark_g1_variacion_destino` | `_800.png`, `_1600.png`, `.svg` |
| G2 | `output/benchmark_g2_agregado_vs_eu` | `_800.png`, `_1600.png`, `.svg` |
| Script | `scripts/15_benchmark_charts.py` | reproducible |

Títulos dentro de los gráficos, ya alineados con los H2 aprobados:
G1 lleva "Cuatro suben, uno baja" (H2 de S2) y G2 "El crecimiento no es
estadounidense" (H2 de S3). G1 **no** repite el H1 de la pieza, que era su título
provisional.

---

## Tabla firma (formato pieza)

Los universos van como **columna visible**, no como nota al pie: que la
imposibilidad de restar se vea en la tabla.

| Destino | Universo medido | Fuente | Total ene-may | Mercado Estados Unidos |
|---|---|---|---:|---:|
| **Cancún** | pasajeros de terminal | AFAC | **−3.4%** | **−6.4%** ᵃ |
| Curazao | stayover arrivals | CTB | +9.0% | +6.0% |
| Rep. Dominicana | llegadas, registro migratorio | Banco Central | +10.0% | +6.2% |
| Aruba | stay over arrivals | ATA | +10.4% | +4.4% |
| **Punta Cana** ᵇ | llegadas, registro migratorio | Banco Central | **+10.6%** | **+4.6%** |

ᵃ Cancún, pata Estados Unidos: BTS T-100, pasajeros de segmento aéreo, **enero-abril**.
Otro universo y otro corte que el resto de la columna. No se compara de frente.
ᵇ Punta Cana está **dentro** de Rep. Dominicana. No se suman.

**Regla de lectura de la tabla:** cinco autoridades, cinco universos. Las filas se
leen lado a lado. **Ninguna resta entre filas.**

---

## Esqueleto de secciones

### S1. Apertura (sin H2, va bajo el dek)
- **Asset:** tabla firma completa.
- **Bullets de datos:**
  - Cancún, enero-mayo 2026 contra 2025: **−3.4%** (13,150,885 a 12,701,085 pasajeros de terminal, AFAC).
  - Punta Cana, mismo corte: **+10.6%** (2,431,855 a 2,688,696 llegadas, Banco Central).
  - Rep. Dominicana país: **+10.0%** (4,138,223 a 4,553,063 llegadas).
  - Aruba: **+10.4%** (635,965 a 702,158 stayover).
  - Curazao: **+9.0%** (342,554 a 374,216 stayover).

### S2. "Cuatro suben, uno baja"
- **Asset:** **G1** (`benchmark_g1_variacion_destino`). El gráfico ya lleva ese título.
- **Bullets de datos:** los cinco de S1, leídos como contraste. El universo de cada
  destino va rotulado dentro del propio gráfico, así que aquí no hace falta repetirlo.
- **Nota obligatoria:** Punta Cana está dentro de Rep. Dominicana. No se suman.

### S3. "El crecimiento no es estadounidense"
- **Asset:** **G2** (`benchmark_g2_agregado_vs_eu`). El gráfico ya lleva ese título.
- **Bullets de datos:**
  - En los cuatro destinos que crecen, el agregado sube entre **9.0% y 10.6%** y el mercado estadounidense entre **4.4% y 6.2%**. El mercado de Estados Unidos crece menos que el total en los cuatro, sin excepción.
  - Punta Cana: total **+10.6%**, Estados Unidos **+4.6%**.
  - Aruba: total **+10.4%**, Estados Unidos **+4.4%**.
  - Rep. Dominicana: total **+10.0%**, Estados Unidos **+6.2%**.
  - Curazao: total **+9.0%**, Estados Unidos **+6.0%**.
  - Cancún, pata Estados Unidos (BTS T-100, enero-abril, universo distinto): **−6.4%**, con asientos **+0.25%** y factor de ocupación de **83.3% a 77.8%**.

### S4. "La diversificación, en una cifra"
- **Formato:** recuadro (estilo `.limitbox` o equivalente), no párrafo corrido.
- **Bullets de datos:**
  - Aruba sumó **66,193** stay over arrivals en enero-mayo 2026 contra 2025.
  - De esos, **38,832 son argentinos**: el 58.7% del crecimiento (cálculo propio sobre cifras publicadas).
  - Argentina pasó de 20,073 a 58,905 stayover: **+193.5%**.
  - La participación de Estados Unidos en el stayover de Aruba cayó de **74.2% a 70.2%** (dato publicado por ATA).
  - Estados Unidos creció **+4.4%** mientras el total creció **+10.4%**.

### S5. Enlace con "Dos pasaportes" (dentro de S4 o como cierre, a decidir)
- **Formato:** bullets de datos, dos series lado a lado. Los números hacen el trabajo.
- **Bullets de datos:**
  - Cancún, composición de extranjeros por nacionalidad, enero-mayo 2026 (UPM, Cuadro 1.3.1): Estados Unidos y Canadá suman **75.6%**. El tercer mercado, Reino Unido, no llega a **3.5%** (publicado en "Dos pasaportes").
  - Aruba, mismo periodo: participación de Estados Unidos en el stayover **70.2%**, contra 74.2% un año antes; el crecimiento lo aporta Argentina, que sube **+193.5%**.
  - Curazao: Estados Unidos **+6%**, Canadá **+32%**, Países Bajos **+4%**; el crecimiento se reparte entre tres mercados.
  - Rep. Dominicana: total **+10.0%** con Estados Unidos en **+6.2%**.
- **Nota de universo obligatoria en esta sección:** la cifra de Cancún es de UPM (entradas de extranjeros) y las de los otros destinos son de sus autoridades nacionales (stayover y llegadas). Van lado a lado, no se restan.

### Recuadro. "Lo que se puede comparar y lo que no"
- **Formato:** recuadro al cierre, antes de la firma. Contenido completo en el bloque de abajo.

---

## Recuadro "Lo que se puede comparar y lo que no" (contenido)

### Universos, uno por fuente

| Fuente | Qué cuenta exactamente |
|---|---|
| AFAC (México) | Pasajeros de terminal, ambos sentidos, todas las nacionalidades |
| BTS T-100 (Estados Unidos) | Pasajeros embarcados por segmento de vuelo, rutas Estados Unidos a Cancún |
| Banco Central (Rep. Dominicana) | Llegadas vía aérea del registro migratorio (e-ticket, MITUR y DGM) |
| ATA (Aruba) | "Stay over arrivals", cruceristas en línea aparte |
| CTB (Curazao) | "Stayover arrivals", cruceristas y day trippers en tablas aparte |
| UPM (México) | Entradas aéreas de extranjeros por nacionalidad |

**Regla de no resta:** son seis autoridades y seis universos. Ninguna cifra de una
se resta ni se suma con la de otra. Las comparaciones son de dirección y magnitud
relativa, lado a lado.

Dos precisiones que cambian la lectura si se ignoran:
- La cifra del Banco Central **incluye dominicanos no residentes que regresan**
  (727,741 en enero-junio 2026) y también residentes.
- Estados Unidos en el Banco Central tiene dos cifras distintas, por **residencia**
  (la usada aquí) y por **nacionalidad**. No son intercambiables.

### Exclusiones motivadas

- **Jamaica queda fuera.** Su reporte declara que la isla "continues to recover from
  the impact of the Category 5 hurricane that devastated the Island in late October
  2025". Su caída de **−24.4%** en stopover no es señal de demanda de mercado.
- **Bahamas queda fuera.** Su desglose por país de origen no llega a 2026 (el último
  es **2024**), así que Estados Unidos no se puede aislar. Además su cifra aérea
  **incluye tránsitos y visitantes de un día**, o sea no es pernocta y no equivale al
  stayover de Aruba y Curazao.

### El límite del control emisor, declarado como pregunta abierta

Saber si el estadounidense **viajó menos** o **viajó a otro lado** exige el lado
emisor, y ahí el dato público no alcanza:

- **NTTO (Estados Unidos) reexpresa.** Su artículo de marzo 2026 declara +5.2%
  contra marzo 2025, pero contra la cifra que el propio NTTO publicó en 2025 la
  variación es **+1.97%**. Implica una revisión de marzo 2025 cercana a **−3.07%**,
  no explicada.
- **El cruce terrestre a México no es separable.** CBP declara que "does not have a
  system for automatically recording departures by land to Mexico", y la cifra
  mexicana de NTTO (39.9 millones en 2024) es incompatible con tráfico aéreo puro.
  Mientras eso no se resuelva, la cifra de México **no es comparable** con la del
  Caribe, que sí es aérea.
- **Statistics Canada no publica destino desde 2014.** Colapsa el destino de sus
  residentes en "Estados Unidos" contra "todo lo demás". La única tabla que tuvo país
  de destino murió en 2014.

**Por lo tanto esta edición no responde si el viajero estadounidense viajó menos en
total.** Responde a dónde llegó, destino por destino, que es lo que el dato público
sí permite.

### Reexpresiones detectadas

| Fuente | Revisión de una cifra ya publicada |
|---|---|
| SEDETUR (Quintana Roo) | **−2.82%** en el total enero-marzo 2025 |
| NTTO (Estados Unidos) | **−3.07%** implícito en marzo 2025 |
| JAC (Rep. Dominicana) | **−0.14%** en el total 2025 |

Ninguna de las tres lo anuncia. Solo se detectan comparando dos cosechas del mismo
dato. **Por eso el Pulse archiva cada corte con su checksum**: sin la copia previa,
estas revisiones son invisibles y cualquier variación calculada entre cosechas
distintas es falsa.

---

## Pendientes de estructura

- H2 de cada sección: los decide Fernando.
- **El "cuatro" del dek depende de contar Punta Cana como destino propio.** Los que
  crecen son Rep. Dominicana (+10.0%), Aruba (+10.4%), Curazao (+9.0%) y Punta Cana
  (+10.6%). El rango "entre 9 y 10.6%" cuadra exacto con esos cuatro, pero **Punta
  Cana está dentro de Rep. Dominicana** y aporta el 59.1% de sus llegadas: son los
  mismos pasajeros contados en dos filas. Si se cuentan como tres países (Rep.
  Dominicana, Aruba, Curazao), el rango sería "entre 9 y 10.4%". Las dos versiones
  son defendibles si el traslape se declara; hoy la tabla firma y G1 muestran los
  cinco con la nota "Punta Cana está dentro de Rep. Dominicana; no se suman".
- Falta decidir si G2 incluye a Cancún. Hoy sí, con barra rayada y leyenda propia,
  porque su cifra de Estados Unidos es de otro universo y otro corte.
- Junio 2026 existe para Curazao y Rep. Dominicana pero no para Aruba, así que el
  corte común sigue siendo enero-mayo. Si se quiere mover a enero-junio, Aruba sale
  de la canasta.
