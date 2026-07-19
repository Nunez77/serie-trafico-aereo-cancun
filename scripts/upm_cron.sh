#!/usr/bin/env bash
# Envoltura de cron para el archivador del Cuadro 1.3.1 de UPM. Corre en el VPS
# (187.77.12.2, /opt/upm-archive) el día 15 de cada mes.
#
# Hace tres cosas y en este orden:
#   1. sincroniza el repo (pull --rebase) para no divergir de lo que se trabaja local,
#   2. corre el archivador, que es idempotente,
#   3. si apareció un .xls nuevo, lo commitea y lo empuja.
#
# El commit se limita a data/upm/: hay trabajo en paralelo en otras carpetas de
# este repo y el cron no debe arrastrarlo. Nunca `git add -A`.
#
# Si el push falla, el .xls YA está archivado en disco: se pierde el versionado
# de ese mes, no el dato. El log lo deja anotado para recuperarlo a mano.
set -uo pipefail

REPO="/opt/upm-archive"
LOG="/var/log/upm-archive.log"

log(){ echo "$(date '+%Y-%m-%d %H:%M:%S') [cron] $*" >>"$LOG"; }

cd "$REPO" || { log "FALLO no existe $REPO"; exit 1; }

log "inicio"

# 1) sincronizar. Si el pull falla se sigue de todos modos: archivar el .xls es
# más urgente que el versionado, y UPM sobrescribe el archivo cada mes.
if ! git pull --rebase --quiet 2>>"$LOG"; then
  log "AVISO git pull falló; se archiva igual y se intentará commitear después"
fi

# 2) archivar
salida="$(./scripts/archive_upm_1.3.1.sh 2>&1)"
estado=$?
log "archivador: $salida (estado=$estado)"

if [ $estado -ne 0 ]; then
  log "fin con fallo del archivador"
  exit $estado
fi

# 3) versionar solo si hay .xls nuevo bajo data/upm/
if [ -z "$(git status --porcelain -- data/upm)" ]; then
  log "sin cambios que versionar"
  log "fin"
  exit 0
fi

nuevos="$(git status --porcelain -- data/upm | awk '{print $2}' | tr '\n' ' ')"
git add -- 'data/upm/*.xls'
if git diff --cached --quiet; then
  log "cambios en data/upm pero ningún .xls nuevo (¿solo el log?); nada que commitear"
  log "fin"
  exit 0
fi

git commit --quiet -m "Archivador UPM: snapshot del Cuadro 1.3.1 ($(date '+%Y-%m'))" 2>>"$LOG"
if git push --quiet 2>>"$LOG"; then
  log "OK commit y push de: $nuevos"
else
  log "FALLO push; el commit quedó local en $REPO con: $nuevos"
fi

log "fin"
