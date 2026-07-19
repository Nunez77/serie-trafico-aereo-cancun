# Serie histórica de tráfico aéreo: Cancún, Cozumel y Tulum

Serie mensual de pasajeros de los aeropuertos de **Cancún (CUN)** y **Cozumel
(CZM)** (a partir del workbook oficial de **ASUR**) y del aeropuerto de **Tulum
(TQO)** (a partir de la Estadística Operativa de Aeropuertos de la **AFAC**, el
regulador federal). Datos, scripts y metodología abiertos para que cualquiera
reproduzca el cálculo y llegue al mismo número.

> **Dos fuentes oficiales.** Cancún y Cozumel provienen de ASUR (el operador);
> Tulum, de AFAC (el regulador), porque Tulum no es un aeropuerto de ASUR. Ambas
> son oficiales. Donde se traslapan (Cancún, que aparece en las dos) coinciden al
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
  06_playa_afac.py       Serie anual de los destinos de playa vs total nacional (AFAC)
  07_region_afac.py      Cancún/Cozumel/Chetumal con split nac/intl + validación vs ASUR
  08_nacional_split_afac.py  Total nacional (68 aptos) + Los Cabos/PV/Mazatlán con split
  09_tulum_riviera_afac.py   Tulum + combinado "Riviera aérea" (Cancún+Tulum) con split
  10_playa_vs_urbano_afac.py Clasifica los 68 aptos en playa vs no playa + agregados
  11_playa_barras_afac.py    Barras del cambio por destino de playa: total, doméstico e internacional
  12_internacional_charts.py Pareto de nacionalidad (Cancún, UPM) + pax/vuelo mensual (AFAC)
  archive_upm_1.3.1.sh       Archiva mensualmente el Cuadro 1.3.1 de UPM sin sobrescribir
  archive_sedetur_comovamos.sh  Archiva "¿Cómo vamos?" de SEDETUR (reexpresa cifras)
  13_tulum_operaciones_afac.py  Tulum: operaciones y pasajeros ene-may 2026 vs 2025
  _upm_href.py / _upm_check.py  Helpers del archivador (href de la página; validación + periodo)
  upm_cron.sh                Envoltura de cron de los archivadores (VPS: pull, archiva, commit+push)
  com.rivieramayapulse.upm-archive.plist  LaunchAgent de respaldo, NO activo (ver archivador)
output/
  asur_pax_tidy.csv          Serie ASUR validada (CUN + CZM), formato tidy
  asur_pax_2019plus.csv      Subconjunto 2019 en adelante
  afac_tulum_tidy.csv        Serie mensual de Tulum (TQO), formato tidy
  afac_playa_*.csv           Serie anual playa vs nacional, pico y 2026 vs 2025
  afac_region_*.csv          Cancún/Cozumel/Chetumal con split + validación vs ASUR
  afac_nacsplit_*.csv        Total nacional + Los Cabos/PV/Mazatlán con split nac/intl
  afac_tulum_split_*.csv     Tulum y "Riviera aérea" (Cancún+Tulum) con split
  afac_playa_vs_urbano_ytd.csv  Agregado playa/no playa + desglose por aeropuerto
  trafico_cancun_{1600,800}.png / .svg     Gráfico Cancún
  panel_cancun_tulum_{1600,800}.png / .svg Small-multiple Cancún vs Tulum
  playa_{total,dom,intl}_{1600,800}.png / .svg  Barras del cambio por destino (3 versiones)
  pulse-og-riviera.jpg       Imagen OG de la pieza (cambio total por destino)
  intl_pareto_nacionalidad_{1600,800}.png / .svg  Pareto de nacionalidad (Cancún, UPM)
  intl_paxvuelo_mensual_{1600,800}.png / .svg     Pax por vuelo mensual, Cancún intl (AFAC)
  upm_cancun_nacionalidad_2026_ene-may.csv        Extracto tidy del Cuadro 1.3.1 (Cancún)
data/upm/
  c131_YYYY_MM.xls           Snapshots archivados del Cuadro 1.3.1 de UPM (ver archivador)
data/sedetur/
  como_vamos_*.pdf           Los 80 "¿Cómo vamos?" de SEDETUR + SHA256SUMS.txt
data/benchmark/
  jac_*.pdf/.xlsx            Benchmark Caribe: JAC República Dominicana (ver FUENTE.md)
CLASSIFICATION.md        Clasificación playa/no playa de los 68 aptos, con criterio y listas
```

## Segunda entrega: la Riviera concentra la caída

De enero a mayo de 2026, la Riviera Maya (Cancún + Tulum) perdió **294,541
pasajeros nacionales**, más que las catorce playas del país juntas (−285,177):
sin la Riviera, la playa mexicana **gana** viajeros nacionales. La caída nacional
la cargan los destinos grandes, mientras La Paz, Zihuatanejo y Puerto Escondido
crecen. En el mercado internacional el patrón no se repite: casi toda la playa
cae, con Puerto Vallarta al frente. El país que **no** es playa gana en los dos
mercados, así que la caída no es macro.

Todo esto sale del mismo pivot-cache de AFAC (`scripts/06`–`11`), con la
clasificación de los 68 aeropuertos documentada en
[`CLASSIFICATION.md`](CLASSIFICATION.md). La validación cruzada Cancún/Cozumel
contra ASUR está en `07_region_afac.py`.

## Archivo del Cuadro 1.3.1 de UPM (por qué archivamos)

Para el desglose internacional por nacionalidad se usa el **Cuadro 1.3.1** de la
Unidad de Política Migratoria (SEGOB): entradas aéreas de extranjeros por país de
nacionalidad y punto de internación, con Cancún, Tulum y Cozumel como columnas
propias. **UPM publica ese cuadro como un solo archivo por año que se sobrescribe
cada mes**, así que al cerrar el año queda como año completo y se pierde la foto
acumulada de cada mes (por ejemplo ene-may). Internet Archive tampoco lo capturó
en la ventana relevante. Conclusión operativa: **UPM sobrescribe, nosotros
archivamos**.

`scripts/archive_upm_1.3.1.sh` baja el cuadro vigente (curl -k, el host tiene el
cert TLS mal encadenado), valida estructura y periodo con `xlrd`, y lo guarda en
`data/upm/c131_YYYY_MM.xls` **sin sobrescribir** (idempotente; si el periodo ya
está archivado, no hace nada). La página viene en Latin-1, no UTF-8, por lo que la
extracción del enlace va en Python (`_upm_href.py`). Registra cada corrida en
`data/upm/archive.log`.

Cadencia: el acumulado del mes M se publica alrededor del día 7 del mes M+2
(evidencia: el archivo ene-may 2026 quedó guardado el 2026-07-07). El archivador
corre el **día 15** para dar margen.

### Dónde corre: cron en el VPS (activo)

La automatización vive en el VPS 187.77.12.2, no en la Mac: una laptop que
duerme se pierde la corrida del mes y UPM ya sobrescribió el archivo.

| | |
|---|---|
| Clon | `/opt/upm-archive` (este repo, rama `main`) |
| Envoltura | `scripts/upm_cron.sh` (corre UPM y SEDETUR; si una falla, la otra sigue) |
| Crontab (root) | `15 9 15 * * /opt/upm-archive/scripts/upm_cron.sh` |
| Log | `/var/log/upm-archive.log` |
| Credencial | deploy key SSH de solo este repo (`vps-archivador-upm`, con escritura), alias `github-upm` en `/root/.ssh/config` |

El wrapper hace pull, corre los dos archivadores (UPM y SEDETUR) y, **solo si
apareció material nuevo**, commitea y empuja. El `git add` está acotado a
`data/upm/*.xls` y `data/sedetur/*.pdf`: en este repo hay trabajo en otras
carpetas y el cron no debe arrastrarlo. Si una fuente falla, la otra sigue y el
wrapper sale con código 2. Si el push falla, lo archivado ya quedó en disco y el
log lo anota; se recupera a mano.

```bash
# corrida manual en el VPS
ssh root@187.77.12.2 'cd /opt/upm-archive && ./scripts/upm_cron.sh; tail /var/log/upm-archive.log'
# corrida manual en cualquier máquina (solo archiva, no versiona)
bash scripts/archive_upm_1.3.1.sh
bash scripts/archive_sedetur_comovamos.sh
```

## Archivo de "¿Cómo vamos?" de SEDETUR (por qué archivamos)

UPM sobrescribe un archivo por año. SEDETUR hace algo distinto y peor de detectar:
**publica archivos nuevos y corrige hacia atrás los números ya publicados.**

Caso verificado el 19 de julio de 2026, afluencia de turistas al Caribe Mexicano,
acumulado enero-marzo de 2025:

| Reporte que se consulte | Total ene-mar 2025 |
|---|---:|
| `data/sedetur/como_vamos_202503.pdf`, p.8 (publicado en 2025) | 5,384,416 |
| `data/sedetur/como_vamos_202603.pdf`, p.8 (base del reporte de 2026) | 5,232,585 |
| Diferencia | **−151,831 (−2.82%)** |

Las dos cifras son de SEDETUR, dicen medir lo mismo, y difieren en casi tres
puntos. Consecuencia operativa: **una variación interanual que tome el año en
curso de un reporte y el año anterior de otro es falsa.** Solo son válidas las
comparaciones internas a un mismo PDF, y para poder hacerlas hay que conservar
todos los PDFs. De ahí este archivo.

`scripts/archive_sedetur_comovamos.sh` lee el índice de
`sedeturqroo.gob.mx/ARCHIVOS/comovamos/`, baja lo que falte y refresca
`data/sedetur/SHA256SUMS.txt`. Valida HTTP 200, tamaño mínimo y cabecera `%PDF`
(el 404 del sitio devuelve HTML, que sin ese chequeo se archivaría como si fuera
un PDF). Registra cada corrida en `data/sedetur/archive.log`.

Dos rarezas de la fuente que el script ya contempla:

- **Nomenclatura.** `como_vamos_AAAAMM.pdf` donde MM es el mes de **cierre de un
  acumulado que arranca en enero**, no un mes suelto. Hay huecos: `como_vamos_202602`
  nunca se publicó (404).
- **Colisión de nombres.** El directorio tiene `COMO VAMOS ABRIL 2021.pdf` y
  `COMO_VAMOS_ABRIL_2021.pdf`, que al normalizar caen en el mismo nombre pero son
  archivos distintos (2.3 MB contra 4.9 MB, hashes distintos). Cuando dos href
  chocan se les añade un sufijo estable derivado del href, así que ambos se
  conservan y la corrida sigue siendo idempotente.

Al 19 de julio de 2026 el archivo tiene los **80 PDFs** del directorio, de 2017 a
mayo de 2026. Pesan cerca de 250 MB, así que clonar este repo ya no es barato.

### LaunchAgent de macOS (respaldo documentado, NO activo)

`scripts/com.rivieramayapulse.upm-archive.plist` queda como respaldo por si el
VPS deja de estar disponible. **No está cargado** y no debe cargarse mientras el
cron del VPS esté activo: los dos a la vez archivan el mismo periodo y compiten
por el push.

```bash
# activarlo solo si el cron del VPS se apaga
cp scripts/com.rivieramayapulse.upm-archive.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/com.rivieramayapulse.upm-archive.plist
# desactivarlo
launchctl unload -w ~/Library/LaunchAgents/com.rivieramayapulse.upm-archive.plist
```

Los workbooks originales de ASUR y AFAC **no se redistribuyen** en este
repositorio: se obtienen de la fuente (ver `scripts/00_descargar.sh`). Lo que se
preserva aquí es el CSV derivado (el dato ya tidy y validado), de modo que la liga
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
