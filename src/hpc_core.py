"""
Funciones de calculo para el proyecto HPC (secuencial vs paralelo).

f(x) = sqrt(x) + x^2 + sin(x) + cos(x) + log(x)

Estan en un .py (y no en el notebook) para que multiprocessing funcione
tambien en Windows y Mac.
"""
import math
import time
from multiprocessing import Pool

CHUNKS_POR_WORKER = 8


def f(x):
    return math.sqrt(x) + x ** 2 + math.sin(x) + math.cos(x) + math.log(x)


def procesar_bloque(rango):
    """Suma f(x) para x en [inicio, fin)."""
    inicio, fin = rango
    total = 0.0
    for x in range(inicio, fin):
        total += f(x)
    return total


def dividir_en_bloques(n, cantidad):
    """Parte el rango 1..n en 'cantidad' bloques casi iguales."""
    tam = math.ceil(n / cantidad)
    bloques = []
    inicio = 1
    while inicio <= n:
        fin = min(inicio + tam, n + 1)
        bloques.append((inicio, fin))
        inicio = fin
    return bloques


def version_secuencial(n):
    return procesar_bloque((1, n + 1))


def version_paralela(n, workers):
    bloques = dividir_en_bloques(n, workers * CHUNKS_POR_WORKER)
    with Pool(processes=workers) as pool:
        parciales = pool.map(procesar_bloque, bloques)
    return sum(parciales)


def medir(funcion, *args):
    """Regresa (tiempo_en_segundos, resultado)."""
    t0 = time.perf_counter()
    resultado = funcion(*args)
    return time.perf_counter() - t0, resultado
