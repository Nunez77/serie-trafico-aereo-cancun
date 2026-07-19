# Benchmark Caribe: el lado emisor (NTTO y Statistics Canada)

Descargado: 2026-07-19. Checksums en SHA256SUMS.txt.

## Estados Unidos: NTTO / ITA

Producto usado: "Total International Travel Volume", artículo mensual gratuito.
Patrón de URL: https://www.trade.gov/feature-article/<mes>-<anio>-total-international-travel-volume

Otros dos productos existen y NO son intercambiables:
- SIAT (Survey of International Air Travelers): encuesta, publica SHARES no conteos,
  sin trimestres de 2026. Sí abre el Caribe en Aruba, Bahamas, República Dominicana
  y Jamaica; Curazao cae en "Other Caribbean".
- I-92 / APIS: **de pago**, de 205 a 7,150 dólares.

### Universo, con inconsistencia de la fuente

El mismo total de 2024 (107,713,681) aparece descrito por NTTO como
"U.S. **citizen** international visitor departures" en el artículo de volumen y como
"U.S. **resident** outbound travelers" en el material de SIAT. NTTO no lo resuelve
en el material público.

### Dos riesgos abiertos, ambos sin resolver

1. **Reexpresión.** El artículo de marzo 2026 declara +5.2% contra marzo 2025, pero
   contra el 9,128,717 que publicó el artículo de marzo 2025 la variación es +1.97%.
   Implica una revisión de marzo 2025 a unos 8,848,473 (−3.07%). No explicada.
   Por eso las variaciones calculadas cruzando cosechas son indicativas, no citables.
2. **Cruce terrestre a México.** CBP declara que "does not have a system for
   automatically recording departures by land to Mexico", y la magnitud de la cifra
   mexicana (39.9 millones en 2024) es incompatible con tráfico aéreo puro. Mientras
   no se resuelva, **la cifra de México no es comparable con la del Caribe**.

## Canadá: Statistics Canada

Tabla 24-10-0053-01, "International travellers entering or returning to Canada, by
type of transportation and traveller type", programa Frontier Counts.
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2410005301

### Universo (citado literal)

"Canadian residents returning from countries other than the United States of
America". Son **residentes**, no ciudadanos, y es conteo de **cruces fronterizos de
regreso**, no de personas únicas ni de viajes. Separa "Excursionists (same-day)" de
"Tourists (overnight)".

### Limitación que define el alcance

**México no es separable.** El destino se colapsa en "Estados Unidos" contra
"países distintos a Estados Unidos". Ningún miembro nombra a México ni a país
alguno del Caribe. La única tabla que tuvo país de destino (24-10-0037) murió
en 2014, con único periodo 2014.

### Trampa a evitar

La tabla 24-10-0056 trae una dimensión con `Mexico`, `Bahamas`, `Jamaica` y otros,
pero es **"Country of residence" de visitantes que ENTRAN a Canadá**, no el destino
de los canadienses. Tomarla como destino construye el control al revés.
