"""Graficas del proyecto HPC. Se generan con codigo y se guardan en resultados/."""
import os

import matplotlib.pyplot as plt

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")


def _guardar_y_mostrar(nombre):
    os.makedirs(CARPETA, exist_ok=True)
    plt.savefig(os.path.join(CARPETA, nombre), dpi=150, bbox_inches="tight")
    plt.show()


def grafica_tiempo(workers, tiempos):
    plt.figure()
    plt.plot(workers, tiempos, marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Workers vs. tiempo de ejecución")
    plt.xticks(workers)
    plt.grid(True)
    _guardar_y_mostrar("workers_vs_tiempo.png")


def grafica_speedup(workers, speedups):
    plt.figure()
    plt.plot(workers, speedups, marker="o", label="Speedup real")
    plt.plot(workers, workers, linestyle="--", label="Speedup ideal")
    plt.xlabel("Número de workers")
    plt.ylabel("Speedup")
    plt.title("Workers vs. speedup")
    plt.xticks(workers)
    plt.legend()
    plt.grid(True)
    _guardar_y_mostrar("workers_vs_speedup.png")


def grafica_eficiencia(workers, eficiencias):
    plt.figure()
    plt.plot(workers, eficiencias, marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Eficiencia")
    plt.title("Workers vs. eficiencia")
    plt.xticks(workers)
    plt.ylim(0, 1.1)
    plt.grid(True)
    _guardar_y_mostrar("workers_vs_eficiencia.png")
