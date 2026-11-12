"""Ejercicio 02 · Entrenar, probar y la referencia: medir lo que un modelo no ha visto.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

print("Ejercicio 02 · Entrenar, probar y la referencia")

# Doscientas medidas de cuatro zonas. En el Sur y en el Centro el valor es más alto, y el
# 10 % de las medidas son de nivel "alto". No leas cómo se generan: descúbrelo midiendo.
rng = np.random.default_rng(31)
zone = rng.choice(["Norte", "Sur", "Este", "Centro"], size=200)
shift = pd.Series(zone).map({"Norte": 0.0, "Sur": 12.0, "Este": 0.0, "Centro": 6.0})
value = (20 + shift + rng.normal(0, 5, 200)).round(1)
frame = pd.DataFrame({"zona": zone, "hora": rng.uniform(0, 24, 200).round(2), "valor": value})
frame["nivel"] = np.where(frame["valor"] >= frame["valor"].quantile(0.9), "alto", "normal")
print(f"{len(frame)} medidas · nivel alto: {(frame['nivel'] == 'alto').mean():.0%}")


# ============================================
# PASO 1: Repartir
# ============================================
# Descomenta las siguientes líneas:
# train, test = train_test_split(frame, test_size=0.25, random_state=31)
# print(f"entrenamiento: {len(train)} · prueba: {len(test)}")
# print(f"primeras filas de prueba: {list(test.index[:5])}")
# again = train_test_split(frame, test_size=0.25, random_state=31)[1]
# other = train_test_split(frame, test_size=0.25, random_state=32)[1]
# print(f"misma semilla, mismo reparto: {list(again.index) == list(test.index)}")
# print(f"otra semilla, otro reparto: {list(other.index) != list(test.index)}")


# ============================================
# PASO 2: Estratificar
# ============================================
# Descomenta las siguientes líneas:
# for seed in [1, 2, 3]:
#     plain = train_test_split(frame, test_size=0.25, random_state=seed)[1]
#     strata = train_test_split(frame, test_size=0.25, random_state=seed, stratify=frame["nivel"])[1]
#     print(
#         f"semilla {seed}: altos en prueba {(plain['nivel'] == 'alto').sum():>2} al azar,"
#         f" {(strata['nivel'] == 'alto').sum()} estratificado"
#     )


# ============================================
# PASO 3: Las métricas, a mano y con scikit-learn
# ============================================
# Descomenta las siguientes líneas:
# x = pd.get_dummies(frame["zona"], dtype="float64")
# x_train, x_test = x.loc[train.index], x.loc[test.index]
# y_train, y_test = train["valor"], test["valor"]
# model = LinearRegression().fit(x_train, y_train)
# predicted = model.predict(x_test)
# errors = y_test - predicted
# mae, rmse, r2 = (
#     f(y_test, predicted) for f in [mean_absolute_error, root_mean_squared_error, r2_score]
# )
# print(f"MAE  a mano {errors.abs().mean():.3f} · scikit-learn {mae:.3f}")
# print(f"RMSE a mano {np.sqrt((errors**2).mean()):.3f} · scikit-learn {rmse:.3f}")
# by_hand = 1 - (errors**2).sum() / ((y_test - y_test.mean()) ** 2).sum()
# print(f"R²   a mano {by_hand:.3f} · scikit-learn {r2:.3f}")


# ============================================
# PASO 4: Entrenamiento y prueba
# ============================================
# Descomenta las siguientes líneas:
# print(f"zona, R²: entrenamiento {model.score(x_train, y_train):.3f} · prueba {r2:.3f}")
# hour = frame[["hora"]]
# memory = KNeighborsRegressor(n_neighbors=1).fit(hour.loc[train.index], y_train)
# fit_r2 = memory.score(hour.loc[train.index], y_train)
# test_r2 = memory.score(hour.loc[test.index], y_test)
# print(f"hora, 1 vecino, R²: entrenamiento {fit_r2:.3f} · prueba {test_r2:.3f}")


# ============================================
# PASO 5: La referencia
# ============================================
# Descomenta las siguientes líneas:
# baseline = DummyRegressor(strategy="mean").fit(x_train, y_train)
# guessed = baseline.predict(x_test)
# print(f"la referencia predice siempre {guessed[0]:.2f}, la media: {y_train.mean():.2f}")
# print(f"MAE: modelo {mae:.2f} · referencia {mean_absolute_error(y_test, guessed):.2f}")
# print(f"R²:  modelo {r2:.3f} · referencia {r2_score(y_test, guessed):.3f}")


# ============================================
# PASO 6: Los residuos
# ============================================
# Descomenta las siguientes líneas:
# print("residuo medio por zona, referencia y modelo:")
# table = pd.DataFrame({"referencia": y_test - guessed, "modelo": errors, "zona": test["zona"]})
# print(table.groupby("zona").mean().round(2).to_string())
