"""Lo que ejecuta `python -m meteo`."""

from meteo.stats import mean

print("meteo como programa: media de 20, 22,5 y 19 =", mean([20.0, 22.5, 19.0]))
