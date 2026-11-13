"""Ejercicio 01 · Árboles de decisión: preguntas de sí o no.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor, export_text

print("Ejercicio 01 · Árboles de decisión")

# Medidas horarias de partículas finas (PM2.5) en cuatro zonas. Sube en hora punta (mucho
# más en el Centro, por el tráfico), con el aire en calma (viento < 2 m/s) y baja con lluvia
# (humedad > 85 %). Son umbrales y cruces, no rectas.
rng = np.random.default_rng(33)
n = 1500
hours = np.sort(rng.integers(0, 300 * 24, n))
air = pd.DataFrame(
    {
        "momento": pd.Timestamp("2026-01-05") + pd.to_timedelta(hours, unit="h"),
        "zona": rng.choice(["Centro", "Norte", "Sur", "Este"], n),
        "humedad": rng.uniform(30, 98, n).round(),
        "viento": rng.gamma(2.0, 2.0, n).round(1),
    }
)
air["hora"] = air["momento"].dt.hour
air["dia"] = air["momento"].dt.day_of_week
rush = air["hora"].isin([7, 8, 9, 18, 19, 20])
center = air["zona"] == "Centro"
zone = air["zona"].map({"Centro": 10.0, "Norte": 4.0, "Sur": 0.0, "Este": 6.0})
traffic = rush * np.where(center, 14.0, 4.0)
air["pm25"] = (
    12 + zone + traffic + 10 * (air["viento"] < 2) - 8 * (air["humedad"] > 85) + rng.normal(0, 3, n)
).round(1)
print(f"{len(air)} medidas · de {air['momento'].min():%d/%m} a {air['momento'].max():%d/%m}")

x = air[["hora", "dia", "zona", "humedad", "viento"]]
y = air["pm25"]
folds = KFold(5, shuffle=True, random_state=33)
scoring = "neg_mean_absolute_error"


def tree(depth: int | None) -> Pipeline:
    """La zona en one-hot y el resto tal cual: a un árbol no le hace falta escalar."""
    prepare = ColumnTransformer(
        [("zona", OneHotEncoder(handle_unknown="ignore"), ["zona"])],
        remainder="passthrough",
        verbose_feature_names_out=False,
    )
    return Pipeline(
        [("prepare", prepare), ("model", DecisionTreeRegressor(max_depth=depth, random_state=33))]
    )


# ============================================
# PASO 1: Un árbol de dos niveles
# ============================================
# Descomenta las siguientes líneas:
# small = tree(2).fit(x, y)
# names = small.named_steps["prepare"].get_feature_names_out().tolist()
# print(export_text(small.named_steps["model"], feature_names=names, decimals=1))


# ============================================
# PASO 2: Predice en escalones
# ============================================
# Descomenta las siguientes líneas:
# calm = pd.DataFrame(
#     {"hora": 12, "dia": 2, "zona": "Norte", "humedad": 50.0, "viento": np.arange(0, 10, 0.5)}
# )
# steps = small.predict(calm)
# print(f"{len(calm)} vientos de 0 a 9.5 m/s · {len(np.unique(steps))} predicciones distintas:")
# print(np.unique(steps).round(1))


# ============================================
# PASO 3: La profundidad
# ============================================
# Descomenta las siguientes líneas:
# for depth in [1, 2, 4, 6, 10, None]:
#     scores = cross_validate(tree(depth), x, y, cv=folds, scoring=scoring, return_train_score=True)
    # abs: sin límite, el error de entrenamiento es 0, y -0.0 se escribiría "-0.00".
#     train_mae, test_mae = abs(scores["train_score"].mean()), -scores["test_score"].mean()
#     print(f"max_depth={depth!s:<5} MAE entrenamiento {train_mae:5.2f} · validación {test_mae:5.2f}")


# ============================================
# PASO 4: Un árbol frente a una recta
# ============================================
# Descomenta las siguientes líneas:
# line = Pipeline([("prepare", tree(None).named_steps["prepare"]), ("model", LinearRegression())])
# for name, model in [("recta", line), ("árbol, max_depth=6", tree(6))]:
#     mae = -cross_val_score(model, x, y, cv=folds, scoring=scoring)
#     print(f"{name:<19} MAE {mae.round(2)} · media {mae.mean():.2f}")


# ============================================
# PASO 5: Al árbol no le importa la escala
# ============================================
# Descomenta las siguientes líneas:
# squeezed = x.assign(viento=np.log1p(x["viento"]), humedad=x["humedad"] / 100)
# for name, model in [("árbol", tree(6)), ("recta", line)]:
#     before = model.fit(x, y).predict(x)
#     after = model.fit(squeezed, y).predict(squeezed)
#     print(f"{name}: ¿las mismas predicciones? {np.allclose(before, after)}")


# ============================================
# PASO 6: Un árbol no extrapola
# ============================================
# Descomenta las siguientes líneas:
# days = pd.DataFrame({"dia": np.arange(60)})
# trend = 20 + 0.5 * days["dia"]
# seen = days["dia"] < 40
# later = pd.DataFrame({"dia": [45, 50, 59]})
# for name, model in [
#     ("árbol", DecisionTreeRegressor(random_state=33)),
#     ("recta", LinearRegression()),
# ]:
#     model.fit(days[seen], trend[seen])
#     print(f"{name}: días 45, 50 y 59 → {model.predict(later).round(1)}")
# print(f"de verdad: {(20 + 0.5 * later['dia']).to_numpy()}")
