#!/usr/bin/env bash
# Obtiene los workbooks oficiales (fuentes primarias). No se redistribuyen en el
# repo; se bajan de la fuente para reproducir el pipeline.
set -euo pipefail
mkdir -p data

# --- ASUR (Cancún, Cozumel) ---
# Se puede bajar directo por HTTP:
ASUR="https://www.asur.com.mx/media/Inversionistas/Trafico%20de%20pasajeros/Trafico_de_pasajeros_ASUR.xlsx"
curl -fSL -A "Mozilla/5.0" -o data/Trafico_de_pasajeros_ASUR.xlsx "$ASUR"
echo "OK: data/Trafico_de_pasajeros_ASUR.xlsx"

# --- AFAC (Tulum) ---
# gob.mx sirve un gate de JavaScript a los clientes no-navegador, por lo que curl
# recibe solo un shell HTML, NO el archivo. Descarga el Excel manualmente desde:
#
#   https://www.gob.mx/afac/acciones-y-programas/estadisticas-280404
#   -> "(Excel File) Estadística Operativa de Aeropuertos / Statistics by Airport 2006-2026"
#
# y guárdalo como:
#
#   data/afac_aeropuertos_2006_2026.xlsx
#
echo "AFAC: descarga manual (ver comentario en este script)."
