# Metodología
El ejercicio de graficar, estimar los datos faltantes y realizar la predicción de datos se aplicará para las elecciones generales del 2020. Los pasos más relevantes son:

Obtención de la localización de los recintos (coordenadas)
Cruce de información de total de personas habilitadas por mesa y recinto electoral con la localización de los recintos (georeferenciación)
Se elaboró el código para representar cartografía de la base de datos consolidada
Se elaboró un primer producto con el programa CART donde se representa cada recinto y votos en un cartograma que permitió mostrar una distribución espacial constante de la densidad de los recintos (se aplica un filtro para normalizar la distribución). Así, las ciudades y las áreas dispersas están igualmente representadas en el gráfico en función de la densidad.
En cuanto al indicador en observación (diferencia porcentual de votos entre MAS y CC), se completarán los datos de los recintos faltantes mediante una interpolación. Se empleará el método de interpolación por triangulación cuando los datos lo permitan y el método de vecino más cercano el los casos restantes.
Posteriormente, se comparará la evolución temporal y espacial del conteo de votos del cómputo oficial.
Finalmente, se realizará un modelo predictivo de los resultados posibles en base a los datos del cómputo oficial a medida que vayan siendo disponibles. 
