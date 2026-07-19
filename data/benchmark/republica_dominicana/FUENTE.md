# Benchmark Caribe: República Dominicana, lado LLEGADAS (Banco Central)

Fuente: Banco Central de la República Dominicana, Estadísticas > Sector Turismo >
Flujo turístico. https://www.bancentral.gov.do/a/d/2537-sector-turismo
Los enlaces no están en el HTML servido (SPA); el listado se obtiene de
`POST https://www.bancentral.gov.do/Home/GetContentForRender` con `id=2537`.
Descargado: 2026-07-19. Checksums en SHA256SUMS.txt.

## Universo (citado literal)

"LLEGADA MENSUAL DE PASAJEROS SEGÚN RESIDENCIA Y AEROPUERTO UTILIZADO, VÍA AÉREA".

Nota al pie del propio archivo: desde septiembre de 2021, tras la resolución
178-2021 de la JAC que hizo obligatorio el e-ticket, la compilación quedó a cargo
del MITUR, que suministra los datos al BCRD. Al pie de los gráficos del informe:
"Banco Central en base a los datos recibidos del Ministerio de Turismo (MITUR),
provenientes de la Dirección General de Migración (DGM)".
Las cifras vienen marcadas "sujetas a rectificación".

### Tres precisiones que definen el uso

1. Es **solo llegadas**, del registro migratorio. **NO se resta ni se combina** con
   la JAC (entradas más salidas, base IDAC) ni con AFAC o ASUR de México. Enero 2026
   ilustra la brecha: BCRD registra 945,866 llegadas contra el orden de 1.8 millones
   de pasajeros mensuales que reporta la JAC.
2. **Incluye dominicanos no residentes que regresan** (fila propia, 727,741 en
   enero-junio 2026) y también residentes en la fila TOTAL PASAJEROS.
3. **Tránsito: NO DECLARADO** en ninguna fuente primaria consultada. Queda como no
   confirmado; no se infiere.

### Estados Unidos: dos cifras no intercambiables

Por **residencia** (1,823,552 en enero-junio 2026) y por **nacionalidad**
(1,557,623). Para leer mercado emisor la correcta es residencia. El desglose por
país cuelga de "no residentes > extranjeros", así que **excluye a los dominicanos
no residentes**, muchos de los cuales viven en Estados Unidos.

## Corte y rezago

XLS hasta **junio 2026**, publicados el 2026-07-09. **Rezago de 9 días**, el más
corto de todo el scoping y por delante del compromiso oficial de 30 días.
El informe narrativo en PDF va un mes atrás; el de junio devuelve 404.

## Granularidad, y el cruce que importa

El desglose por país se repite **dentro de cada aeropuerto**, así que existe el
cruce **Estados Unidos por Punta Cana** mensual.

## Nota de calidad

Las celdas mensuales por aeropuerto traen decimales (por ejemplo 884.389), lo que
sugiere expansión o prorrateo y no conteo entero. La fuente no explica el método.
