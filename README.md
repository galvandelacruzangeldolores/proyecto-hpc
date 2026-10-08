- Angel Dolores Galván de la Cruz (@galvandelacruzangeldolores)
- Pamela (@pamela-mtz)
- Rosa (@rosa1208)

## ¿De qué trata?
Hicimos un programa en Python que procesa 5,000,000 de datos (x = 1 hasta N) aplicando la función f(x) = raíz(x) + x² + sin(x) + cos(x) + log(x) y suma todos los resultados.

Lo hicimos de dos formas: una secuencial y una paralela con multiprocessing.Pool, que reparte el rango en bloques y se los da a los workers.

Medimos el tiempo con time.perf_counter(), probamos con 1, 2 y 4 workers y cada configuración se corrió 3 veces.

## Cómo correrlo

```bash
pip install -r requirements.txt
python src/benchmark.py

Hardware usado
- Procesador: Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz
- Núcleos / hilos: 8 hilos
- RAM: 15 GiB
- Sistema operativo: Ubuntu 24.04.5 LTS
- Versión de Python: 3.12.3
Resultados
La versión secuencial obtuvo los siguientes tiempos:
- Prueba 1: 1.7837 s
- Prueba 2: 1.9089 s
- Prueba 3: 1.7718 s
- Tiempo promedio: 1.8215 s
Los resultados de la ejecución paralela fueron:
Workers	Prueba 1 (s)	Prueba 2 (s)	Prueba 3 (s)	Promedio (s)	Speedup	Eficiencia
1	1.8227	1.7762	1.7740	1.7910	1.0000	100.00%
2	0.9479	0.9683	0.9587	0.9583	1.8689	93.45%
4	0.5147	0.5030	0.5126	0.5101	3.5111	87.78%


Los resultados completos también se guardan automáticamente en la carpeta resultados/.
Gráficas
El programa genera automáticamente tres gráficas:
Workers vs tiempo de ejecución

Workers vs speedup

Workers vs eficiencia

Análisis de resultados
1. ¿La ejecución paralela fue más rápida que la secuencial?
Sí. La versión secuencial obtuvo un promedio de 1.8215 segundos. Al utilizar 2 workers el tiempo bajó a 0.9583 segundos y con 4 workers disminuyó hasta 0.5101 segundos. Esto muestra que dividir el trabajo entre varios procesos mejoró el tiempo de ejecución.
2. ¿Qué número de workers obtuvo el menor tiempo?
La configuración de 4 workers obtuvo el menor tiempo, con un promedio de 0.5101 segundos.
3. ¿Duplicar el número de workers duplicó el rendimiento? ¿Por qué?
No exactamente. Con 2 workers obtuvimos un speedup de 1.8689 y con 4 workers un speedup de 3.5111. El rendimiento aumentó bastante, pero no de forma completamente proporcional.
Esto ocurre porque el paralelismo también tiene un costo. Se deben crear procesos, repartir los bloques de datos, coordinar los workers y juntar los resultados.
4. ¿Por qué el problema seleccionado puede paralelizarse?
Porque el cálculo realizado para cada valor de x es independiente de los demás. Un worker puede procesar una parte de los números mientras los otros procesan diferentes partes al mismo tiempo.
Al final solamente se suman los resultados parciales.
5. ¿En qué momento agregar más workers deja de ser beneficioso?
Agregar workers deja de ser beneficioso cuando el costo de crear y coordinar más procesos es mayor que la mejora obtenida.
También depende de la cantidad de núcleos o hilos disponibles en el procesador. Si se utilizan demasiados procesos, estos tendrán que competir por los mismos recursos del equipo.
6. ¿Qué limitaciones tiene el hardware utilizado?
Las pruebas se realizaron en una computadora con un Intel Core i7-7700HQ y 8 hilos.
Esto limita la cantidad de procesos que realmente pueden trabajar de manera simultánea. También influyen la memoria RAM, el sistema operativo y otros procesos que estén ejecutándose durante las pruebas.
Por esta razón los tiempos pueden variar ligeramente entre una ejecución y otra.
7. ¿Este experimento representa HPC o solo demuestra principios utilizados en HPC?
Este experimento demuestra principios utilizados en HPC, principalmente el procesamiento paralelo, la distribución del trabajo, la medición del rendimiento, el speedup y la eficiencia.
Sin embargo, no representa un sistema HPC a gran escala porque todas las pruebas se realizaron en una sola computadora. Un entorno HPC real puede utilizar muchos procesadores, múltiples nodos y sistemas distribuidos para resolver problemas mucho más grandes.
Conclusión
Los resultados muestran que el procesamiento paralelo permitió reducir considerablemente el tiempo de ejecución.
Con 1 worker el promedio fue de 1.7910 segundos, mientras que con 4 workers disminuyó a 0.5101 segundos, obteniendo un speedup de 3.5111.
También observamos que aumentar el número de workers no produce una mejora perfectamente proporcional, ya que existe un costo asociado con la creación y coordinación de los procesos.
¿Qué es GitFlow?
GitFlow es una forma de organizar las ramas de un repositorio. main tiene la versión estable, develop es donde se junta todo lo que se va terminando y cada tarea nueva se realiza en su propia rama feature/....
Cuando una feature está lista se abre un Pull Request hacia develop, otro integrante revisa los cambios y, cuando develop está completo y probado, se abre un Pull Request final hacia main.
