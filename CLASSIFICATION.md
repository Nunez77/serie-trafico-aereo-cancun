# Clasificación de los 68 aeropuertos: playa vs no playa

Esta clasificación es **nuestra**, no de la fuente. La AFAC no cataloga sus
aeropuertos por tipo de destino; agrupamos los 68 para poder medir si la caída
del tráfico de la Riviera Maya es un fenómeno del país, de la playa mexicana o
de la Riviera en específico. Se publica completa para que cualquiera la discuta
o la rehaga con otro criterio.

## Criterio declarado

**"Playa"** = aeropuerto cuyo mercado dominante es el turismo de ocio sol y playa
(destino de resort costero). Una ciudad costera cuyo aeropuerto sirve
principalmente tráfico urbano, de negocios, de gobierno o fronterizo **no** es
playa (por ejemplo Mérida, Veracruz, Tijuana, Campeche, Ciudad del Carmen).

**"No playa"** = todo lo demás: hubs urbanos, capitales, ciudades de negocios,
fronterizos, industriales, petroleros y regionales.

## Grupo PLAYA (14)

Acapulco, Cancún, Cozumel, Huatulco, La Paz, Loreto, Manzanillo, Mazatlán,
Puerto Escondido, Puerto Peñasco, Puerto Vallarta, San José del Cabo (Los Cabos),
Tulum, Zihuatanejo.

## Grupo NO PLAYA (54)

Aguascalientes, Bajío, Campeche, Ciudad del Carmen, Ciudad Juárez, Ciudad Obregón,
Ciudad Victoria, Chetumal, Chichén Itzá, Chihuahua, Ciudad de México, Colima,
Creel, Cuernavaca, Culiacán, Del Norte, Durango, Guadalajara, Guaymas, Hermosillo,
Ixtepec, Los Mochis, Matamoros, Mérida, Mexicali, Minatitlán, Monterrey, Morelia,
Nogales, Nuevo Laredo, Oaxaca, Palenque, Poza Rica, Puebla, Querétaro, Reynosa,
San Cristóbal de las Casas, San Luis Potosí, Santa Lucía (AIFA), Tampico, Tamuín,
Tapachula, Tehuacán, Tepic, Terán, Tijuana, Toluca, Torreón,
Tuxtla Gutiérrez (Ángel Albino Corzo), Uruapan, Veracruz, Villahermosa, Zacatecas.

> La lista de arriba enumera **53 aeropuertos distintos**. La AFAC reporta la
> etiqueta "Chichén Itzá" **duplicada** (dos entradas en el pivot-cache), ambas
> en no playa y de volumen negligible, por lo que el conteo de entradas sobre el
> que agregan los scripts es **54**. De ahí "(54)".

## Casos discutibles

- **Mérida, Tijuana, Villahermosa** → **no playa.** Sirven principalmente tráfico
  urbano, fronterizo o de negocios. Tijuana en particular responde al puente
  fronterizo Cross Border Xpress hacia San Diego, no al turismo.
- **La Paz, Manzanillo, Acapulco** → **playa** (clasificación frágil, declarada).
  La Paz es capital de Baja California Sur pero su tráfico es mayoritariamente de
  turismo marino y de playa; Manzanillo es un gran puerto de carga pero su pasaje
  es de resort; Acapulco es playa clásica, deprimida por el huracán Otis
  (octubre de 2023).

## Robustez

El resultado agregado (la playa pierde en los dos mercados; lo no playa gana en
los dos) no depende de estos casos. Mover cualquiera de los discutibles solo
**agranda** la brecha. La reproducción está en `scripts/10_playa_vs_urbano_afac.py`.

"Riviera" se define aparte, como la suma de **Cancún + Tulum**, que sirven al
corredor Cancún-Tulum. Cozumel se cuenta como playa pero no como Riviera.

Fuente de los volúmenes: AFAC, Estadística Operativa de Aeropuertos. Corte:
julio de 2026 (acumulado enero a mayo para las comparaciones 2026 vs 2025).
