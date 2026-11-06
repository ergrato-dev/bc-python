# Glosario — Semana 03

| Término | Definición |
|---|---|
| **Acumulador** | Variable que combina todos los elementos de un bucle en un resultado: una suma, un producto, un texto. Empieza en el elemento neutro, antes del bucle |
| **`break`** | Termina el bucle de inmediato; solo sale del bucle en que está |
| **Bucle** | Bloque de código que se repite: una vez por elemento (`for`) o mientras se cumpla una condición (`while`) |
| **Bucle anidado** | Un bucle dentro de otro: por cada vuelta del de fuera, el de dentro da todas las suyas |
| **Bucle infinito** | Bucle cuya condición nunca se vuelve falsa; se corta con `Ctrl+C` |
| **Búfer** | Memoria donde un programa junta la salida antes de escribirla de golpe; por eso stdout y stderr pueden verse en otro orden |
| **Centinela** | Valor especial que indica "no hay más datos", como `fin` |
| **`continue`** | Salta el resto del cuerpo y pasa a la siguiente vuelta |
| **Contador** | Variable que empieza en `0` y suma `1` cada vez que un elemento cumple algo |
| **Cuerpo** | Las líneas con sangría bajo `for` o `while`: lo que se repite |
| **Depurador** | Herramienta que detiene un programa para ver sus variables y avanzar línea a línea: `pdb`, el de VS Code |
| **`else` de un bucle** | Bloque que se ejecuta si el bucle terminó sin `break` |
| **`enumerate`** | Da parejas `(posición, elemento)` al recorrer algo; `start=1` empieza a contar en 1 |
| **EOF** | *End of file*: fin de la entrada. Desde el teclado se envía con `Ctrl+D` |
| **Error lógico** | El programa termina sin error, pero el resultado es falso |
| **Iterable** | Valor que puede dar sus elementos uno a uno: `str`, `range`, una lista, `sys.stdin` |
| **Iteración** | Cada vuelta de un bucle |
| **`pdb`** | El depurador de la terminal de Python; se abre con `breakpoint()` |
| **Pila de llamadas** | La cadena de funciones que se llamaron hasta llegar a un punto; el traceback la muestra |
| **Punto de parada** | Línea donde el depurador detiene el programa; puede ser condicional |
| **`range`** | Genera enteros desde un inicio hasta un final **sin incluirlo**, con un paso opcional |
| **Racha** | La mayor cantidad de elementos seguidos que cumplen algo |
| **Redirección** | Conectar un archivo a la entrada (`<`) o a la salida (`>`, `2>`) de un programa |
| **Tabla de traza** | Tabla con una fila por vuelta y una columna por variable, para seguir un bucle a mano |
| **Traceback** | El informe de una excepción: qué pasó (última línea) y por dónde pasó el programa (las de arriba) |
| **Tubería** | `\|`: conecta la salida de un programa a la entrada de otro |
| **`while`** | Bucle que se repite mientras su condición sea verdadera |
| **`zip`** | Recorre varias secuencias a la vez; para en la más corta salvo con `strict=True` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
