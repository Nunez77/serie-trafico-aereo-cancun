#!/usr/bin/env python3
"""Lee el HTML de la página de cuadros de UPM por stdin e imprime el href
relativo del Cuadro 1.3.1 del año dado (o vacío si no aparece). El nombre del
archivo varía por año (cuadro1.3.1_.xls en 2025, cuadro_1.3.1.xls en 2026), por
eso se extrae del HTML en vez de asumirlo. Robusto frente al quoting de bash.
Uso: curl ... | python3 _upm_href.py 2026"""
import sys, re
year = sys.argv[1] if len(sys.argv) > 1 else r"\d{4}"
# la página de UPM viene en Latin-1 (no UTF-8); latin-1 mapea los 256 bytes y no
# falla, y el href buscado es ASCII, así que se decodifica sin riesgo.
html = sys.stdin.buffer.read().decode("latin-1")
m = re.search(rf"Cuadros{year}/[^'\"]*1\.3\.1[^'\"]*\.xls", html, re.IGNORECASE)
print(m.group(0) if m else "")
