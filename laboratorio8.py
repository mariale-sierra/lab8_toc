
from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import matplotlib.pyplot as plt

N_VALUES = [1, 10, 100, 1000, 10000, 100000, 1000000]
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "resultados"


def revisar_plazo(plazo: float | None) -> None:
    if plazo is not None and time.perf_counter() >= plazo:
        raise TiempoAgotado


def ejercicio_1(n: int, plazo: float | None = None) -> int:
    counter = 0
    for i in range(n // 2, n + 1):
        for j in range(1, n - n // 2 + 1):
            k = 1
            while k <= n:
                revisar_plazo(plazo)
                counter += 1
                k *= 2
    return counter


def ejercicio_2(n: int, emitir: bool = False, plazo: float | None = None) -> int:
    contador = 0
    for _ in range(1, n + 1):
        revisar_plazo(plazo)
        for _ in range(1, n + 1):
            contador += 1
            if emitir:
                print("Sequence")
            break
    return contador


def ejercicio_3(n: int, emitir: bool = False, plazo: float | None = None) -> int:
    contador = 0
    for _ in range(1, n // 3 + 1):
        for _ in range(1, n + 1, 4):
            revisar_plazo(plazo)
            contador += 1
            if emitir:
                print("Sequence")
    return contador


def operaciones_teoricas(ejercicio: int, n: int) -> int:
    if ejercicio == 1:
        return (n - n // 2 + 1) * (n - n // 2) * (n.bit_length())
    if ejercicio == 2:
        return n
    if ejercicio == 3:
        return (n // 3) * ((n - 1) // 4 + 1)
    raise ValueError(ejercicio)


class TiempoAgotado(Exception):
    pass


def medir(ejercicio: int, n: int, timeout: float) -> tuple[str, int | None]:
    """Devuelve (estado, microsegundos). timeout evita inputs impracticables."""
    inicio = time.perf_counter_ns()
    plazo = time.perf_counter() + timeout
    try:
        if ejercicio == 1:
            ejercicio_1(n, plazo)
        elif ejercicio == 2:
            ejercicio_2(n, emitir=False, plazo=plazo)
        else:
            ejercicio_3(n, emitir=False, plazo=plazo)
        micros = (time.perf_counter_ns() - inicio) // 1000
        return "medido", micros
    except TiempoAgotado:
        return "timeout", None


def ejecutar(ejercicio: int, timeout: float) -> None:
    OUT.mkdir(exist_ok=True)
    filas = []
    for n in N_VALUES:
        estado, micros = medir(ejercicio, n, timeout)
        teoricas = operaciones_teoricas(ejercicio, n)
        filas.append({
            "n": n,
            "estado": estado,
            "tiempo_microsegundos": "" if micros is None else micros,
            "operaciones_teoricas": teoricas,
        })
        valor = "--" if micros is None else f"{micros} us"
        print(f"Ejercicio {ejercicio}, n={n}: {estado}, tiempo={valor}, teoricas={teoricas}")

    csv_path = OUT / f"ejercicio_{ejercicio}_resultados.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=filas[0].keys())
        writer.writeheader()
        writer.writerows(filas)

    medidos = [(r["n"], r["tiempo_microsegundos"]) for r in filas if r["tiempo_microsegundos"]]
    plt.figure(figsize=(8, 5))
    if medidos:
        plt.loglog([x for x, _ in medidos], [int(y) for _, y in medidos], "o-", label="Tiempo medido")
    plt.loglog(N_VALUES, [operaciones_teoricas(ejercicio, n) for n in N_VALUES], "--", label="Operaciones teóricas")
    plt.xlabel("Tamaño de entrada n")
    plt.ylabel("Tiempo (microsegundos) / operaciones")
    plt.title(f"Ejercicio {ejercicio}: tamaño de entrada vs. crecimiento")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / f"ejercicio_{ejercicio}_grafica.png", dpi=160)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--ejercicio", type=int, choices=[1, 2, 3])
    grupo.add_argument("--todos", action="store_true")
    parser.add_argument("--timeout", type=float, default=2.0,
                        help="segundos máximos por tamaño (por defecto: 2)")
    args = parser.parse_args()
    ejercicios = [1, 2, 3] if args.todos else [args.ejercicio]
    for ejercicio in ejercicios:
        ejecutar(ejercicio, args.timeout)


if __name__ == "__main__":
    main()
