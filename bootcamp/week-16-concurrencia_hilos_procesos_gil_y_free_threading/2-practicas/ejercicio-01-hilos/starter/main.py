"""Ejercicio 01 · Hilos: esperar a la vez, recoger resultados, carreras, Lock y Queue.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import queue
import threading
import time

# Cuatro "descargas" falsas: cada una espera medio segundo, como una lectura de red.
STATIONS = ["Norte", "Sur", "Oriente", "Occidente"]
DELAY = 0.5


def download(station: str) -> str:
    """Simula una lectura lenta: mientras duerme, el hilo no usa la CPU."""
    time.sleep(DELAY)
    return f"{station};{len(station) * 3.5:.1f}"


print("Ejercicio 01 · Hilos")


# ============================================
# PASO 1: Una detrás de otra
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# lines = [download(station) for station in STATIONS]
# print(f"secuencial: {time.perf_counter() - start:.1f} s · {lines[0]}")


# ============================================
# PASO 2: Un hilo por descarga
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# threads = [threading.Thread(target=download, args=(station,)) for station in STATIONS]
# for thread in threads:
#     thread.start()
# print(f"hilos vivos: {threading.active_count()}")
# for thread in threads:
#     thread.join()
# elapsed = time.perf_counter() - start
# print(f"4 hilos: {elapsed:.1f} s · vivos al final: {threading.active_count()}")


# ============================================
# PASO 3: Sin join, nadie espera
# ============================================
# Descomenta las siguientes líneas:
# def late() -> None:
#     time.sleep(0.2)
#     print(f"[{threading.current_thread().name}] terminé")
#
#
# thread = threading.Thread(target=late, name="lento")
# thread.start()
# print("el hilo principal sigue sin esperar")
# thread.join()
# print("después de join: el hilo ya terminó")


# ============================================
# PASO 4: Los resultados de cada hilo
# ============================================
# Descomenta las siguientes líneas:
# results: list[str | None] = [None] * len(STATIONS)
#
#
# def download_into(index: int, station: str) -> None:
#     # Cada hilo escribe solo en su casilla: ningún otro la toca.
#     results[index] = download(station)
#
#
# threads = [
#     threading.Thread(target=download_into, args=(index, station))
#     for index, station in enumerate(STATIONS)
# ]
# for thread in threads:
#     thread.start()
# for thread in threads:
#     thread.join()
# print(f"resultados: {results}")


# ============================================
# PASO 5: Una condición de carrera
# ============================================
# Descomenta las siguientes líneas:
# class Counter:
#     def __init__(self) -> None:
#         self.value = 0
#
#     def add(self) -> None:
#         current = self.value  # 1. leer
#         time.sleep(0)  # aquí otro hilo puede entrar (lo forzamos para verlo)
#         self.value = current + 1  # 2. escribir: pisa lo que otro escribió
#
#
# def count_many(counter: Counter) -> None:
#     for _ in range(100):
#         counter.add()
#
#
# counter = Counter()
# threads = [threading.Thread(target=count_many, args=(counter,)) for _ in range(4)]
# for thread in threads:
#     thread.start()
# for thread in threads:
#     thread.join()
# print(f"sin Lock: esperado 400 · obtenido {counter.value}")


# ============================================
# PASO 6: El Lock
# ============================================
# Descomenta las siguientes líneas:
# class SafeCounter(Counter):
#     def __init__(self) -> None:
#         super().__init__()
#         self.lock = threading.Lock()
#
#     def add(self) -> None:
#         # Solo un hilo a la vez ejecuta este bloque: leer y escribir ya no se separan.
#         with self.lock:
#             super().add()
#
#
# safe = SafeCounter()
# threads = [threading.Thread(target=count_many, args=(safe,)) for _ in range(4)]
# for thread in threads:
#     thread.start()
# for thread in threads:
#     thread.join()
# print(f"con Lock: esperado 400 · obtenido {safe.value}")


# ============================================
# PASO 7: Productor y consumidores con Queue
# ============================================
# Descomenta las siguientes líneas:
# tasks: queue.Queue[str | None] = queue.Queue()
# done: queue.Queue[str] = queue.Queue()  # Queue ya trae su propio Lock por dentro
#
#
# def worker() -> None:
#     while True:
#         station = tasks.get()  # espera hasta que haya algo
#         if station is None:  # la señal de parar
#             return
#         done.put(download(station))
#
#
# workers = [threading.Thread(target=worker, name=f"w{number}") for number in range(2)]
# for thread in workers:
#     thread.start()
# for station in STATIONS:
#     tasks.put(station)
# for _ in workers:
#     tasks.put(None)  # una señal de parar por cada consumidor
# for thread in workers:
#     thread.join()
# print(f"procesadas: {sorted(done.get() for _ in range(done.qsize()))}")
