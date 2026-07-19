# Scoping: benchmark Caribe. ¿A dónde se fue el turista?

Pregunta del scoping: enero-mayo 2026 contra 2025, ¿los destinos que compiten por
el turista de la Riviera Maya crecieron o cayeron?

Corte de la exploración: 19 de julio de 2026.
Estado: **exploración de fuentes**. Sin conclusiones editoriales. La canasta final
y el ángulo los decide Fernando.

Regla que atraviesa todo el documento: **llegadas de turistas y pasajeros de
aeropuerto son universos distintos y no se restan entre sí.** Cada cifra va
etiquetada con su universo. Las comparaciones entre países son dos series
nacionales puestas lado a lado, nunca una resta.

---

## Sección 1. México, lado receptor (AFAC)

Sin trabajo nuevo: sale del pipeline AFAC ya existente
(`output/afac_nacsplit_2026vs2025.csv` y `output/afac_tulum_operaciones_2026vs2025.csv`).

**Universo:** AFAC, Estadística Operativa de Aeropuertos. Pasajeros de terminal en
ambos sentidos, todas las nacionalidades. Acumulado enero-mayo.

| Destino | Tipo | ene-may 2025 | ene-may 2026 | Var |
|---|---|---:|---:|---:|
| Cancún | total | 13,150,885 | 12,701,085 | **−3.4%** |
| Cancún | nacional | 4,006,866 | 3,763,732 | −6.1% |
| Cancún | internacional | 9,144,019 | 8,937,353 | −2.3% |
| Tulum | total | 619,247 | 423,837 | **−31.6%** |
| Los Cabos | total | 3,369,718 | 3,234,100 | **−4.0%** |
| Los Cabos | internacional | 2,193,156 | 2,107,825 | −3.9% |
| Puerto Vallarta | total | 3,296,426 | 2,922,236 | **−11.4%** |
| Puerto Vallarta | internacional | 2,084,241 | 1,752,410 | −15.9% |
| Mazatlán | total | 780,680 | 715,271 | −8.4% |
| TOTAL NACIONAL | total | 79,180,624 | 78,907,136 | −0.3% |

Dato adicional de Tulum, para la pregunta de frecuencias: **operaciones −29.2%**
(nacional −19.7%, internacional −36.2%). Pasajeros por operación pasó de 111.1 a
107.4, así que la caída de Tulum es de frecuencias, no de aviones más chicos.

---

## Sección 2. República Dominicana, lado pasajeros (JAC)

**Fuente:** Junta de Aviación Civil, "Reporte Histórico 2005 - jun. 2026", hoja
"5. Pasajeros por Aeropuertos". Archivado en `data/benchmark/` con checksum.
Reproducible con `scripts/14_benchmark_jac_rd.py`.

**Universo citado:** pasajeros comerciales de **entrada más salida** por aeropuerto
dominicano, elaborado por la JAC a partir de la base de datos del IDAC. Es
movimiento de terminal, **no** llegadas de turistas.

**Corte y rezago:** llega a **junio 2026**, publicado el 12 de mayo de 2026 para el
corte de abril y actualizado después. Es el rezago más corto de todo el scoping,
más corto incluso que AFAC en México. Aquí se usa enero-mayo para que sea
comparable con Cancún.

| Aeropuerto | ene-may 2025 | ene-may 2026 | Var |
|---|---:|---:|---:|
| Punta Cana | 4,876,559 | 5,408,969 | **+10.9%** |
| Santo Domingo, Las Américas | 2,016,632 | 2,208,398 | +9.5% |
| Santiago | 853,532 | 928,651 | +8.8% |
| Puerto Plata | 442,054 | 460,656 | +4.2% |
| Samaná, El Catey | 51,006 | 85,206 | +67.1% |
| La Romana | 123,154 | 99,804 | −19.0% |
| Santo Domingo, El Higüero | 16,099 | 15,440 | −4.1% |
| **TOTAL PAÍS** | **8,379,036** | **9,207,124** | **+9.9%** |

Validación aplicada: la suma de las filas de aeropuerto cuadra exacto con la fila
"Total" de la propia hoja, en los dos años. El script aborta si no cuadra.

**Reexpresión detectada.** El total de 2025 vale **19,592,794** en el reporte
histórico de junio de 2026 y **19,619,578** en el comunicado de la JAC de enero de
2026: una revisión de **−26,784 (−0.14%)**. Es el mismo fenómeno que SEDETUR pero
un orden de magnitud menor (SEDETUR revisó −2.82%). Confirma que archivar cada
corte no es opcional en ninguna de estas fuentes.

Comparación disponible, sin restar: en el mismo corte enero-mayo y con el mismo
tipo de universo (movimiento de terminal), Cancún hizo **−3.4%** y República
Dominicana **+9.9%**, con Punta Cana en **+10.9%**. Son dos autoridades distintas
de dos países distintos; la lectura es de tendencia, no de diferencia aritmética.

---

## Sección 3. Aruba (ATA)

**Fuente:** Aruba Tourism Authority, "Monthly Report". Índice en `ata.aw/knowledge-base`.
Archivado: `data/benchmark/aruba/` (reportes de abril y mayo 2026, anual 2025).

**Universo citado literal:** "STAY OVER ARRIVALS". Los cruceristas van en línea
aparte ("CRUISE ARRIVALS"). Verificado que no se mezclan: 702,158 stayover más
505,026 cruise dan 1,207,184, que es el "TOTAL STAY OVER AND CRUISE" que publica
el propio reporte. La resta aérea es limpia.

**Corte y rezago:** llega a **mayo 2026**. Junio no está publicado al 19 de julio.
Rezago de 20 a 40 días tras cierre de mes.

**Granularidad:** mensual con acumulado. Desglosa por país **con Estados Unidos
aislado**, y además por estado de la Unión Americana.

Acumulado enero-mayo, dato publicado:

| Concepto | 2025 | 2026 | Var |
|---|---:|---:|---:|
| Stay over, total | 635,965 | 702,158 | **+10.4%** |
| Stay over, Estados Unidos | 471,830 | 492,689 | **+4.4%** |
| Stay over, Canadá | 38,337 | 44,454 | +16.0% |
| Stay over, Argentina | 20,073 | 58,905 | +193.5% |
| Cruceristas | 471,483 | 505,026 | +7% |

**Matiz de composición que conviene no perder:** de los 66,193 stayover adicionales
del acumulado, **38,832 son argentinos**. Aruba crece 10.4% en agregado pero su
mercado estadounidense crece 4.4%. La participación de Estados Unidos en el
stayover bajó de 74.2% a 70.2%, dato publicado por la propia ATA.

---

## Sección 4. Curazao (CTB)

**Fuente:** Curaçao Tourist Board, "Overall Visitor Arrival Performance" (exportación
de Power BI). Índice en `curacaotouristboard.com/monthly-statistics`.
Archivado: `data/benchmark/curazao/` (junio y mayo 2026, abril 2026, mayo 2025).

**Universo citado literal:** "Stayover Arrivals". Cruceristas en tabla propia
("Cruise Arrivals") y una tercera categoría separada, "Day Trippers". Las tres se
publican desglosadas, así que la resta aérea es limpia.

**Corte y rezago:** llega a **junio 2026**, el rezago más corto del bloque caribeño
junto con la JAC: de 9 a 10 días tras cierre de mes.

**Granularidad:** mensual con columna acumulada. Estados Unidos aislado.

Acumulado enero-mayo (para comparar con Aruba), dato publicado:

| Concepto | 2025 | 2026 | Var |
|---|---:|---:|---:|
| Stayover, total | 342,554 | 374,216 | **+9%** |
| Stayover, Estados Unidos | 94,740 | 100,882 | **+6%** |
| Stayover, Canadá | 22,944 | 30,186 | +32% |
| Stayover, Países Bajos | 109,682 | 114,582 | +4% |
| Cruceristas | 430,858 | 476,327 | +11% |

Acumulado enero-junio, disponible solo para Curazao: stayover total 437,086 contra
399,967 (+9%), Estados Unidos 116,952 contra 111,861 (+5%).

**Señal de mes suelto:** en junio 2026 el mercado estadounidense de Curazao **cae**,
16,070 contra 17,121 (−6% publicado). Norteamérica completa cae 4% en el mes. Es un
mes, no una tendencia, pero es el primer dato del bloque que apunta hacia abajo en
el mercado de Estados Unidos.

---

## Sección 5. Jamaica (JTB)

**Fuente:** Jamaica Tourist Board, "Monthly Statistical Report", Vol. XXXVI No. 5.
Fuentes primarias declaradas dentro del PDF: Passport, Immigration & Citizen Agency
(formulario C5) y Port Authority of Jamaica.
Archivado: `data/benchmark/jamaica/`.

**Universo citado literal:** "Total Stopover Arrivals by Permanent Residence".
Clasifica por **residencia permanente**, no por nacionalidad. Los cruceristas van en
columna aparte y solo se suman en "Total Visitor Arrivals", así que la separación ya
viene hecha en la fuente. Se subdivide en "Foreign Nationals" y "Non-Resident
Jamaicans" (846,311 y 71,086 en enero-mayo 2026).

**Corte y rezago:** llega a **mayo 2026**, publicado el 17 de julio de 2026. Rezago
de unos 48 días, el más largo del bloque.

**Granularidad:** mensual y acumulada. Estados Unidos aislado y además por estado y
subregión. Las llegadas **no** se desglosan por aeropuerto sino por zona turística
de destino (Montego Bay, Ocho Ríos, Negril, etc.).

Acumulado enero-mayo, dato publicado:

| Concepto | 2025 | 2026 | Var |
|---|---:|---:|---:|
| Stopover, total | 1,213,228 | 917,397 | **−24.4%** |
| Stopover, Estados Unidos | 836,570 | 593,104 | **−29.1%** |
| Stopover, Canadá | 197,413 | 150,043 | −24.0% |
| Cruceristas | 650,733 | 632,091 | −2.9% |

**Confounder declarado en la propia fuente, y es descalificante:** el reporte abre
diciendo que Jamaica "continues to recover from the impact of the Category 5
hurricane that devastated the Island in late October 2025". La caída de 24.4% **no
es señal de demanda de mercado** y no se puede poner junto a Cancún como si lo fuera.

Nota de calidad de la fuente: la fila de variación de la tabla de airlift viene
rotulada "% Change 2025/2024" sobre columnas de enero-mayo 2026. El rótulo parece
erróneo en el original; esa fila queda como no verificada.

---

## Sección 6. Bahamas (Ministry of Tourism)

**Fuente:** Bahamas Ministry of Tourism, Investments & Aviation, portal TourismToday.
Archivado: `data/benchmark/bahamas/`.

**Universo citado literal:** "Foreign Air Arrival: anyone who is not a resident of
The Bahamas who arrives by scheduled or chartered airline or by a private plane."
La nota metodológica del PDF advierte que es "a manual immigration card count of all
foreign visitors **and transit arrivals**", que excluye tripulaciones y residentes
que regresan, y que "take no account of multiple entries made by the same visitors".

Consecuencia: **la cifra aérea de Bahamas incluye tránsitos y visitantes de un día,
y no es una cifra de pernocta.** No es equivalente al "stopover" de Jamaica ni al
"stayover" de Aruba y Curazao.

**Corte y rezago:** la serie aérea llega a **mayo 2026** (rezago de unos 33 días).
La serie que separa cruceristas de "sea landed" solo llega a **febrero 2026**
(rezago de unos 4 meses). Todo 2026 viene marcado "PRELIMINARY & SUBJECT TO REVISION".

**Granularidad:** mensual y acumulada, con mucho detalle por isla y punto de entrada.
**Por nacionalidad: NO DISPONIBLE para 2026.** El desglose por país de origen existe
pero su corte más reciente es **2024**. **Estados Unidos no se puede aislar en Bahamas
para 2026**, lo que la deja fuera de cualquier lectura por mercado emisor.

Acumulado enero-mayo, dato publicado:

| Concepto | 2025 | 2026 | Var |
|---|---:|---:|---:|
| Llegadas aéreas, total | 813,355 | 852,753 | **+4.8%** |
| Llegadas aéreas, Nassau | 605,748 | 641,090 | +5.8% |
| Llegadas marítimas | 4,506,700 | 5,221,319 | +15.9% |

**Artefacto declarado en la fuente:** el salto de +320.6% en llegadas marítimas de
Gran Bahama se explica en la nota al pie: "In July 2025, Celebration Key in Grand
Bahama opened". Es un puerto privado de crucero nuevo, no crecimiento de demanda.

---

## Sección 7. El emisor como control: Estados Unidos (NTTO)

Esta es la sección que responde si el estadounidense **viajó menos** o **viajó a
otro lado**. Archivado en `data/benchmark/emisores/`.

**Producto útil:** "Total International Travel Volume", artículo mensual gratuito
de NTTO, sección "International Departures from the United States".
Existen otros dos productos: SIAT (encuesta, shares no conteos, sin trimestres de
2026) e I-92 (**de pago**, de 205 a 7,150 dólares). El nombre histórico
"U.S. Citizen Air Traffic to Overseas Regions" está descontinuado.

**Corte y rezago:** último publicado **marzo 2026**, con fecha 4 de junio de 2026.
Rezago de unos 2 meses. Los slugs de abril, mayo y junio 2026 devuelven 404; las
cifras de esos meses que circulan en prensa **no tienen artículo oficial** y no se
dan por verificadas.

**Separabilidad, que era la pregunta crítica: SÍ.** México se publica como país
individual y el Caribe como región propia; México no queda enterrado dentro de
"North America". En el anual de SIAT el Caribe se abre en Aruba, Bahamas,
República Dominicana y Jamaica por separado (**Curazao no**, cae en "Other
Caribbean"), pero como porcentajes de encuesta, no como conteos.

Cifras publicadas, acumulado enero-marzo:

| Serie | 2025 | 2026 |
|---|---:|---:|
| México, YTD ene-mar | 10,440,250 | 10,498,488 |
| Caribe, YTD ene-mar | 3,017,619 | 2,954,688 |
| Total salidas, marzo | 9,128,717 | 9,308,594 |

**ADVERTENCIA QUE INVALIDA EL CÁLCULO DIRECTO.** El artículo de marzo 2026 declara
que su total "increased 5.2 percent compared to March 2025". Pero el artículo de
marzo 2025 publicó 9,128,717 para ese mes, y 9,308,594 sobre 9,128,717 da **+1.97%,
no +5.2%**. Para que el 5.2% se sostenga, marzo 2025 tuvo que reexpresarse a unos
**8,848,473**, una revisión de **−280,244 (−3.07%)**. NTTO no explica la diferencia
en el artículo.

Consecuencia operativa: **NTTO también reexpresa**, y es la tercera fuente de este
scoping que lo hace (SEDETUR −2.82%, JAC −0.14%, NTTO −3.07% implícito). Por lo
tanto las variaciones que se obtienen cruzando las dos cosechas de artículo
(**México +0.56%**, **Caribe −2.09%**) son **indicativas y no citables como dato
duro**. Para construir el control hay que sacar la serie completa de una sola
cosecha, vía los monitores Power BI de NTTO, o comprar I-92.

**Universo, con una inconsistencia de la propia fuente:** el mismo número de 2024
(107,713,681) aparece descrito por NTTO como "U.S. **citizen** international visitor
departures" en el artículo de volumen y como "U.S. **resident** outbound travelers"
en el material de SIAT. Ciudadanos y residentes no son lo mismo y NTTO no lo
resuelve en el material público.

**Riesgo abierto y sin resolver: el cruce terrestre a México.** La página de I-94 de
CBP dice literal que "CBP does not have a system for automatically recording
departures by land to Mexico". La magnitud de la cifra mexicana es incompatible con
tráfico aéreo puro: 39.9 millones anuales en 2024, cuando los destinos mexicanos
top que lista SIAT (Cancún, Ciudad de México, Los Cabos, Guadalajara, Puerto
Vallarta) suman del orden de 11 millones. La inferencia razonable es que la cifra de
México incorpora cruce terrestre por fuente mexicana, pero **NTTO no publica nota
metodológica que lo diga y no hay desglose aire contra tierra en el producto
gratuito**. Mientras eso no se resuelva, **la cifra de México de NTTO no es
comparable con la del Caribe**, que sí es aérea. Es el punto que hay que cerrar
antes de construir cualquier pieza sobre el lado emisor.

---

## Sección 8. El emisor como control: Canadá (Statistics Canada)

**Tabla:** 24-10-0053-01, "International travellers entering or returning to Canada,
by type of transportation and traveller type", programa Frontier Counts. Mensual
desde 1972. Archivado en `data/benchmark/emisores/`.

**Corte y rezago:** llega a **abril 2026**, publicado el 23 de junio de 2026. Rezago
de unos 2 meses. La tabla 24-10-0056 (indicador adelantado, solo aéreo) llega a
**junio 2026** con apenas 2 semanas de rezago.

**Separabilidad de México: NO.** Statistics Canada colapsa el destino de sus
residentes en dos categorías y nada más: "returning from the United States of
America" y "returning from countries other than the United States of America".
Ningún miembro de la dimensión nombra a México ni a país alguno del Caribe. La
única tabla que alguna vez tuvo país de destino (24-10-0037) **murió en 2014**.

**Trampa documentada, que conviene dejar por escrito:** la tabla 24-10-0056 sí trae
una dimensión con 81 miembros donde aparecen `Mexico`, `Bahamas`, `Jamaica` y otros.
Pero esa dimensión es **"Country of residence" de visitantes que ENTRAN a Canadá**,
no el destino de los canadienses. Quien la tome como destino construye el control
al revés.

Cifras publicadas, acumulado enero-abril:

| Serie | 2025 | 2026 | Var |
|---|---:|---:|---:|
| Canadienses que regresan, total | 15,617,304 | 14,934,560 | **−4.37%** |
| Regresando de Estados Unidos | 10,046,908 | 9,041,983 | **−10.00%** |
| Regresando de países distintos a EU | 5,570,396 | 5,892,577 | **+5.78%** |

**Ese +5.78% NO es México.** Es un agregado que mezcla México, el Caribe, Europa,
Asia y todo lo que no sea Estados Unidos. Presentarlo como señal de México sería un
error de lectura.

**Universo citado literal:** "Canadian residents returning from countries other than
the United States of America". Son **residentes**, no ciudadanos, y es conteo de
**cruces fronterizos de regreso**, no de personas únicas ni de viajes. La tabla sí
separa "Excursionists (same-day)" de "Tourists (overnight)", cosa que NTTO no
ofrece del lado emisor.

---

## Sección 9. República Dominicana, lado llegadas (Banco Central)

**Fuente:** Banco Central de la República Dominicana, Estadísticas > Sector Turismo >
Flujo turístico. Los enlaces no están en el HTML servido (es una SPA); el listado se
obtiene del endpoint `POST /Home/GetContentForRender` con `id=2537`.
Archivado en `data/benchmark/republica_dominicana/`.

**Universo citado literal:** "LLEGADA MENSUAL DE PASAJEROS SEGÚN RESIDENCIA Y
AEROPUERTO UTILIZADO, VÍA AÉREA". Nota al pie: desde septiembre de 2021 la
compilación quedó a cargo del MITUR vía formulario electrónico e-ticket, que
suministra al BCRD. Al pie de los gráficos: "Banco Central en base a los datos
recibidos del Ministerio de Turismo (MITUR), provenientes de la Dirección General
de Migración (DGM)". Las cifras vienen marcadas "sujetas a rectificación".

Tres precisiones del universo que importan:

- Es **solo llegadas**, del registro migratorio. **No** es movimiento de terminal.
  **No se resta ni se combina** con la JAC (que cuenta entradas más salidas), ni con
  AFAC, ni con ASUR. Enero 2026 ilustra la brecha: BCRD registra 945,866 llegadas;
  la JAC reporta del orden de 1.8 millones de pasajeros mensuales.
- **Sí incluye dominicanos no residentes que regresan**, en fila propia (727,741 en
  enero-junio 2026), y también residentes en la fila `TOTAL PASAJEROS`.
- **Tránsito: no declarado.** No hay mención en los XLS, en el informe mensual ni en
  la sección. Queda como no confirmado; no se infiere.

**Corte y rezago:** los XLS llegan a **junio 2026**, publicados el 9 de julio.
**Rezago de 9 días**, el más corto de todo el scoping, por delante de su propio
compromiso oficial de 30 días. El informe narrativo en PDF va un mes atrás
(enero-mayo); el de junio devuelve 404.

**Granularidad:** el desglose por país se repite **dentro de cada aeropuerto**, así
que existe el cruce **Estados Unidos por Punta Cana** mensual. Ese es el número
directamente confrontable con la pregunta de mercado emisor de Cancún.

Acumulado enero-mayo:

| Serie | 2025 | 2026 | Var |
|---|---:|---:|---:|
| Total país, TOTAL PASAJEROS | 4,138,223 | 4,553,063 | **+10.0%** (publicado) |
| Total país, no residentes | 3,743,471 | 4,146,831 | +10.8% (publicado) |
| Punta Cana, total pasajeros | 2,431,855 | 2,688,696 | +10.6% (cálculo) |
| **Estados Unidos, país (residencia)** | 1,387,137 | 1,472,416 | **+6.2%** (cálculo) |
| **Estados Unidos, Punta Cana** | 991,496 | 1,037,030 | **+4.6%** (cálculo) |

Acumulado enero-junio, disponible: total país +9.2%, Punta Cana +9.7%, Estados
Unidos país +5.3%, Estados Unidos por Punta Cana +3.9%.

**Validación:** las sumas mensuales del XLS reproducen exactamente las cifras del
informe narrativo de enero-mayo. Única diferencia, 2 unidades en el total de Estados
Unidos, por decimales en las celdas.

**Advertencia de definición:** Estados Unidos tiene **dos cifras distintas y no
intercambiables**, por residencia (1,823,552 en enero-junio) y por nacionalidad
(1,557,623). Para leer mercado emisor, la correcta es residencia. Además, el
desglose por país cuelga de "no residentes > extranjeros", así que **excluye a los
dominicanos no residentes**, muchos de los cuales viven en Estados Unidos.

Nota de calidad: las celdas mensuales por aeropuerto traen decimales (por ejemplo
884.389), lo que sugiere expansión o prorrateo y no conteo entero. La fuente no
explica el método.

---

## Sección 10. Evaluación: ¿es construible el benchmark?

### 10.1 Un patrón que aparece en todas las fuentes con desglose

Ordenando lo verificado, enero-mayo 2026, agregado contra mercado estadounidense:

| Destino | Universo | Total | Mercado Estados Unidos |
|---|---|---:|---:|
| Rep. Dominicana (BCRD) | llegadas | +10.0% | **+6.2%** |
| Punta Cana (BCRD) | llegadas | +10.6% | **+4.6%** |
| Aruba (ATA) | stayover | +10.4% | **+4.4%** |
| Curazao (CTB) | stayover | +9% | **+6%** |
| Bahamas (MOT) | llegadas aéreas | +4.8% | no publicado |
| Jamaica (JTB) | stopover | −24.4% | −29.1% (huracán) |
| Cancún (AFAC) | pax terminal | −3.4% | no separable en AFAC |
| Cancún, pata EU (BTS) | pax de segmento | n/a | **−6.4%** (ene-abr) |

En los cuatro destinos que publican desglose por mercado y no tienen shock, **el
agregado crece entre 9 y 10.6 por ciento pero el mercado estadounidense crece entre
4.4 y 6.2**. El crecimiento del bloque caribeño no está sostenido por Estados Unidos.
En Aruba es explícito: de 66,193 stayover adicionales, 38,832 son argentinos, y la
participación estadounidense bajó de 74.2% a 70.2%.

Esto es una lectura de los datos disponibles, no una conclusión editorial.

### 10.2 Qué es construible y qué no

**Construible, lado receptor.** Cuatro destinos con universo declarado, corte
enero-mayo 2026, desglose de Estados Unidos aislado y rezago de 9 a 40 días. Es una
canasta homogénea en granularidad aunque no en universo.

**No construible con fuentes gratuitas, lado emisor.** Es el hallazgo que más
condiciona el alcance:

- **Canadá queda descartado.** StatCan no separa México ni el Caribe. Punto final,
  no hay vuelta con esa fuente.
- **Estados Unidos queda con dos problemas sin resolver.** NTTO reexpresa (marzo
  2025 revisado en torno a −3.07% sin explicación), lo que invalida calcular
  variaciones cruzando cosechas de artículo. Y no está confirmado si la cifra de
  México incluye cruce terrestre, lo que rompería la comparabilidad con el Caribe.
  Resolverlo exige la serie completa de una sola cosecha desde los monitores Power
  BI, o comprar I-92 (de 205 a 7,150 dólares).

### 10.3 Canasta mínima propuesta

**Núcleo (los cuatro que sí aguantan):**

1. **Cancún**, AFAC pasajeros de terminal, más BTS T-100 para la pata estadounidense.
2. **República Dominicana y Punta Cana**, BCRD llegadas, con el cruce Estados Unidos
   por Punta Cana. Es la fuente más fresca del scoping, 9 días de rezago.
3. **Aruba**, ATA stayover, Estados Unidos aislado.
4. **Curazao**, CTB stayover, Estados Unidos aislado, 9 a 10 días de rezago.

**Corte común:** enero-mayo 2026. Es el único estrictamente comparable entre los
cuatro, porque Aruba y Jamaica no tienen junio.

**Fuera de la canasta, con motivo:**

- **Jamaica**: huracán categoría 5 de octubre de 2025 declarado en la propia fuente.
  Su caída no es señal de demanda de mercado.
- **Bahamas**: sin desglose por país para 2026 (el último es 2024), y su cifra aérea
  incluye tránsitos y visitantes de un día, o sea no es pernocta.
- **Lado emisor**: no resuelto, ver 10.2.

**Regla de presentación que exige esta canasta:** los cuatro miden universos
distintos (pasajeros de terminal, llegadas migratorias, stayover). Van **lado a lado
con su etiqueta**, nunca restados entre sí, y la lectura es de dirección y magnitud
relativa, no de diferencia aritmética.

### 10.4 Pendientes que quedan abiertos

1. Confirmar si la cifra de México de NTTO incluye cruce terrestre. Sin esto el
   control emisor no se sostiene.
2. Sacar la serie NTTO de una sola cosecha (Power BI) para evitar el problema de
   reexpresión.
3. Tratamiento de pasajeros en tránsito en el BCRD: no declarado en ninguna fuente
   primaria consultada.
4. Junio 2026 en Aruba y Jamaica, no publicado al 19 de julio.
5. El método detrás de los decimales en las celdas del BCRD.

### 10.5 Nota transversal sobre reexpresión

**Tres de las fuentes de este scoping revisan cifras ya publicadas:**

| Fuente | Revisión detectada |
|---|---|
| SEDETUR (QRoo) | −2.82% en el total ene-mar 2025 |
| NTTO (Estados Unidos) | −3.07% implícito en marzo 2025 |
| JAC (Rep. Dominicana) | −0.14% en el total 2025 |

Ninguna lo anuncia. Se detectan solo comparando dos cosechas del mismo dato. La
implicación operativa para el benchmark es la misma que ya rige para UPM y SEDETUR:
**archivar cada corte con checksum, y no calcular variaciones mezclando cosechas.**
