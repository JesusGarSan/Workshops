# Nombre del taller: Decisiones espacio-temporales

## Materiales
- Ordenador con la aplicación en ejecución
- Proyector para el ordenador
- Pizarra y utensilios de escritura
- Folios y fiso
- Rotuladores

## Etapa 0: Captación de interés
Queremos que el tema a tratar en el taller sea de interés para el público. Ya que el problema a plantear es la planificación de un evento, podemos jugar con aspectos como para qué artista será el evento.

Este taller se plantea altamente cooperativo con el público. Por tanto, es muy importante entablar covnersación con ellos desde el principio.

### Algunas estrategias:
- Exageración del personajes (modo payaso): Como "monitor" del taller queremos trasmitir energía al público, ser algo "payaso" si es necesario, y darle muchísima importancia a lo que estamos haciendo al mismo tiempo. "
- Intereses a medida: Si el público es suficientemente participativo de forma natural, se le puede preguntar acerca de sus gustos. Música favorita, artista favorito (No tiene por qué ser música)

## Etapa 1: Planteamiento del problema
El objetivo de esta etapa es plantear el problema que encauzará el taller de forma natural y "de a pie"

Problema: 
Somos agentes de un artista. Tenemos que organizar su siguiente espectáculo y queremos asegurarnos de que sea un exitazo. ¿Qué hacemos?

Habiendo planteado el problema, dejamos al público el tiempo que sea necesario para que empiecen a proponer ideas. 

Deliberando (con la ayuda del monitor si es necesario) llegaremos a la conclusión de que tenemos que tomar varias **decisiones** como:

- Decidir dónde hacer el concierto 
- Decidir cuándo realizar el concierto
- Decidir cuánto vamos a cobrar por la entrada

Nota: Si sólo se plantea uno de estos problemas, la colecta de información de después será incompleta (sólo será temporal o espacial, no espaciotemporal).

Tomar estas decisiones no es algo que podamos tomarnos a la ligera, al final y al cabo queremos que el evento sea un exitazo. Se hará evidente que para tomar estas decisiones tan importantes es necesario tener información.

## Etapa 2: Colecta de información
Los participantes se dan cuenta de que es difícil tomar decisiones sin información.

Entonces, tenemos que recolectar información.

¿Qué información vamos a recolectar? De nuevo, con ayuda del monitor si es necesario el público propondrá la información que le parece relevante para tomar estas decisiones. Algunas de las respuestas esperadas son:

- ¿Qué recintos hay disponibles? 
- ¿Están techados?
- ¿Cómo será el clima?
- ¿A qué ciudades podrá ir más gente?
- ¿A qué hora podrá ir más gente?
- ¿Cuánto cuesta alquilar el recinto?
- ¿Cuánto cobramos por la entrada?

Según se proponen ideas el monitor las escribirá en una pizarra en dos columnas distintas (sin indicar inicialmente por qué las separa). Una de las columnas representará información (variables $^1$ ) de carácter espacial y otra la información de carácter temporal. 

$^1$ Aunque lo que estemos recolectando sean propiamente "variables", evitaremos hacer uso de esta palabra para no "intimidar" al público. Nos podemos referir a cada una de las variables como "preguntas" o "dato".

## Etapa 3: Análisis de la información

Una vez se haya cofeccionado la lista de información importante por parte del público, el monitor les pregunta cómo proceder.

Supongamos que ya hemos recolectado toda esta información: ¿Qué hacemos con ella? ¿Cómo la utilizamos para decidir?

Una de las respuestas esperadas es un enfoque **univariante**. Es decir, centrarse en la información de una de las variables recogidas. Ideas como: "Vamos a hacer el evento en el sitio con mayor aforo", "Hagámoslo en la ciudad con más fans" o "Hagámoslo el día de la semana que más gente pueda ir".

Si esta es la respuesta que proponen, el monitor llamará la atención a que si hacemos eso, estamos descartando información que nosotros mismos hemos decidido que es importante.

Quedará claro entonces que no sirve con considerar sólo una de las variables.

Algún miembro del público puede proponer enfoques multivariantes. Ideas como: "Hagámoslo en el recinto más grande de la ciudad con más fans". Estas ideas están bien orientadas. Sin embargo, nos daremos cuenta de que son difíciles de implementar. Podemos, por ejemplo multiplicar el número de fans por el aforo de cada recinto y elegir el que tenga el número más grande. Utilizando enfoques de este tipo es difícil asimilar todas las variables, pero peor aun, estamos dándole una relevancia arbitraria a cada variable: ¿Por qué multiplicar y no sumar? ¿Restamos por el precio del recinto? ¿dividimos?.

Otra idea deseable es simplemente "vamos a ver la información que hemos recolectado".

#### Material auxiliar
Como material de este taller se ha creado una base de datos con información de carácter espacio temporal acerca de los diferentes recintos para eventos disponibles en España. Podemos apoyarnos en este material para ilustrar la discusión.

Por ejemplo, viendo la información en crudo podemos ver lo abrumante que puede ser la cantidad de información. Una visualización que ayude a entender es fundamental.


## Etapa 4: Revelando lo aprendido


## Notas

### Información estática vs. información dinámica
No todas las variables cambian su valor en el tiempo.

### Outliers
Puede ser interesante buscar generar outliers. Siempre y caudno podamos observarlos de forma clara y explicar a qué se deben. Por ejemplo, las islas canarias tendrán un coste de desplazamiento mayor.

### Multiescala
Este ejemplo es también de naturaleza multiescala. Espacialmente, nos podemos preguntar por en qué ciudad hacer el evento o en qué país. Temporalmente, podemos preguntarnos por la estación del año, mes semana dío u hora en la que hacer el concierto. Por simpleza, no haremos alusión a la naturaleza multiescala de este ejemplo. Sólo se mencionará como apunte al final si se valora que el público es receptivo ante este matiz.



### Notas Veracruz:
- El comienzo si puede ser del estilo: Plantear el problema, que sea de interés, captando la anteción, hablando hasta llegar a la conclusión de que tenemos que tomar dos decisiones: Dónde y Cuándo hacer el evento. Recoger la información interesante mediante la pizarra.

- La relación entre las variables está chula

- Debería guiar yo más

- Una vez decididas las variables, explicadas las posibles relaciones y los que son distribuidos en el tiempo y en el espacio pasamos al ordenador

- En el ordenador guio yo por completo. Puedo plantear una ruta interesante habiendo estudiado los datos antes. Por ejemplo:

    - Mostrar toda la información, que es abrumadora.

    - La mostramos en el mapa, es más asimilable, pero difícil de analizar.

    - Podemos estudiar la información por separado.

    - ¿Qué sitio es más barato? Resulta que el más barato es un pueblo perdido en el que a penas hay habitantes y no esperamos que vaya nadie.

    - Vamos entonces a ver en qué localidad tiene más fans. Dentro de la que más fans tiene miramos el sitio con mayor aforo. Seleccionamos el día que sea más barato. Nos encontramos que ese día está ocupado. Nos vamos a el día más barato que no está ocupado. Esta decisión posiblemente sea buena, pero no la mejor. Resulta que el día que este día es entre semana y se prevee mal tiempo, por lo que seguramente no pueda ir tanta gente.

    - Llegados hasta aquí, aunque sea "sacado de la manga", les planteo como mejor opción un recinto de la 2º ciudad con más fans, que resulta tener mucha mejor disponibilidad, de tal modo que a buen precio podemos encontrar un lugar con gran aforo en un día mejor. Esta respuesta es multivariante. Se ha obtenido considerando las diferentes variables y no una a una.


## Puntos a resaltar:
- 





