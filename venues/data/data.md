# data/

## Información estática
La información "estática" es la información que no cambia a lo largo del tiempo.

### venue_data_scrap.csv
Contiene información "estática" (invariante en el tiempo) acerca de los recintos.\
Información obtenida de: https://www.proyectomire.org/

- `name`: nombre del recinto
- `town`: localidad en la que se encuentra el recinto
- `latitude`: latitud geográfica del recinto
- `longitude`: longitud geográfica del recinto
- `capacity`: aforo máximo del recinto
- `roofed`: indica si el recinto está techado o no
<!-- - `avg_cost`: coste medio del alquiler diario del recinto -->

### town_data_scrap.csv
Contiene información "estática" (invariante en el tiempo) acerca de las localidades.\
Información obtenida de: https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n

- `town`: nombre de la localidad
- `population`: número de habitantes del municipio
<!-- - `connection`: valor del 1 al 10 de lo comunicada que está la localidad con otras (1: poco comunicado) (10: muy bien comunicado) -->

### fuse.py
Combina la información de estas dos tablas en una única tabla.

## Información dinámica
La información "dinámica" es la información que sí cambia a lo largo del tiempo

- `availability`: disponibilidad del recinto
- `cost`: coste del alquiler del recinto
- `weather`: clima esperado para cierto día
- `fans`: número de (oyentes diarios en spotify?) del artista en cada localidad
- `weekday`: especifica el día de la semana.
<!-- - `expected_attendance`: cantidad de personas que esperamos que puedan ir -->
<!-- - `connectivity`: cómo de fácil es viajar a cierta localidad -->
### Información independiente
Los valores de estas variables no están condicionadas por los valores de ninguna otra variable:
`weekday`

### Información dependiente
Los valores de estas variables sí están condicionadas por los valores de alguna de las otras variables.\
Esto se utiliza para la generación de datos (simulador).

`cost` $\propto$ `population`, `capacity`, `weekday`, `roofed`\
`weather`$\propto$ `weather` (autocorrelación temporal. El clima de mañana es parecido al de hoy)\
`fans` $\propto$ `population`\
`availability` $\propto$ `cost`$^{-1}$, `weekday`, `weather`*`roofed` (Estar techado es sólo relevante si se esperan precipitaciones)

