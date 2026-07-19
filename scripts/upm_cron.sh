#!/usr/bin/env bash
# Envoltura de cron para los archivadores mensuales. Corre en el VPS
# (187.77.12.2, /opt/upm-archive) el día 15 de cada mes.
#
# Hace tres cosas y en este orden:
#   1. sincroniza el repo (pull --rebase) para no divergir de lo que se trabaja local,
#   2. corre los archivadores, que son idempotentes:
#        - Cuadro 1.3.1 de UPM (SEGOB), que se sobrescribe cada mes,
#        - "¿Cómo vamos?" de SEDETUR QRoo, que REEXPRESA cifras ya publicadas,
#   3. si apareció material nuevo, lo commitea y lo empuja.
#
# El commit se limita a data/upm/ y data/sedetur/: hay trabajo en paralelo en
# otras carpetas de este repo y el cron no debe arrastrarlo. Nunca `git add -A`.
#
# Un archivador que falle no cancela al otro: se registra y se sigue.
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

# 2) archivar. Cada fuente por separado; el fallo de una no tumba a la otra.
fallas=0

salida="$(./scripts/archive_upm_1.3.1.sh 2>&1)"
estado=$?
log "archivador UPM: $salida (estado=$estado)"
[ $estado -ne 0 ] && fallas=$((fallas+1))

salida="$(./scripts/archive_sedetur_comovamos.sh 2>&1)"
estado=$?
log "archivador SEDETUR: $salida (estado=$estado)"
[ $estado -ne 0 ] && fallas=$((fallas+1))

# 3) versionar solo si hay material nuevo bajo data/upm/ o data/sedetur/
if [ -z "$(git status --porcelain -- data/upm data/sedetur)" ]; then
  log "sin cambios que versionar"
  log "fin"
  exit 0
fi

nuevos="$(git status --porcelain -- data/upm data/sedetur | awk '{print $2}' | tr '\n' ' ')"
git add -- 'data/upm/*.xls' 'data/sedetur/*.pdf' 'data/sedetur/SHA256SUMS.txt'
if git diff --cached --quiet; then
  log "cambios en data/ pero nada archivable (¿solo los logs?); nada que commitear"
  log "fin"
  exit 0
fi

git commit --quiet -m "Archivadores: snapshots de UPM 1.3.1 y SEDETUR ($(date '+%Y-%m'))" 2>>"$LOG"
if git push --quiet 2>>"$LOG"; then
  log "OK commit y push de: $nuevos"
else
  log "FALLO push; el commit quedó local en $REPO con: $nuevos"
fi

log "fin (archivadores con falla: $fallas)"
exit $([ "$fallas" -gt 0 ] && echo 2 || echo 0)
