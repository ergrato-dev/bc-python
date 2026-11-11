# Observatorio de datos — <tu dominio>

Dominio: <escribe aquí tu dominio de docs/dominios.md>.

Qué registra: <una frase>. Medida principal: <medida y unidad>.

```bash
uv run observatorio --help                         # los comandos y sus opciones
uv run observatorio informe "etiqueta;valor"       # clasifica una o varias líneas
uv run observatorio informe < medidas.txt          # clasifica un archivo y lo resume
uv run observatorio informe -f medidas.csv -j resumen.json   # lee un CSV y guarda el resumen
uv run observatorio informe -f medidas.csv -e escala.json    # con la escala de un JSON
uv run observatorio validar medidas.json           # comprueba un JSON de medidas
uv run observatorio lote medidas.csv medidas.txt   # resume varios archivos a la vez
uv run observatorio lote --procesos -t 2 medidas.csv medidas.txt   # con procesos
uv run observatorio vigilar -i 0.2 medidas.csv medidas.txt   # medidas en directo, una a una
uv run observatorio vigilar --tiempo 5 -l 2 medidas.csv medidas.txt   # con límite y plazo
uv run observatorio -v informe -f medidas.csv      # con el registro DEBUG en stderr
uv run observatorio --version                      # la versión del paquete
uv run pytest                                      # tests en tu máquina
uv run coverage run -m pytest && uv run coverage report   # cobertura
uv run ruff check && uv run ruff format            # estilo y errores habituales
uv run mypy                                        # tipos
docker compose run --build --rm app                # tests en el contenedor
```
