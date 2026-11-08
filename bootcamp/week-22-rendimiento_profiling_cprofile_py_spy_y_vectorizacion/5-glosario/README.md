# Glosario — Semana 22

| Término | Definición |
|---|---|
| **Array (NumPy)** | Un bloque de memoria con números del mismo tipo seguidos, sin objetos de Python. `np.array(lista)` lo crea |
| **Arranque** | Lo que tarda un programa antes de hacer su trabajo, sobre todo en importar módulos. Se mide con `python -X importtime` |
| **`autorange`** | El método de `timeit.Timer` que prueba cuántas vueltas hacen falta para que la medida dure al menos 0,2 s |
| **Complejidad** | Cómo crece el tiempo con el tamaño de los datos: O(1), O(n), O(n²)... Se ve midiendo con dos o tres tamaños |
| **cProfile** | El perfilador determinista de la biblioteca estándar: anota cada llamada y cada retorno de función |
| **Cuello de botella** | La parte de un programa que más limita su velocidad. Arreglar otra cosa apenas se nota |
| **`cumsum`** | La suma acumulada de NumPy: en cada posición, la suma de todo lo anterior. Sirve para medias móviles sin bucle |
| **`cumtime`** | En cProfile, el tiempo acumulado de una función: desde que entra hasta que sale, con todo lo que llama |
| **Determinista (perfilador)** | Un perfilador que registra todas las llamadas. Es exacto en `ncalls`, pero frena el programa en cada una |
| **`dtype`** | El tipo de todos los elementos de un array, como `float64`: números de 8 bytes |
| **`dump` (py-spy)** | La orden de py-spy que escribe la pila de cada hilo de un proceso en ese instante. Sirve para programas colgados |
| ***Flaky*** | Un test que a veces falla sin que el código cambie, como uno con un límite de segundos |
| **Gráfico de llamas (*flame graph*)** | El dibujo de un perfil por muestreo: el ancho de cada función es la parte de las muestras en que estaba en la pila. El eje horizontal no es el tiempo |
| **`--idle`** | La opción de py-spy que cuenta también las muestras en que el programa espera |
| **Ley de Amdahl** | Acelerar una parte que ocupa una fracción `p` del tiempo nunca gana más que quitar esa `p` |
| **Máscara** | Un array de booleanos que sale de una comparación (`array > 50`). Sirve para contar y para filtrar |
| **Muestreo (perfilador)** | Un perfilador que mira la pila cada cierto tiempo y cuenta. Casi no frena el programa |
| **`ncalls`** | En cProfile, cuántas veces se llamó una función. Con `a/b`, `b` son las llamadas primitivas, que no vienen de la propia función |
| **`--nonblocking`** | La opción de py-spy que lee la pila sin pausar el programa. Algunas muestras salen rotas (`Errors`) |
| **Optimización prematura** | Hacer el código más rápido, y más difícil, antes de saber si hace falta y dónde |
| **`perf_counter`** | El reloj de `time` para medir duraciones: alta resolución, no salta si cambia la hora |
| **Perfil** | El registro de dónde se va el tiempo de un programa, función por función |
| **`process_time`** | El reloj de `time` que mide solo el tiempo de CPU de tu proceso, sin las esperas |
| **`pstats`** | El módulo que lee, ordena y filtra un perfil de cProfile, también guardado en un archivo |
| **py-spy** | Un perfilador por muestreo escrito en Rust que lee desde fuera la memoria de un proceso de Python |
| **`record` (py-spy)** | La orden de py-spy que graba un perfil y lo guarda, por defecto como gráfico de llamas en SVG |
| **Ruido** | Las variaciones en una medida que no vienen de tu código: otros procesos, la frecuencia de la CPU, las cachés |
| **`SYS_PTRACE`** | La capacidad de Linux que permite leer la memoria de otros procesos. Docker no la da por defecto |
| **Tiempo de reloj (*wall time*)** | Todo el tiempo que pasa, también las esperas. Es el `real` de la orden `time` |
| **Tiempo de CPU** | El tiempo que la CPU trabajó para tu proceso. Es `user + sys` en la orden `time` |
| **`timeit`** | El módulo que repite una medida muchas veces y apaga el recolector de basura mientras mide |
| **`top` (py-spy)** | La orden de py-spy que muestra el perfil en vivo, como `top` con los procesos |
| **`tottime`** | En cProfile, el tiempo propio de una función, sin contar las que llama |
| **Vectorizar** | Escribir una operación sobre un array entero, sin bucle de Python, para que el bucle lo haga código compilado |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
