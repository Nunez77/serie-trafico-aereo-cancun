#!/usr/bin/env bash
# Archiva el Cuadro 1.3.1 de UPM (SEGOB) cada mes SIN sobrescribir.
#
# Por qué existe: UPM publica el 1.3.1 (entradas aéreas por nacionalidad y punto
# de internación) como un solo archivo por año que se SOBRESCRIBE cada mes. Al
# cerrar el año queda como año completo y se pierde la foto acumulada de cada
# mes (p. ej. ene-may). Este script baja el archivo vigente y lo guarda con
# sufijo de periodo (c131_YYYY_MM.xls) para conservar la serie mensual.
#
# Cadencia: el acumulado del mes M se publica ~día 7 del mes M+2 (evidencia:
# ene-may 2026 guardado 2026-07-07). Corre el día 15 para dar margen, por cron
# en el VPS (ver scripts/upm_cron.sh). El host portales.segob.gob.mx tiene el
# cert TLS mal encadenado -> curl -k.
#
# Idempotente: si el archivo del periodo ya existe, no lo vuelve a bajar.
# Portable macOS/Linux: el tamaño se lee con stat de GNU o de BSD, según haya.
set -uo pipefail

# stat -c es GNU (Linux) y stat -f es BSD (macOS); el script corre en los dos.
tamano(){ stat -c%s "$1" 2>/dev/null || stat -f%z "$1" 2>/dev/null || echo 0; }

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO/data/upm"
LOG="$DEST/archive.log"
PY="$REPO/.venv/bin/python"
YEAR="$(date +%Y)"
PAGE="https://portales.segob.gob.mx/es/PoliticaMigratoria/CuadrosBOLETIN?Anual=${YEAR}&Secc=1"
BASE="https://portales.segob.gob.mx/work/models/PoliticaMigratoria/CEM/Estadisticas/Boletines_Estadisticos/${YEAR}"
UA="Mozilla/5.0 (archivador UPM 1.3.1; Riviera Maya Pulse)"

mkdir -p "$DEST"
log(){ echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >>"$LOG"; }

# 1) localizar el href del cuadro 1.3.1 en la página del año vigente.
# El nombre del archivo varía por año (cuadro1.3.1_.xls en 2025, cuadro_1.3.1.xls
# en 2026), así que se extrae el href real del HTML en vez de asumirlo. La página
# viene en Latin-1 (no UTF-8), lo que rompe grep en locale UTF-8; por eso la
# extracción va en Python (_upm_href.py, decodifica latin-1). Se reintenta porque
# el host responde vacío de forma intermitente.
TMPD="$(mktemp -d)"
trap 'rm -rf "$TMPD"' EXIT
PAGE_TMP="$TMPD/pagina.html"
href=""
for try in 1 2 3 4 5; do
  curl -sk -A "$UA" --max-time 40 -o "$PAGE_TMP" "$PAGE" 2>/dev/null
  href="$("$PY" "$REPO/scripts/_upm_href.py" "$YEAR" <"$PAGE_TMP" 2>/dev/null)"
  [ -n "$href" ] && break
  sleep 5
done
if [ -z "$href" ]; then
  log "FALLO no se encontró el href de 1.3.1 en la página ${YEAR} tras 5 intentos (¿cambió el sitio?)"
  echo "FALLO href"; exit 1
fi
URL="${BASE}/${href}"

# 2) descargar a temporal
TMP="$TMPD/c131.xls"
code="$(curl -sk -A "$UA" --retry 4 --retry-delay 5 --max-time 120 -o "$TMP" -w '%{http_code}' "$URL" 2>/dev/null)"
size="$(tamano "$TMP")"
if [ "$code" != "200" ] || [ "$size" -lt 500000 ]; then
  log "FALLO descarga http=$code size=${size}b url=$URL"
  echo "FALLO descarga"; exit 1
fi

# 3) validar estructura y derivar periodo (año, mes) con xlrd
chk="$("$PY" "$REPO/scripts/_upm_check.py" "$TMP" 2>/dev/null)"
if [ "${chk%% *}" != "OK" ]; then
  log "FALLO validación: $chk (size=${size}b)"
  echo "FALLO validacion $chk"; exit 1
fi
y="$(echo "$chk" | awk '{print $2}')"; m="$(echo "$chk" | awk '{print $3}')"
OUT="$DEST/c131_${y}_${m}.xls"

# 4) archivar sin sobrescribir
if [ -e "$OUT" ]; then
  log "OK sin cambio: c131_${y}_${m}.xls ya existe (periodo vigente ya archivado)"
  echo "SKIP existe c131_${y}_${m}.xls"; exit 0
fi
mv "$TMP" "$OUT"
log "OK archivado c131_${y}_${m}.xls (${size}b) desde $URL"
echo "OK c131_${y}_${m}.xls"
