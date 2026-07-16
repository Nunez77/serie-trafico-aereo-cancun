# Serie histórica de tráfico aéreo — Cancún, Cozumel y Tulum

Serie mensual de pasajeros de los aeropuertos de **Cancún (CUN)** y **Cozumel
(CZM)** —a partir del workbook oficial de **ASUR**— y del aeropuerto de **Tulum
(TQO)** —a partir de la Estadística Operativa de Aeropuertos de la **AFAC**, el
regulador federal—. Datos, scripts y metodología abiertos para que cualquiera
reproduzca el cálculo y llegue al mismo número.

> **Dos fuentes oficiales.** Cancún y Cozumel provienen de ASUR (el operador);
> Tulum, de AFAC (el regulador), porque Tulum no es un aeropuerto de ASUR. Ambas
> son oficiales. Donde se traslapan —Cancún, que aparece en las dos— coinciden al
> **2 pasajeros en 2023** y difieren **~0.5% en 2024 y 2025**. Se declara la mezcla
> de fuentes de forma explícita.

El dato duro cubre **enero 2000 – junio 2026** (último mes disponible al corte).
El foco de esta entrega es el techo de **2023**: tras la recuperación pospandemia,
el tráfico anual de Cancún alcanzó su máximo histórico ese año (32.75 M) y desde
entonces **encadena dos años a la baja** (2024 −7.1%, 2025 −3.5%), con 2026 camino
al tercero.

## Qué hay aquí

```
scripts/
  00_descargar.sh        Notas para obtener los workbooks oficiales (fuentes primarias)
  01_extract.py          Parsea el workbook de ASUR -> CSV tidy (con validación)
  02_report.py           Totales anuales, variación interanual y verificación cruzada
  03_chart.py            Gráfico de la serie mensual de Cancún (techo 2023)
  04_tulum_afac.py       Extrae Tulum del pivot-cache del Excel de AFAC + valida Cancún
  05_panel_cancun_tulum.py  Small-multiple Cancún vs Tulum a la misma escala
output/
  asur_pax_tidy.csv          Serie ASUR validada (CUN + CZM), formato tidy
  asur_pax_2019plus.csv      Subconjunto 2019 en adelante
  afac_tulum_tidy.csv        Serie mensual de Tulum (TQO), formato tidy
  trafico_cancun_{1600,800}.png / .svg     Gráfico Cancún
  panel_cancun_tulum_{1600,800}.png / .svg Small-multiple Cancún vs Tulum
```

Los workbooks originales de ASUR y AFAC **no se redistribuyen** en este
repositorio: se obtienen de la fuente (ver `scripts/00_descargar.sh`). Lo que se
preserva aquí es el CSV derivado —el dato ya tidy y validado—, de modo que la liga
a la fuente es trazabilidad, no dependencia.

## Formato del CSV (`asur_pax_tidy.csv`)

| columna | descripción |
|---|---|
| `aeropuerto` | `CUN` (Cancún) o `CZM` (Cozumel) |
| `anio` | año |
| `mes` | mes, 1–12 |
| `nacional` | pasajeros nacionales |
| `internacional` | pasajeros internacionales |
| `total` | pasajeros totales (nacional + internacional) |

## Metodología

1. **Fuente.** Workbook oficial *Tráfico de pasajeros* de ASUR
   (https://www.asur.com.mx/trafico-de-pasajeros-1), hojas `PAX CUN` y `PAX CZM`.
   Columnas: Año · Mes · Nacional · Internacional · Total.

2. **Parseo bloque por bloque.** Cada año es un bloque delimitado por su etiqueta
   de año y su fila `Total AÑO`. El workbook publicado contiene una región
   desalineada en el tramo 2006–2008 (bloques duplicados y una etiqueta de año
   espuria). Para no arrastrar esa basura, el extractor **valida cada bloque**: la
   suma de sus doce meses debe igualar exactamente la fila `Total AÑO` publicada.
   Un bloque que no cuadra, o un año repetido, se marca y **no entra** al CSV
   limpio. Todos los bloques 2019–2026 cuadran al peso con su total oficial.

3. **Verificación cruzada.** El acumulado enero–mayo 2026 y sus variaciones se
   contrastan contra cifras previamente publicadas por el proyecto. La corrida
   imprime `CUADRA` / `NO CUADRA` para cada una (ver `02_report.py`).

4. **Tulum (AFAC).** Tulum no es aeropuerto de ASUR, así que su serie sale de la
   *Estadística Operativa de Aeropuertos* de la AFAC (https://www.gob.mx/afac).
   La tabla dinámica del Excel solo muestra un mes, pero su **pivot-cache** interno
   guarda los doce meses × tipo (nacional/internacional) × aeropuerto × 2006–2026;
   `04_tulum_afac.py` lo lee y extrae Tulum (etiquetado `TULÚM`, grupo GAFSACOMM).
   Como control de calidad, el mismo script valida el **Cancún de AFAC contra el de
   ASUR**: coinciden a 2 pasajeros en 2023 y difieren ~0.5% en 2024–2025. Cancún se
   reporta con ASUR (serie larga, incluye junio); Tulum, con AFAC. La mezcla de dos
   fuentes oficiales se declara de forma explícita.

5. **Gráficos.** *Cancún:* serie mensual (línea cian) sobre fondo oscuro, con una
   escalera del **promedio mensual de cada año** (línea sand) superpuesta al mismo
   eje: hace visible el ascenso pospandemia, el techo de 2023 y el descenso de
   2024–2025 sin recurrir a un doble eje. Se marca el **máximo anual (2023)** y,
   por separado para no confundirlos, el **máximo mensual (marzo 2024)**; se anota
   la caída interanual de cada año y el acumulado en curso de 2026. Se conservan la
   línea base de 2019 (punteada) y la banda del cierre de 2020, y se sombrea el
   tramo de descenso 2023 → 2026. Ambos colores se validan por contraste sobre el
   fondo (≥ 3:1) y por separación para daltonismo (ΔE muy por encima del piso).
   *Cancún vs Tulum:* small-multiple de dos paneles apilados a la **misma escala Y**.
   La escala compartida es deliberada: muestra el tamaño real de Tulum (~4% del
   tráfico regional), sin la distorsión que produciría indexar a base 100 o darle un
   eje propio. Doble eje: nunca.

## Reproducir

```bash
python3 -m venv .venv && ./.venv/bin/pip install pandas openpyxl matplotlib
bash scripts/00_descargar.sh          # instrucciones para bajar los workbooks a data/
./.venv/bin/python scripts/01_extract.py       # ASUR -> asur_pax_tidy.csv
./.venv/bin/python scripts/02_report.py        # reporte + verificación cruzada
./.venv/bin/python scripts/03_chart.py         # gráfico Cancún
./.venv/bin/python scripts/04_tulum_afac.py    # AFAC -> afac_tulum_tidy.csv (+ validación)
./.venv/bin/python scripts/05_panel_cancun_tulum.py  # small-multiple Cancún vs Tulum
```

## Licencia

- **Código** (`scripts/`): [MIT](LICENSE).
- **Datos derivados y gráficos** (`output/`): [CC BY 4.0](LICENSE-DATA).
  Atribución sugerida: *Riviera Maya Economic Pulse, a partir de datos de ASUR y AFAC.*

Los datos originales son propiedad de ASUR y de la AFAC y se usan aquí para fines de
análisis; este repositorio publica únicamente la serie derivada y el método para
reproducirla.

---

*Riviera Maya Economic Pulse*
