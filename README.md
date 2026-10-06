# Proyecto Práctico HPC: ejecución secuencial vs paralela

## Integrantes
- Angel Dolores Galván de la Cruz (@galvandelacruzangeldolores)
- Pamela (@pamela-mtz)
- Rosa (@rosa1208)

## ¿De qué trata?
Hicimos un programa en Python que procesa 5,000,000 de datos (x = 1 hasta N) aplicando la función f(x) = raíz(x) + x² + sin(x) + cos(x) + log(x) y suma todos los resultados. Lo hicimos de dos formas: una secuencial y una paralela con multiprocessing.Pool, que reparte el rango en bloques y se los da a los workers. Medimos el tiempo con time.perf_counter(), probamos con 1, 2 y 4 workers y cada configuración se corrió 3 veces.

## Cómo correrlo
pip install -r requirements.txt
python src/benchmark.py

## Hardware usado
- Procesador:
- Núcleos / hilos:
- RAM:
- Sistema operativo:
- Versión de Python:

## Resultados

| Workers | Prueba 1 (s) | Prueba 2 (s) | Prueba 3 (s) | Promedio (s) | Speedup | Eficiencia |
|---|---|---|---|---|---|---|
| 1 | | | | | 1.00 | 1.00 |
| 2 | | | | | | |
| 4 | | | | | | |

## Análisis de resultados
1. ¿La ejecución paralela fue más rápida que la secuencial?
2. ¿Qué número de workers obtuvo el menor tiempo?
3. ¿Duplicar el número de workers duplicó el rendimiento? ¿Por qué?
4. ¿Por qué el problema seleccionado puede paralelizarse?
5. ¿En qué momento agregar más workers deja de ser beneficioso?
6. ¿Qué limitaciones tiene el hardware utilizado?
7. ¿Este experimento representa HPC o solo demuestra principios utilizados en HPC? Justifiquen.

## ¿Qué es GitFlow?
GitFlow es una forma de organizar las ramas de un repositorio. main tiene la versión estable, develop es donde se junta todo lo que se va terminando, y cada tarea nueva se hace en su propia rama feature/... Cuando una feature está lista se abre un Pull Request hacia develop, otro integrante la revisa, y ya que develop está probado se abre otro Pull Request hacia main.
