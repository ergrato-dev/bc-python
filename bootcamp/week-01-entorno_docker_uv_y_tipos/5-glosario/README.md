# Glosario — Semana 01

| Término | Definición |
|---|---|
| **Anotación de tipo** | Indicación del tipo esperado (`count: int`, `-> float`). Python no la comprueba al ejecutar; la usan mypy y el editor |
| **Build multi-stage** | `Dockerfile` con varios `FROM`: una etapa prepara algo y la final solo copia lo necesario |
| **Bytecode** | Instrucciones intermedias en las que CPython compila tu código antes de ejecutarlo |
| **Caché de capas** | Docker reutiliza las capas cuyas instrucciones y archivos no cambiaron |
| **Capa** | Resultado de una instrucción del `Dockerfile`; una imagen es una pila de capas |
| **Contenedor** | Proceso aislado creado a partir de una imagen |
| **CPython** | El intérprete oficial de Python, escrito en C |
| **Dependencia transitiva** | Biblioteca que no pediste tú, sino otra de tus dependencias |
| **Docstring** | Texto entre `"""` al principio de una función que explica qué hace |
| **Entorno virtual** | Carpeta (`.venv/`) con un Python y las bibliotecas de un solo proyecto |
| **f-string** | Texto con `f` delante que inserta valores entre llaves: `f"{value:.1f}"` |
| **float** | Número decimal en coma flotante; no es exacto: se compara con `math.isclose` |
| **Imagen** | Plantilla de solo lectura con sistema, Python, bibliotecas y código |
| **int** | Número entero; en Python no tiene límite de tamaño |
| **Lockfile (`uv.lock`)** | Archivo con la versión exacta y el hash de cada dependencia, transitivas incluidas |
| **None** | El valor "no hay dato"; se pregunta con `is None` |
| **`pyproject.toml`** | Archivo que declara el proyecto: nombre, Python aceptado y dependencias directas |
| **PVM** | Máquina virtual de Python: ejecuta el bytecode |
| **REPL** | *Read-Eval-Print Loop*: el intérprete interactivo (`>>>`) |
| **root** | Usuario con todos los permisos en Linux (identificador 0) |
| **SyntaxError** | Error de escritura del código; impide ejecutar cualquier línea |
| **Tipado dinámico** | El tipo pertenece al objeto, no al nombre; un nombre puede apuntar a objetos de tipos distintos |
| **Traceback** | Informe de un error en ejecución; se lee de abajo arriba |
| **uv** | Herramienta que instala Python, crea entornos, resuelve dependencias y ejecuta proyectos |
| **ValueError** | Error cuando el tipo es correcto pero el valor no sirve: `int("4.5")` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
