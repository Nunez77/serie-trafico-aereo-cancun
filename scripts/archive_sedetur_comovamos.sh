#!/usr/bin/env bash
# Archiva "¿Cómo vamos en turismo?" de SEDETUR Quintana Roo SIN sobrescribir.
#
# Por qué existe: SEDETUR REEXPRESA su propia serie entre reportes. El total de
# afluencia ene-mar 2025 vale 5,384,416 en como_vamos_202503.pdf y 5,232,585 en
# como_vamos_202603.pdf, una revisión de -151,831 turistas (-2.82%). Sin la copia
# de cada mes es imposible reconstruir qué decía la fuente en cada momento, y
# cualquier variación interanual calculada entre dos cosechas distintas es falsa.
# Mismo riesgo que el Cuadro 1.3.1 de UPM, distinta mecánica: UPM sobrescribe un
# archivo por año, SEDETUR publica archivos nuevos pero corrige los números viejos.
#
# Cadencia observada: el corte del mes M se publica entre 6 y 8 semanas después
# (ene-may 2026 se publicó el 2026-07-13). Corre el día 15, junto con UPM.
#
# Nomenclatura de la fuente: como_vamos_AAAAMM.pdf, donde MM es el mes de CIERRE
# de un acumulado que arranca en enero, no un mes suelto. Hay huecos: 202602
# nunca se publicó.
#
# Idempotente: solo baja lo que no está archivado.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO/data/sedetur"
LOG="$DEST/archive.log"
BASE="https://sedeturqroo.gob.mx/ARCHIVOS/comovamos"
UA="Mozilla/5.0 (archivador Como Vamos; Riviera Maya Pulse)"
MIN_BYTES=200000

mkdir -p "$DEST"
log(){ echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >>"$LOG"; }
tamano(){ stat -c%s "$1" 2>/dev/null || stat -f%z "$1" 2>/dev/null || echo 0; }

TMPD="$(mktemp -d)"
trap 'rm -rf "$TMPD"' EXIT

# 1) leer el índice del directorio (Apache autoindex) y sacar los .pdf
IDX="$TMPD/index.html"
if ! curl -sL -A "$UA" --retry 3 --retry-delay 5 --max-time 90 -o "$IDX" "$BASE/"; then
  log "FALLO no se pudo leer el índice de $BASE/"
  echo "FALLO indice"; exit 1
fi

# Los href vienen url-encoded y con mayúsculas irregulares; se resuelven en Python
# y se emite "href<TAB>nombre_local".
#
# Ojo con las colisiones: el directorio tiene "COMO VAMOS ABRIL 2021.pdf" y
# "COMO_VAMOS_ABRIL_2021.pdf", que al normalizar caen en el mismo nombre pero
# son archivos DISTINTOS (2.3 MB contra 4.9 MB, hashes distintos). Normalizar sin
# más perdía uno en silencio. Cuando dos href chocan se les cuelga un sufijo
# estable derivado del href original, para que la corrida sea idempotente.
python3 - "$IDX" >"$TMPD/lista.txt" <<'PY'
import re, sys, html, hashlib, collections
from urllib.parse import unquote

src = open(sys.argv[1], encoding="utf-8", errors="replace").read()
hrefs = []
for h in re.findall(r'(?i)href="([^"]+\.pdf)"', src):
    h = html.unescape(h)
    if not h.startswith(("http", "/")) and h not in hrefs:
        hrefs.append(h)

def norm(h):
    n = unquote(h).lower()
    n = re.sub(r"[^a-z0-9._-]+", "_", n)
    return re.sub(r"_+", "_", n).strip("_")

cuenta = collections.Counter(norm(h) for h in hrefs)
for h in hrefs:
    n = norm(h)
    if cuenta[n] > 1:                       # colisión: desambiguar de forma estable
        tok = hashlib.sha1(h.encode()).hexdigest()[:6]
        raiz = n[:-4] if n.endswith(".pdf") else n
        n = f"{raiz}__{tok}.pdf"
    print(f"{h}\t{n}")
PY

total=$(wc -l <"$TMPD/lista.txt" | tr -d ' ')
if [ "$total" -lt 10 ]; then
  log "FALLO el índice devolvió solo $total PDFs (¿cambió el sitio?)"
  echo "FALLO indice corto"; exit 1
fi

nuevos=0; fallos=0
while IFS=$'\t' read -r href local_name; do
  [ -z "$href" ] && continue
  OUT="$DEST/$local_name"
  [ -e "$OUT" ] && continue

  TMP="$TMPD/descarga.pdf"
  code="$(curl -sL -A "$UA" --retry 3 --retry-delay 4 --max-time 180 \
          -o "$TMP" -w '%{http_code}' "$BASE/$href" 2>/dev/null)"
  size="$(tamano "$TMP")"

  # validación: HTTP 200, tamaño mínimo y cabecera PDF real (el 404 devuelve HTML)
  if [ "$code" != "200" ] || [ "$size" -lt "$MIN_BYTES" ] || [ "$(head -c 4 "$TMP")" != "%PDF" ]; then
    log "FALLO $local_name http=$code size=${size}b (no es PDF válido)"
    fallos=$((fallos+1)); continue
  fi

  mv "$TMP" "$OUT"
  sha="$(shasum -a 256 "$OUT" | awk '{print $1}')"
  log "OK archivado $local_name (${size}b) sha256=$sha"
  nuevos=$((nuevos+1))
done <"$TMPD/lista.txt"

# 2) refrescar el manifiesto de checksums.
# LC_ALL=C fija el orden: macOS y Linux ordenan los guiones distinto y, sin esto,
# cada corrida en la otra máquina reescribía el archivo entero y generaba un
# commit que no cambiaba ni un hash.
( cd "$DEST" && LC_ALL=C shasum -a 256 *.pdf 2>/dev/null | LC_ALL=C sort -k2 >SHA256SUMS.txt )

log "fin: $total en el índice, $nuevos nuevos, $fallos fallidos"
echo "OK indice=$total nuevos=$nuevos fallos=$fallos"
[ "$fallos" -gt 0 ] && exit 2
exit 0
