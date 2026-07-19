# Benchmark Caribe: índice de fuentes

Carpeta de evidencia del scoping "¿A dónde se fue el turista?".
Ver `PULSE_benchmark_caribe_scoping.md` en la raíz del repo.

| Carpeta | País | Fuente | Universo | Corte | Rezago |
|---|---|---|---|---|---|
| (raíz) | Rep. Dominicana | JAC | pasajeros de terminal (entrada + salida) | jun 2026 | corto |
| `republica_dominicana/` | Rep. Dominicana | Banco Central | llegadas, registro migratorio | jun 2026 | 9 días |
| `aruba/` | Aruba | ATA | stayover arrivals | may 2026 | 20 a 40 días |
| `curazao/` | Curazao | CTB | stayover arrivals | jun 2026 | 9 a 10 días |
| `jamaica/` | Jamaica | JTB | stopover, por residencia permanente | may 2026 | 48 días |
| `bahamas/` | Bahamas | Ministry of Tourism | llegadas aéreas, incluye tránsito | may 2026 | 33 días |
| `emisores/` | EU y Canadá | NTTO y StatCan | salidas y retornos de residentes | mar y abr 2026 | 2 meses |

**Regla que aplica a toda la carpeta:** cada país mide un universo distinto. Las
cifras van lado a lado con su etiqueta, **nunca restadas entre sí**. Cada subcarpeta
tiene su propio `FUENTE.md` con el universo citado literal y sus advertencias.

**Por qué se archiva todo esto.** Tres de las fuentes de este scoping reexpresan
cifras ya publicadas sin anunciarlo: SEDETUR (−2.82%), NTTO (−3.07% implícito) y la
JAC (−0.14%). Solo se detecta comparando dos cosechas del mismo dato, y para eso
hay que conservarlas.
