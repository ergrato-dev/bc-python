"""Ejercicio 02 · Tareas, errores y cancelación: TaskGroup, except*, timeout y cancel.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import asyncio
import time


async def read(station: str, seconds: float) -> str:
    """Simula la lectura de una estación que tarda `seconds` y avisa si la cancelan."""
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        print(f"  {station}: cancelada")
        raise  # Una tarea cancelada debe relanzar CancelledError, no tragárselo.
    return f"{station} ok"


async def broken(station: str, seconds: float) -> str:
    """Una estación que falla al cabo de `seconds`."""
    await asyncio.sleep(seconds)
    raise ValueError(f"{station}: lectura imposible")


print("Ejercicio 02 · Tareas, errores y cancelación")


# ============================================
# PASO 1: TaskGroup
# ============================================
# Descomenta las siguientes líneas:
# async def group_of_three() -> list[str]:
#     async with asyncio.TaskGroup() as group:
#         tasks = [group.create_task(read(name, 0.2)) for name in ["Norte", "Sur"]]
#         print(f"dentro del bloque: {sum(task.done() for task in tasks)} terminadas")
#     print(f"después del bloque: {sum(task.done() for task in tasks)} terminadas")
#     return [task.result() for task in tasks]
#
#
# print(f"TaskGroup: {asyncio.run(group_of_three())}")


# ============================================
# PASO 2: Un error cancela a las demás
# ============================================
# Descomenta las siguientes líneas:
# async def one_fails() -> None:
#     async with asyncio.TaskGroup() as group:
#         group.create_task(read("Norte", 1))
#         group.create_task(broken("Sur", 0.1))
#         group.create_task(read("Este", 1))
#
#
# start = time.perf_counter()
# try:
#     asyncio.run(one_fails())
# except* ValueError as errors:
#     print(f"ExceptionGroup con {len(errors.exceptions)} error: {errors.exceptions[0]}")
# print(f"tardó {time.perf_counter() - start:.1f} s, no 1 s")


# ============================================
# PASO 3: gather con return_exceptions
# ============================================
# Descomenta las siguientes líneas:
# async def keep_going() -> list[str | BaseException]:
#     jobs = [read("Norte", 0.1), broken("Sur", 0.1), read("Este", 0.1)]
#     return await asyncio.gather(*jobs, return_exceptions=True)
#
#
# for result in asyncio.run(keep_going()):
#     print(f"  {type(result).__name__}: {result}")


# ============================================
# PASO 4: Un tiempo máximo con timeout
# ============================================
# Descomenta las siguientes líneas:
# async def in_time(seconds: float) -> str:
#     async with asyncio.timeout(0.3):
#         return await read("Norte", seconds)
#
#
# print(f"a tiempo: {asyncio.run(in_time(0.1))}")
# try:
#     asyncio.run(in_time(5))
# except TimeoutError:
#     print("tarde: TimeoutError a los 0.3 s")


# ============================================
# PASO 5: Cancelar una tarea a mano
# ============================================
# Descomenta las siguientes líneas:
# async def cancel_one() -> None:
#     task = asyncio.create_task(read("Oriente", 5))
#     await asyncio.sleep(0.1)
#     print(f"cancel() devuelve {task.cancel()}")
#     try:
#         await task
#     except asyncio.CancelledError:
#         print(f"cancelled() = {task.cancelled()}")
#
#
# asyncio.run(cancel_one())


# ============================================
# PASO 6: as_completed, en orden de llegada
# ============================================
# Descomenta las siguientes líneas:
# async def first_come() -> None:
#     jobs = [read("lenta", 0.3), read("media", 0.2), read("rápida", 0.1)]
#     for next_result in asyncio.as_completed(jobs):
#         print(f"  llega {await next_result}")
#
#
# asyncio.run(first_come())


# ============================================
# PASO 7: Una tarea que se pierde
# ============================================
# Descomenta las siguientes líneas:
# async def forgotten() -> None:
#     asyncio.create_task(broken("Occidente", 0))
#     await asyncio.sleep(0.1)
#     print("la corrutina principal termina sin enterarse del error")
#
#
# asyncio.run(forgotten())
