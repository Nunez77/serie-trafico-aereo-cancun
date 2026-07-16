#!/usr/bin/env bash
# Descarga el workbook oficial de trafico de pasajeros de ASUR (fuente primaria).
# No se redistribuye en el repo; se obtiene de la fuente para reproducir el pipeline.
set -euo pipefail
mkdir -p data
URL="https://www.asur.com.mx/media/Inversionistas/Trafico%20de%20pasajeros/Trafico_de_pasajeros_ASUR.xlsx"
curl -fSL -A "Mozilla/5.0" -o data/Trafico_de_pasajeros_ASUR.xlsx "$URL"
echo "OK: data/Trafico_de_pasajeros_ASUR.xlsx"
