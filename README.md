# Serie histórica de tráfico aéreo — Cancún y Cozumel (ASUR)

Serie mensual de pasajeros de los aeropuertos de **Cancún (CUN)** y **Cozumel
(CZM)**, reconstruida a partir del workbook oficial de tráfico de pasajeros de
**ASUR**. Datos, scripts y metodología abiertos para que cualquiera reproduzca el
cálculo y llegue al mismo número.

El dato duro cubre **enero 2000 – junio 2026** (último mes disponible al corte).
El foco de esta entrega es el techo de **2023**: tras la recuperación pospandemia,
el tráfico anual de Cancún alcanzó su máximo histórico ese año (32.75 M) y desde
entonces **encadena dos años a la baja** (2024 −7.1%, 2025 −3.5%), con 2026 camino
al tercero.

## Qué hay aquí

```
scripts/
  01_extract.py   Parsea el workbook de ASUR y produce el CSV tidy (con validación)
  02_report.py    Totales anuales, variación interanual y verificación cruzada
  03_chart.py     Gráfico de la serie mensual de Cancún (paleta del proyecto)
output/
  asur_pax_tidy.csv        Serie completa validada (CUN + CZM), formato tidy
  asur_pax_2019plus.csv    Subconjunto 2019 en adelante
  trafico_cancun_1600.png  Gráfico (1600 px)
  trafico_cancun_800.png   Gráfico (800 px)
  trafico_cancun.svg       Gráfico (vectorial)
scripts/00_descargar.sh    Descarga el workbook oficial (fuente primaria)
```

El workbook original de ASUR **no se redistribuye** en este repositorio: se
descarga de la fuente con `scripts/00_descargar.sh`. Lo que se preserva aquí es el
CSV derivado —el dato ya tidy y validado—, de modo que la liga a ASUR es
trazabilidad, no dependencia.

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

4. **Gráfico.** Serie mensual de Cancún (línea cian) sobre fondo oscuro, con una
   escalera del **promedio mensual de cada año** (línea sand) superpuesta al mismo
   eje: hace visible el ascenso pospandemia, el techo de 2023 y el descenso de
   2024–2025 sin recurrir a un doble eje. Se marca el **máximo anual (2023)** y,
   por separado para no confundirlos, el **máximo mensual (marzo 2024)**; se anota
   la caída interanual de cada año y el acumulado en curso de 2026. Se conservan la
   línea base de 2019 (punteada) y la banda del cierre de 2020, y se sombrea el
   tramo de descenso 2023 → 2026. Ambos colores se validan por contraste sobre el
   fondo (≥ 3:1) y por separación para daltonismo (ΔE muy por encima del piso).

## Reproducir

```bash
python3 -m venv .venv && ./.venv/bin/pip install pandas openpyxl matplotlib
bash scripts/00_descargar.sh          # baja el workbook de ASUR a data/
./.venv/bin/python scripts/01_extract.py
./.venv/bin/python scripts/02_report.py
./.venv/bin/python scripts/03_chart.py
```

## Licencia

- **Código** (`scripts/`): [MIT](LICENSE).
- **Datos derivados y gráficos** (`output/`): [CC BY 4.0](LICENSE-DATA).
  Atribución sugerida: *Riviera Maya Economic Pulse, a partir de datos de ASUR.*

Los datos originales son propiedad de ASUR y se usan aquí para fines de análisis;
este repositorio publica únicamente la serie derivada y el método para reproducirla.

---

*Riviera Maya Economic Pulse*
