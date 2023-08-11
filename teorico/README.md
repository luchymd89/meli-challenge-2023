# Desafío teórico
## Procesos, hilos y corrutinas
- Un caso en que usaría procesos para resolver un problema sería por ejemplo en un pago, dado que el orden de ejecución es importante y un resultado depende del anterior.
- Para un problema donde se esperen datos de entrada desde un dispositivo, como ser un teclado, usaría threds dado que la espera depende de la entrada.


## Optimización de recursos del sistema operativo
Para este caso usaría multiprocessing, aprovechando el paralelismo para ejecutar varios procesos al mismo tiempo, aprovechando los núcleos de la CPU. 



## Análisis de complejidad

- En orden de complejidad de menor a mayor los algoritmos se ordenarían
D, A, B y C
El que descartaría primero sería el algoritmo C dado que su orden de complejidad es exponencial, es decir la tasa de crecimiento (tiempo requerido para ejecutarse) crece de manera exponencial a medida que se aumenta n.
Con el que me quedaría es con el algoritmo D, dado que su complejidad es casi lineal, por lo que es mucho más eficiente en cuanto a tiempos de ejecución.

Los algoritmos A y B, tienen orden cuadrático y cúbico respectivamente.

- La base de datos AlfaDB la usaría la usaría unicamente en problemas que solo requieran consultas a los datos de la misma y no modificaciones (escrituras), dado que las modificaciones son demasiado costosas (orden exponencial).
- Para casos donde el uso de los datos va a ser tanto de consulta como de modificación pasaría a utilizar la base de datos BetaDB dado que promedialmente es más eficiente donde el orden para ambos casos es lineal. 
