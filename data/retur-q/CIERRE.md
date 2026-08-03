# CIERRE DEL FRENTE · RETUR-Q · anfitriones de Solidaridad

**Frente cerrado el 22 de julio de 2026.** Este documento se escribió el **2 de agosto de 2026**, al
inventariar la carpeta, para dejar por escrito lo que hasta entonces solo se deducía del manifiesto.

---

## El objetivo

Obtener, **por cada anfitrión registrado en Solidaridad**, tres campos:

- **colonia**
- **código postal**
- **número de unidades o habitaciones**

**Para qué:** alimentar el **índice de vivienda temporal (STR)**. Sin domicilio a nivel colonia o CP,
los registros oficiales no se pueden georreferenciar, y sin unidades no se puede medir capacidad. Los
tres campos juntos eran lo que convertía el padrón en numerador utilizable.

## El resultado: no existen en la capa pública

**Ninguno de los tres campos está disponible sin autenticación.** Verificado por dos vías, ambas
documentadas en esta carpeta.

**1. El catálogo público** (`siturq.gob.mx/catalogo-oficial`). Cada ficha expone únicamente nombre,
categoría, teléfono, correo, horario y algunos distintivos. **No hay ficha de detalle**: el enlace del
nombre es `href="#"` y no abre nada. El portal **no ofrece descarga estructurada**; su botón
"Opciones" solo exporta la vista a JPG o PDF. Detalle en `MANIFIESTO.txt`.

**2. El back-office** (`retur-q.siturq.gob.mx`). Se enumeraron endpoints con GET y sin credenciales.
**Todo el panel está detrás de `/login`**; `/home` y `/api/user` responden 302, y una veintena de rutas
candidatas responden 404. **No se encontró ningún endpoint público que devuelva domicilio o unidades.**
Detalle en `RECON_backoffice.txt`.

> **El hallazgo que sí quedó, y vale por sí solo:** el sistema **sí captura** los campos de domicilio.
> El JS de registro maneja un objeto `dataSATQ` con calle, número, colonia, CP, localidad y municipio,
> poblado por validación contra el SAT a partir del RFC del solicitante. **Los datos existen en el
> modelo; lo que no existe es acceso público a ellos.** De "número de unidades" no apareció rastro ni
> siquiera ahí: si existe, vive en el paso autenticado del alta.

**Alcance del reconocimiento, dicho con precisión:** solo GET, con encabezados de navegador estándar,
**sin enviar credenciales ni formularios**. Fue enumeración de superficie pública, no intrusión.

## Lo que sí se obtuvo, y sirve

La extracción **está completa y es utilizable para otra cosa**: **224 registros** de "Alojadores y
personas anfitrionas" en Solidaridad, con nombre, categoría, teléfono, correo, horario y municipio.
Siete de ocho columnas llenas al 100%; solo `horario` tiene huecos (195 de 224).

**Para qué sirve sin los tres campos faltantes:** para medir **la brecha de cumplimiento**. Contar
cuántos alojamientos están registrados oficialmente frente a cuántos operan en el mercado es una
medida por sí misma, y no necesita domicilio. Es el uso que ya le daba el script de `fase3-indice-ageb`
(ver §Reconciliación).

**Referencias de contexto capturadas el 22-jul:** 224 en Solidaridad · 984 en todo Quintana Roo ·
3,350 tarjetas en el catálogo completo.

## Qué reabriría el frente

**Una solicitud de transparencia a SEDETUR por el padrón completo del RETUR-Q, con domicilio y número
de unidades.**

Es la única vía que queda: los datos existen en el modelo del sistema y están en poder de la autoridad,
así que son información pública susceptible de solicitarse. Lo que hay que pedir es el padrón, no el
catálogo: **el catálogo es la vista pública recortada; el padrón es el registro.**

**Precedente que conviene mirar antes de redactar.** Ya hubo una solicitud a SEDETUR sobre este mismo
registro, folio **1411283200002526**, y su respuesta **remitió al portal siturq.gob.mx sin entregar lo
pedido**. Se recurrió: recurso de revisión **1413303700006026** ante el IQTP, con vencimiento
**17/08/2026**. Ambos viven en el expediente de solicitudes de
`~/pulse-promocion-scoping/data/solicitudes/`, frente "anfitriones".

> **Recomendación de secuencia:** **esperar la resolución del recurso antes de redactar la solicitud
> nueva.** Si el IQTP ordena a SEDETUR entregar la información estadística, esa resolución fija un
> criterio que hace más fuerte la petición del padrón con domicilio. Pedirlo antes, por separado,
> arriesga otra remisión al portal.

**Y una precaución de encuadre:** el domicilio de personas físicas anfitrionas puede clasificarse como
dato personal. Conviene pedir **desde el inicio** la versión pública con desglose por colonia o por
código postal en forma agregada, que es información estadística y no identifica a nadie, en vez de
pedir el domicilio individual y arriesgar una negativa total.

---

## Reconciliación · el RETUR-Q vive en tres lugares

| Ubicación | Fecha | Qué es | Estatus |
|---|---|---|---|
| **`~/serie-trafico-aereo/data/retur-q/`** | 22-jul-2026 | HTML crudo íntegro (3,350 tarjetas) + 224 registros filtrados en CSV y JSON + manifiesto + reconocimiento + checksums | **CANÓNICA** |
| `~/fase3-indice-ageb/` | 12-jul-2026 | `scripts/02_returq_catalogo.py` y `output/returq_catalogo.csv` con **3,264 registros**, 4 columnas (id, nombre, municipio, categoría) | **Captura anterior.** Superada |
| `~/indice-str-solidaridad/scripts/` | 14-jul-2026 | `02_returq_catalogo.py`, **byte-idéntico** al de fase3 (SHA256 `60e0c46d…`) | **Copia del script.** Nunca se ejecutó ahí: no hay `output/returq_catalogo.csv` |

**Por qué esta carpeta es la canónica.** Es la única que conserva el **HTML crudo** como fuente de
verdad, la única con **manifiesto de método**, la única con **checksums**, la única que documenta la
**ausencia** de los campos buscados, y la única que trae el **reconocimiento del back-office**. Las
otras dos son un script y su salida.

**Qué son las otras dos, y qué hacer con ellas.** El CSV de `fase3-indice-ageb` es una captura del
**12 de julio** de todo el catálogo, con menos columnas. **No es un error ni un duplicado: es un corte
anterior**, y como tal tiene valor de serie.

> **Dato que sale de compararlas:** el catálogo pasó de **3,264 tarjetas el 12 de julio** a **3,350 el
> 22 de julio**. **86 altas en diez días** [derivado]. No se verificó si son altas nuevas o
> reclasificaciones, pero la comparación es posible porque las dos capturas se conservan.

**No se consolidan ni se borran.** Cada una vive en el repo de su propio proyecto y ahí tiene sentido.
Lo que faltaba era decir cuál manda, y esta nota lo dice.

---

## ⚠️ Dónde vive este material, y por qué

**El conjunto de datos contiene datos personales y por eso vive en un repositorio PRIVADO.**

Los 224 registros extraídos traen **teléfono y correo electrónico de cada prestador**, y **91 de esos
correos son de dominios personales** (gmail, hotmail, live, outlook). Son personas físicas anfitrionas,
no razones sociales. El **HTML crudo contiene lo mismo** para las 3,350 fichas del catálogo completo.

**Que el dato esté publicado en un portal oficial no lo vuelve republicable.** Una cosa es una ficha
consultable de una en una en un sitio de gobierno, y otra es un conjunto estructurado y descargable de
224 contactos en un repositorio público con fork externo activo. La segunda forma habilita usos que la
primera no: extracción masiva, correo no solicitado, cruces. **Es una diferencia de naturaleza, no de
grado.**

**Decisión, tomada el 2 de agosto de 2026:**

| Qué | Dónde |
|---|---|
| `retur-q_catalogo-oficial_RAW.html`, `.csv`, `.json` | **Repositorio PRIVADO** |
| `CIERRE.md`, `MANIFIESTO.txt`, `RECON_backoffice.txt`, `CHECKSUMS.sha256` | Repositorio público. **Es documentación: no contiene un solo dato personal** |

**Verificado antes de decidir:** este material **nunca estuvo** en el historial del repositorio
público. Comprobado por ruta, por recorrido completo del historial y por búsqueda de contenido con
`git log -S` sobre tres cadenas distintas: cero apariciones en las tres. **No hubo que purgar nada.**

**Las otras dos ubicaciones del RETUR-Q no tienen este problema.** Sus archivos guardan cuatro columnas
(id, nombre, municipio, categoría) y **ningún dato de contacto**; el script del repositorio público solo
extrae esos cuatro campos. Ver la sección de reconciliación.

> **Regla que queda para este proyecto:** antes de versionar cualquier extracción de un padrón, **contar
> las columnas de contacto y de domicilio**. Si hay teléfono, correo o dirección de personas físicas, el
> conjunto va a repositorio privado y al público solo va la documentación del método. La regla es del
> conjunto, no del archivo: si el HTML crudo trae lo que el CSV recortó, los dos van al privado.

---

## Nota sobre los checksums

`CHECKSUMS.sha256` cubre **los tres archivos de datos y los tres documentos de texto**, incluido este.

**No se cubre a sí mismo, y no puede.** Un archivo de checksums que contuviera su propio hash sería
imposible de construir: escribir el hash dentro cambia el archivo y por tanto invalida el hash. Es
circular por definición, no una omisión.

**Lo que garantiza su integridad es git.** Desde el 2 de agosto de 2026 esta carpeta está versionada y
con respaldo en el remoto, así que cualquier alteración de `CHECKSUMS.sha256` queda registrada en el
historial. **Antes de eso, esta carpeta era la única copia y no estaba versionada**: existía solo en el
disco local, sin respaldo.
