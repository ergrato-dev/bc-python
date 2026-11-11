# Glosario — Semana 29

| Término | Definición |
|---|---|
| **Atípico** | Una medida muy lejos de las demás. Puede ser un error o lo más interesante de los datos: antes de quitarla, explica por qué es imposible |
| **Carga idempotente** | Una carga que deja lo mismo si se ejecuta una vez o varias. `to_sql(if_exists="replace")` lo es; `"append"` no |
| **Celda** | La unidad de un notebook: de código, que se ejecuta, o de Markdown, que se lee |
| **Centinela** | Un valor que significa "sin dato" (999, −1, "n/d"). Para pandas es un número más, hasta que lo cambias por `NaN` |
| **`chunksize`** | Leer una consulta por partes, como un iterador de `DataFrame`. Con `stream_results=True`, sin traerlo todo a memoria |
| **Colab** | Google Colaboratory: notebooks en la nube, con GPU gratuita limitada. Alternativa oficial del bootcamp para explorar, nunca para entregar |
| **Contador de ejecución** | El `[3]` junto a una celda: cuántas celdas había ejecutado el kernel antes. La única pista del orden real |
| **EDA** | Análisis exploratorio de datos: mirar una tabla con un orden fijo (forma, tipos, huecos, etiquetas, distribuciones, atípicos, relaciones) antes de calcular nada |
| **Estado oculto** | Lo que el kernel recuerda y el archivo no dice: celdas ejecutadas dos veces, en otro orden o ya borradas |
| **ETL** | Extraer, transformar y cargar (*extract, transform, load*): mover datos de donde se guardan a donde se analizan |
| **Grupo de dependencias** | Paquetes de `pyproject.toml` que solo se instalan si los pides (`--group notebook`). `dev` es el grupo por defecto |
| **Huella** | Un resumen de un archivo, como SHA-256, que cambia si cambia un solo byte. Comprueba que los datos son los mismos |
| **Idempotente** | Que da el mismo resultado si se repite. Ver *carga idempotente* |
| **Inyección de SQL** | Un valor pegado en el texto de una consulta que se convierte en SQL. Se evita con parámetros |
| **Instantánea** | Una copia fija de los datos, con su huella, que lee el análisis en lugar de la base viva |
| **`.ipynb`** | El archivo de un notebook: un JSON con celdas, salidas y metadatos (`nbformat` 4) |
| **JupyterLab** | El entorno web para trabajar con notebooks, archivos y terminales. En tu proyecto, en el grupo `notebook` y en un contenedor |
| **Kernel** | El proceso que ejecuta las celdas de un notebook y guarda sus variables. Para Python, `ipykernel` |
| **Magia** | Una orden de IPython que empieza por `%` (`%timeit`). No es Python: falla fuera de Jupyter |
| **`nbclient`** | La biblioteca que ejecuta un notebook con un kernel desde Python. La usan `jupyter execute` y `nbconvert` |
| **`nbconvert`** | Convierte y transforma notebooks; en tu gancho, `--clear-output` quita las salidas |
| **`nbformat`** | La biblioteca que lee, escribe y valida archivos `.ipynb` |
| **Parámetro (SQL)** | Un valor que viaja aparte de la consulta (`:station`), y PostgreSQL trata como dato, nunca como SQL |
| **Perfil (Compose)** | Una etiqueta de un servicio de `compose.yaml` que hace que solo arranque con `--profile` |
| **`read_sql`** | La función de pandas que ejecuta una consulta y devuelve un `DataFrame` |
| **Regla de Tukey** | Marca como atípico lo que queda a más de 1,5 rangos intercuartílicos del primer o del tercer cuartil |
| **Reproducible** | Que otra persona, otro día, con tus datos y tu código, obtiene el mismo resultado |
| **Restart Kernel and Run All Cells** | La orden de JupyterLab que ejecuta el notebook de arriba abajo en un kernel nuevo: la prueba mínima de que funciona |
| **Salida** | Lo que muestra una celda al ejecutarse: texto, el valor de su última línea, una tabla o un gráfico. No va a Git |
| **SHA-256** | Una función de huella de 64 caracteres hexadecimales. `hashlib.sha256(datos).hexdigest()` |
| **`to_sql`** | El método de pandas que escribe un `DataFrame` como tabla de una base de datos |
| **Token (Jupyter)** | La clave al azar que pide el servidor de JupyterLab; sin ella, contesta `403` |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
