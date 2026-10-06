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
