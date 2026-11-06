# Glosario — Semana 02

| Término | Definición |
|---|---|
| **Asignación aumentada** | Forma corta de operar y reasignar: `x += 1` es `x = x + 1` |
| **Captura** | En un `case`, un nombre suelto que recibe el valor de esa posición en vez de compararlo: `case ["hola", name]` |
| **`casefold`** | Método de `str` que pasa a minúsculas para comparar sin distinguir mayúsculas, cubriendo más idiomas que `lower` |
| **Código de salida** | Número que un programa devuelve al terminar: `0` éxito, otro valor fallo. Se ve con `echo $?` |
| **Cortocircuito** | `and` y `or` dejan de evaluar en cuanto conocen el resultado: en `a and b`, si `a` es falso, `b` no se ejecuta |
| **Desempaquetar** | Recibir varios valores en varios nombres a la vez: `user, _, domain = email.partition("@")` |
| **Especificación de formato** | Lo que va después de `:` en una f-string: `.2f`, `>10`, `,.2f`, `.1%` |
| **Expresión** | Código que produce un valor: `2 + 3`, `value > 0` |
| **Expresión condicional** | `a if condición else b`: elige un valor en una línea |
| **Guarda** | Condición `if` añadida a un `case`: el patrón solo cuenta si además la guarda es verdadera |
| **Índice** | Posición de un carácter en un texto, desde `0`; los negativos cuentan desde el final (`-1` es el último) |
| **Inmutable** | Que no se puede modificar después de crearse: los `str` lo son, por eso sus métodos devuelven un texto nuevo |
| **Inyección** | Ataque en el que un valor trae caracteres que otro sistema (HTML, SQL, terminal) interpreta como instrucciones |
| **`Interpolation`** | Objeto de una t-string que guarda un valor junto con su expresión, conversión y formato |
| **`match` / `case`** | Sentencia que compara un valor con patrones de arriba abajo y ejecuta el primero que encaja |
| **Normalización Unicode** | Convertir un texto a una forma única (NFC) para que el mismo acento se guarde siempre igual |
| **Patrón** | Lo que va después de `case`: un literal, alternativas con `\|`, una secuencia, una captura o `_` |
| **Precedencia** | Orden en que se calculan los operadores de una expresión sin paréntesis |
| **Slice** | Fragmento de una secuencia: `s[inicio:fin:paso]`; incluye `inicio` y excluye `fin` |
| **stdin, stdout, stderr** | Los tres flujos estándar: entrada, salida de resultados y salida de errores |
| **`sys.argv`** | Lista con el nombre del programa y los argumentos con que se lanzó, todos `str` |
| **t-string** | Texto con `t` delante (Python 3.14) que produce un `Template` en lugar de un `str` |
| **`Template`** | Objeto que produce una t-string: guarda por separado las partes fijas (`.strings`) y los valores (`.interpolations`) |
| **Truthiness** | Valor de verdad de cualquier objeto en una condición: `0`, `0.0`, `""`, `None` y `False` son falsos |
| **Tubería** | `a \| b` en la terminal: lo que `a` escribe en stdout entra por el stdin de `b` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
