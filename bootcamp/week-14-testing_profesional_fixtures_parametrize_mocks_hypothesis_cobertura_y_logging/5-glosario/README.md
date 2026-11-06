# Glosario — Semana 14

| Término | Definición |
|---|---|
| **`assume`** | Función de Hypothesis que descarta, dentro del test, un ejemplo que no cumple una condición |
| **`autospec`** | Opción de `patch` (y función `create_autospec`) que da al doble la firma del original: una llamada que el original no aceptaría lanza `TypeError` |
| **`basicConfig`** | `logging.basicConfig(level=..., format=...)`: configura el logger raíz con un manejador a stderr. Lo llama el programa, una vez, al arrancar |
| **`caplog`** | Fixture de pytest que captura los mensajes de registro de un test: `caplog.messages`, `caplog.records` y `caplog.set_level` |
| **Cobertura (*coverage*)** | Qué parte del código ejecutaron los tests. La de **líneas** cuenta sentencias; la de **ramas** cuenta también los dos caminos de cada `if` |
| **`conftest.py`** | Archivo de la carpeta de tests que pytest carga antes que ellos: sus fixtures valen en todos los tests de la carpeta, sin importarlas |
| **Contraejemplo** | Un dato que rompe una propiedad. Hypothesis lo encoge y lo escribe como `Failing test case` |
| **Doble de prueba** | Objeto que sustituye en un test a una pieza real que el test no controla: red, reloj, sistema de archivos. Pueden ser *stubs*, *fakes* o *mocks* |
| **Encogimiento (*shrinking*)** | Lo que hace Hypothesis con un contraejemplo: buscar la versión más simple que sigue fallando, como `['0;:']` |
| **Estrategia** | Descripción de un conjunto de datos posibles en Hypothesis: `st.integers()`, `st.text()`, `st.lists(...)`. Se combinan con `\|`, `builds`, `filter` y `map` |
| **`@example`** | Decorador de Hypothesis que añade un caso concreto que se prueba siempre, además de los generados |
| **`fail_under`** | Opción de coverage: por debajo de ese porcentaje, `coverage report` termina con código 2 |
| ***Fake*** | Doble que funciona de verdad, pero de forma simple: un `BytesIO` en lugar de un archivo |
| **Fixture** | Función con `@pytest.fixture` que prepara algo para los tests. Un test la pide poniendo su nombre como parámetro |
| **Fixture fábrica** | Fixture que devuelve una función para crear lo que el test necesite, como `write_file(nombre, texto)` |
| **`@given`** | Decorador de Hypothesis que convierte un test en un test de propiedades: recibe una estrategia por parámetro |
| **`.hypothesis/`** | Carpeta donde Hypothesis guarda los contraejemplos para probarlos primero en la siguiente ejecución. Va al `.gitignore` |
| **Inyección de dependencias** | Recibir como parámetro lo que una función usa (el reloj, los argumentos, el origen de las líneas) para que un test pueda pasar el suyo sin parchear |
| **Logger** | Objeto de `logging` con nombre, creado con `logging.getLogger(__name__)`. Los nombres con puntos forman un árbol que acaba en el logger raíz |
| **Manejador (*handler*)** | Pieza de `logging` que decide dónde se escribe un mensaje: stderr, un archivo, un servicio. Los pone el programa, no el paquete |
| **Marca** | Etiqueta de pytest sobre un test: `skip`, `skipif`, `xfail`, `parametrize` o una propia registrada en `markers` |
| ***Mock*** | Doble que además apunta cómo lo llamaron, para comprobarlo con `assert_called_once_with`. En Python, `unittest.mock.Mock` y `MagicMock` |
| **`monkeypatch`** | Fixture de pytest que cambia un atributo, una variable de entorno o el directorio actual, y lo deshace al terminar el test |
| **Nivel de registro** | La importancia de un mensaje: `DEBUG`, `INFO`, `WARNING`, `ERROR` o `CRITICAL`. Se ve el nivel configurado y los superiores |
| **`parametrize`** | Marca de pytest que ejecuta el mismo test una vez por cada caso de una lista |
| **`patch`** | `unittest.mock.patch("modulo.nombre")`: cambia un nombre por un doble mientras dura un `with`. Se parchea donde se **usa** el nombre |
| **Propiedad** | Algo que debe cumplirse con cualquier dato válido: ida y vuelta, invariantes, límites, "nunca falla" |
| **`scope`** | Cuántas veces se crea una fixture: una por test (`function`), por archivo (`module`) o por ejecución (`session`) |
| **`side_effect`** | Atributo de un `Mock`: una excepción que lanza, una lista de valores que devuelve en orden o una función que llama |
| ***Stub*** | Doble que devuelve una respuesta fija |
| **Último recurso (*last resort*)** | Manejador que usa `logging` si nadie configuró nada: escribe en stderr los WARNING y superiores, solo con el texto |
| **`xfail`** | Marca de un fallo conocido: el test se ejecuta y se espera que falle. Con `strict=True`, si pasa (`XPASS`) cuenta como fallo |
| **`yield` (en una fixture)** | Separa la preparación de la limpieza: lo de después del `yield` se ejecuta al terminar el test, aunque falle |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
