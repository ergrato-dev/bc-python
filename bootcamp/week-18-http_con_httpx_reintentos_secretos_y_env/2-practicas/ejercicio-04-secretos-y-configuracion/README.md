# Ejercicio 04 — Secretos y configuración

⏱️ 1 h · Teoría previa: [04](../../1-teoria/04-secretos-y-configuracion-con-env.md)

## Objetivo

Sacar la configuración del código, y el secreto de donde no debe estar:

- leer variables de entorno con `os.environ`, y ver sus dos problemas;
- cargar un archivo `.env` con `uv run --env-file`;
- leer y validar la configuración con `pydantic-settings`;
- saber quién gana cuando una variable está en el entorno y en `.env`;
- esconder el token con `SecretStr`, y ver lo que `SecretStr` no puede hacer por ti.

Es la clase `Settings` de tu proyecto, con el prefijo `EJERCICIO_`. El token es **inventado** (`abc123`): nunca pongas uno de verdad en un ejercicio. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas **con la orden que dice cada paso** y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-18-http_con_httpx_reintentos_secretos_y_env/2-practicas/ejercicio-04-secretos-y-configuracion/starter
uv run python main.py
```

```
Ejercicio 04 · Secretos y configuración
```

En `starter/` hay dos archivos ocultos: `.env.example`, la plantilla de la configuración, y `.gitignore`, con `.env` dentro. Míralos con `ls -a` y `cat`.

## Pasos

### 1. Leer una variable de entorno

Descomenta el **PASO 1** y ejecuta dos veces, la segunda con la variable delante:

```bash
uv run python main.py
EJERCICIO_TOKEN=abc123 uv run python main.py
```

```
Ejercicio 04 · Secretos y configuración
get: None
KeyError: 'EJERCICIO_TOKEN'
Ejercicio 04 · Secretos y configuración
get: abc123
corchetes: abc123
```

`VARIABLE=valor orden` pone la variable en el entorno **solo** de esa orden, y uv se la pasa a Python. `os.environ` es un diccionario: con corchetes, una variable que no existe es un `KeyError`; con `get`, es `None`.

### 2. Todo es texto

Descomenta el **PASO 2** y ejecuta:

```bash
uv run python main.py
EJERCICIO_RETRIES=0 uv run python main.py
```

Las últimas líneas de cada ejecución:

```
reintentos: '3' · ¿reintenta? True
reintentos: '0' · ¿reintenta? True
```

Con `EJERCICIO_RETRIES=0`, el programa **sigue reintentando**. Una variable de entorno es siempre un texto, y `'0'` es un texto no vacío: verdadero. El fallo no está en el entorno, sino en que nadie convirtió ni validó el valor. Es el primer problema que resuelve `pydantic-settings`.

### 3. Un archivo `.env`

Crea tu `.env` a partir de la plantilla y pon el token inventado:

```bash
cp .env.example .env
```

Abre `.env` y deja la línea del token así: `EJERCICIO_TOKEN=abc123`. Después, descomenta el **PASO 3** y ejecuta de dos formas:

```bash
uv run python main.py
uv run --env-file .env python main.py
```

La última línea de la primera, y la salida entera de la segunda:

```
variables EJERCICIO_*: []
Ejercicio 04 · Secretos y configuración
get: abc123
corchetes: abc123
reintentos: '5' · ¿reintenta? True
variables EJERCICIO_*: ['EJERCICIO_RETRIES', 'EJERCICIO_TIMEOUT', 'EJERCICIO_TOKEN']
```

Que exista `.env` no hace nada por sí solo: es un archivo como otro cualquiera. `uv run --env-file .env` lo lee y mete sus variables en el entorno **antes** de arrancar Python, y entonces `os.environ` las ve. Si escribes mal el nombre: `error: No environment file found at: .env`.

Comprueba que Git no lo verá:

```bash
git check-ignore -v .env
```

```
bootcamp/week-18-http_con_httpx_reintentos_secretos_y_env/2-practicas/ejercicio-04-secretos-y-configuracion/starter/.gitignore:2:.env	.env
```

Qué `.gitignore` lo ignora (la ruta, desde la raíz del repositorio), en qué línea y con qué patrón. Si no escribe nada, `.env` **no** está ignorado.

### 4. `pydantic-settings`

Descomenta el **PASO 4** y ejecuta, otra vez sin `--env-file`:

```bash
uv run python main.py
EJERCICIO_RETRIES=0 uv run python main.py
```

Las dos últimas líneas de cada una:

```
token=SecretStr('**********') timeout=10.0 retries=5
¿reintenta? True
token=SecretStr('**********') timeout=10.0 retries=0
¿reintenta? False
```

Sin `--env-file`, el paso 3 sigue diciendo `[]`: el entorno no tiene nada. Pero `Settings` lee `.env` **por su cuenta** (`env_file=".env"`), con el prefijo `EJERCICIO_`. Y convierte: `retries` es un `int`, y `0` ya es falso. Es lo que hace tu proyecto, así que funciona igual con `uv run`, en Docker o en una API.

Fíjate en el token: está, pero sale como asteriscos.

### 5. Un valor que no vale

Descomenta el **PASO 5** y ejecuta `uv run python main.py`:

```
EJERCICIO_TIMEOUT: Input should be a valid number, unable to parse string as a number
```

El paso pone en el entorno `EJERCICIO_TIMEOUT=rápido`, como si alguien se hubiera equivocado al configurar, y lo quita al terminar. `Settings()` lo valida **al arrancar** y falla con un `ValidationError` que dice qué campo y por qué. Es mucho mejor que un `float("rápido")` que revienta a mitad de una descarga. El mensaje de Pydantic está en inglés; el nombre de la variable lo pones tú.

### 6. ¿Quién gana, el entorno o `.env`?

Descomenta el **PASO 6** y ejecuta `uv run python main.py`:

```
solo .env: 5
entorno y .env: 7
```

`.env` dice 5. Con `EJERCICIO_RETRIES=7` en el entorno, gana el **entorno**. Así puedes tener tu `.env` de siempre y cambiar un valor para una sola orden, como hiciste en el paso 4 con `EJERCICIO_RETRIES=0`.

### 7. `SecretStr`

Descomenta el **PASO 7** y ejecuta `uv run python main.py`:

```
print: **********
repr: SecretStr('**********')
JSON: {"token":"**********","timeout":10.0,"retries":5}
para la cabecera: 6 caracteres, empieza por abc
```

Ni `print`, ni `repr`, ni el JSON de la configuración enseñan el token. Así, un `print(settings)` para depurar o una configuración guardada en un registro no lo filtran. El valor de verdad solo sale con `get_secret_value()`, que es fácil de buscar en el código. Aquí ni siquiera lo imprimimos entero.

### 8. Lo que `SecretStr` no protege

Descomenta el **PASO 8** y ejecuta `uv run python main.py`:

```
con str: token='abc123'
¿.env en .gitignore? True
```

La misma configuración con `token: str`: el primer `print` lo enseña. `SecretStr` solo funciona si lo usas.

Y no protege nada fuera de tu programa: si `.env` acaba en Git, en la imagen Docker o en la captura que pegas en un *pull request*, el token se filtró, y la única solución es **revocarlo**. Por eso `.env` va en `.gitignore` **antes** del primer `git add`, y en `.dockerignore`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pydantic_settings'` | Ejecutaste `python main.py` sin `uv run` |
| `zsh:1: command not found: abc123` (o `bash: abc123: command not found`) | Pusiste un espacio después del `=`: es `EJERCICIO_TOKEN=abc123 uv run ...`, todo junto |
| `error: No environment file found at: .env` | No creaste `.env`: `cp .env.example .env` |
| El paso 4 da `token=None` | El token está vacío en `.env`, o lo escribiste en `.env.example` |
| El paso 4 da `retries=3` | No hay `.env` en la carpeta: `Settings` lo busca en la carpeta desde la que ejecutas |
| Valores raros que no están en `.env` | Exportaste variables `EJERCICIO_*` en tu terminal, y ganan: `env \| grep EJERCICIO` y `unset` |
| `git check-ignore` no escribe nada | `.env` no está ignorado: no hagas `git add` hasta arreglarlo |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Reintentos con espera](../ejercicio-03-reintentos-con-espera/README.md) | **Ejercicio 04 · Secretos y configuración** | [Proyecto · Observatorio, capa 17](../../3-proyecto/README.md) |
