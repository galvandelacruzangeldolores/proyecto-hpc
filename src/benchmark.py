"""
Proyecto HPC - Comparación secuencial vs paralelo.

Función que se evalúa:
    f(x) = sqrt(x) + x^2 + sin(x) + cos(x) + log(x)

Se aplica a N valores (x = 1 ... N) y se suman los resultados.
La versión paralela divide el rango en bloques (chunks) y los reparte
entre varios workers usando multiprocessing.Pool.
"""

import csv
import math
import os
import statistics
import sys
import time
from multiprocessing import Pool, cpu_count

import matplotlib

matplotlib.use("Agg")  # para guardar las gráficas sin abrir ventana
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- config
N = 5_000_000              # cantidad de datos a procesar
WORKERS = [1, 2, 4]        # configuraciones pedidas como mínimo
REPETICIONES = 3           # cada configuración se corre 3 veces
CHUNKS_POR_WORKER = 8      # bloques por worker (reparte mejor la carga)
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")


# ---------------------------------------------------------------- lógica
def f(x):
    return math.sqrt(x) + x ** 2 + math.sin(x) + math.cos(x) + math.log(x)


def procesar_bloque(rango):
    """Procesa un bloque [inicio, fin) y regresa la suma de f(x)."""
    inicio, fin = rango
    total = 0.0
    for x in range(inicio, fin):
        total += f(x)
    return total


def version_secuencial(n):
    return procesar_bloque((1, n + 1))


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


def version_paralela(n, workers):
    bloques = dividir_en_bloques(n, workers * CHUNKS_POR_WORKER)
    with Pool(processes=workers) as pool:
        parciales = pool.map(procesar_bloque, bloques)
    return sum(parciales)


# ---------------------------------------------------------------- medición
def medir(funcion, *args):
    t0 = time.perf_counter()
    resultado = funcion(*args)
    t1 = time.perf_counter()
    return t1 - t0, resultado


def main():
    print(f"CPUs detectados: {cpu_count()} | N = {N:,}")
    print("-" * 50)

    # Resultado de referencia para validar que el paralelo da lo mismo
    _, referencia = medir(version_secuencial, N)

    filas = []  # (version, workers, corrida, tiempo)

    # --- secuencial (línea base extra)
    for i in range(1, REPETICIONES + 1):
        t, r = medir(version_secuencial, N)
        filas.append(("secuencial", 0, i, t))
        print(f"secuencial        corrida {i}: {t:.4f} s")

    # --- paralelo con 1, 2 y 4 workers
    for w in WORKERS:
        for i in range(1, REPETICIONES + 1):
            t, r = medir(version_paralela, N, w)
            ok = math.isclose(r, referencia, rel_tol=1e-9)
            filas.append(("paralelo", w, i, t))
            print(f"paralelo {w} worker(s) corrida {i}: {t:.4f} s | resultado correcto: {ok}")

    # --- promedios, speedup y eficiencia
    prom_seq = statistics.mean(t for v, w, i, t in filas if v == "secuencial")
    prom = {w: statistics.mean(t for v, ww, i, t in filas if v == "paralelo" and ww == w)
            for w in WORKERS}
    T1 = prom[1]
    speedup = {w: T1 / prom[w] for w in WORKERS}
    eficiencia = {w: speedup[w] / w for w in WORKERS}

    print("-" * 50)
    print(f"Tiempo promedio secuencial: {prom_seq:.4f} s")
    print(f"{'workers':>8} {'promedio(s)':>12} {'speedup':>9} {'eficiencia':>11}")
    for w in WORKERS:
        print(f"{w:>8} {prom[w]:>12.4f} {speedup[w]:>9.3f} {eficiencia[w]:>11.3f}")

    guardar_csv(filas, prom, speedup, eficiencia, prom_seq)
    graficar(prom, speedup, eficiencia)
    print("\nListo. Revisa la carpeta 'resultados/'.")


# ---------------------------------------------------------------- salida
def guardar_csv(filas, prom, speedup, eficiencia, prom_seq):
    os.makedirs(CARPETA, exist_ok=True)
    with open(os.path.join(CARPETA, "tiempos_crudos.csv"), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["version", "workers", "corrida", "tiempo_s"])
        wr.writerows([(v, w, i, f"{t:.6f}") for v, w, i, t in filas])

    with open(os.path.join(CARPETA, "resumen.csv"), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["workers", "tiempo_promedio_s", "speedup", "eficiencia"])
        for w in prom:
            wr.writerow([w, f"{prom[w]:.6f}", f"{speedup[w]:.4f}", f"{eficiencia[w]:.4f}"])
        wr.writerow(["secuencial", f"{prom_seq:.6f}", "", ""])


def graficar(prom, speedup, eficiencia):
    os.makedirs(CARPETA, exist_ok=True)
    ws = list(prom.keys())

    plt.figure()
    plt.plot(ws, [prom[w] for w in ws], marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Workers vs. tiempo de ejecución")
    plt.xticks(ws)
    plt.grid(True)
    plt.savefig(os.path.join(CARPETA, "workers_vs_tiempo.png"), dpi=150, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(ws, [speedup[w] for w in ws], marker="o", label="Speedup real")
    plt.plot(ws, ws, linestyle="--", label="Speedup ideal")
    plt.xlabel("Número de workers")
    plt.ylabel("Speedup")
    plt.title("Workers vs. speedup")
    plt.xticks(ws)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(CARPETA, "workers_vs_speedup.png"), dpi=150, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(ws, [eficiencia[w] for w in ws], marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Eficiencia")
    plt.title("Workers vs. eficiencia")
    plt.xticks(ws)
    plt.ylim(0, 1.1)
    plt.grid(True)
    plt.savefig(os.path.join(CARPETA, "workers_vs_eficiencia.png"), dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        N = int(sys.argv[1])  # opcional: python benchmark.py 1000000
    main()
