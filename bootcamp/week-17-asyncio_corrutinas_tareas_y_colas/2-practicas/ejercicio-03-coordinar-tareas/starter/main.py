"""Ejercicio 03 · Coordinar tareas: Semaphore, una carrera con await, Lock, Queue y Event.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import asyncio
import time

STATIONS = ["Norte", "Sur", "Oriente", "Occidente", "Centro", "Isla"]

print("Ejercicio 03 · Coordinar tareas")


# ============================================
# PASO 1: Semaphore, como mucho dos a la vez
# ============================================
# Descomenta las siguientes líneas:
# async def limited(limit: int) -> None:
#     semaphore = asyncio.Semaphore(limit)
#     active = 0
#     peak = 0
#
#     async def read(station: str) -> None:
#         nonlocal active, peak
#         async with semaphore:
#             active += 1
#             peak = max(peak, active)
#             await asyncio.sleep(0.2)
#             active -= 1
#
#     start = time.perf_counter()
#     async with asyncio.TaskGroup() as group:
#         for station in STATIONS:
#             group.create_task(read(station))
#     elapsed = time.perf_counter() - start
#     print(f"límite {limit}: a la vez como mucho {peak} · {elapsed:.1f} s")
#
#
# asyncio.run(limited(2))
# asyncio.run(limited(6))


# ============================================
# PASO 2: Una carrera en un solo hilo
# ============================================
# Descomenta las siguientes líneas:
# class Counter:
#     def __init__(self) -> None:
#         self.value = 0
#         self.lock = asyncio.Lock()
#
#     async def add(self) -> None:
#         current = self.value
#         await asyncio.sleep(0)  # Cualquier await en medio: otra tarea entra aquí.
#         self.value = current + 1
#
#     async def add_safely(self) -> None:
#         async with self.lock:
#             await self.add()
#
#
# async def count(safe: bool) -> int:
#     counter = Counter()
#     add = counter.add_safely if safe else counter.add
#     async with asyncio.TaskGroup() as group:
#         for _ in range(100):
#             group.create_task(add())
#     return counter.value
#
#
# print(f"sin Lock: esperado 100 · obtenido {asyncio.run(count(safe=False))}")


# ============================================
# PASO 3: asyncio.Lock
# ============================================
# Descomenta las siguientes líneas:
# print(f"con Lock: esperado 100 · obtenido {asyncio.run(count(safe=True))}")


# ============================================
# PASO 4: Productor y consumidor con Queue
# ============================================
# Descomenta las siguientes líneas:
# async def consumer(name: str, queue: asyncio.Queue[str], done: list[str]) -> None:
#     while True:
#         station = await queue.get()
#         await asyncio.sleep(0.1)
#         done.append(f"{name}:{station}")
#         queue.task_done()
#
#
# async def one_consumer() -> None:
#     queue: asyncio.Queue[str] = asyncio.Queue()
#     done: list[str] = []
#     for station in STATIONS[:3]:
#         queue.put_nowait(station)
#     worker = asyncio.create_task(consumer("c1", queue, done))
#     await queue.join()  # Espera a que cada elemento tenga su task_done().
#     worker.cancel()
#     print(f"un consumidor: {done}")
#
#
# asyncio.run(one_consumer())


# ============================================
# PASO 5: Varios consumidores y una cola con tope
# ============================================
# Descomenta las siguientes líneas:
# async def producer(queue: asyncio.Queue[str]) -> None:
#     for station in STATIONS:
#         await queue.put(station)  # Con la cola llena, espera a que haya sitio.
#         print(f"  pone {station} · en cola: {queue.qsize()}")
#
#
# async def many_consumers() -> None:
#     queue: asyncio.Queue[str] = asyncio.Queue(maxsize=2)
#     done: list[str] = []
#     start = time.perf_counter()
#     workers = [asyncio.create_task(consumer(f"c{n}", queue, done)) for n in range(3)]
#     await producer(queue)
#     await queue.join()
#     for worker in workers:
#         worker.cancel()
#     print(f"tres consumidores: {len(done)} en {time.perf_counter() - start:.1f} s")
#
#
# asyncio.run(many_consumers())


# ============================================
# PASO 6: Event, una señal para todas
# ============================================
# Descomenta las siguientes líneas:
# async def wait_for_start(name: str, start: asyncio.Event) -> None:
#     print(f"  {name} espera la señal")
#     await start.wait()
#     print(f"  {name} arranca")
#
#
# async def signal() -> None:
#     start = asyncio.Event()
#     async with asyncio.TaskGroup() as group:
#         for name in ["Norte", "Sur"]:
#             group.create_task(wait_for_start(name, start))
#         await asyncio.sleep(0.1)
#         print("señal")
#         start.set()
#
#
# asyncio.run(signal())


# ============================================
# PASO 7: Cerrar la cola con shutdown
# ============================================
# Descomenta las siguientes líneas:
# async def until_shutdown(name: str, queue: asyncio.Queue[str], done: list[str]) -> None:
#     try:
#         while True:
#             done.append(f"{name}:{await queue.get()}")
#     except asyncio.QueueShutDown:
#         print(f"  {name}: la cola está cerrada, termino")
#
#
# async def closing() -> None:
#     queue: asyncio.Queue[str] = asyncio.Queue()
#     done: list[str] = []
#     async with asyncio.TaskGroup() as group:
#         for n in range(2):
#             group.create_task(until_shutdown(f"c{n}", queue, done))
#         for station in STATIONS:
#             await queue.put(station)
#         queue.shutdown()  # Los get() siguen hasta vaciarla, y después fallan.
#     print(f"procesadas: {len(done)}")
#
#
# asyncio.run(closing())
