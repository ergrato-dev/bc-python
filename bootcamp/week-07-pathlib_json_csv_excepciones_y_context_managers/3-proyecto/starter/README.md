# Observatorio de datos — <tu dominio>

Dominio: <escribe aquí tu dominio de docs/dominios.md>.

Qué registra: <una frase>. Medida principal: <medida y unidad>.

```bash
uv run observatorio "etiqueta;valor"       # clasifica una o varias líneas
uv run observatorio < medidas.txt          # clasifica un archivo y lo resume
uv run observatorio -f medidas.csv -j resumen.json   # lee un CSV y guarda el resumen
uv run pytest                              # tests en tu máquina
docker compose run --build --rm app        # tests en el contenedor
```
