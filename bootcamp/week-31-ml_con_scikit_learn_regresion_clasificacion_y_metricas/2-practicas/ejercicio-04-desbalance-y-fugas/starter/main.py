"""Ejercicio 04 · Desbalance y fugas: cuando una buena métrica miente.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

print("Ejercicio 04 · Desbalance y fugas")

# Mil lecturas de sensores. "fallo" dice si el sensor falló poco después: pasa en unas
# cuatro de cada cien, y más cuando la batería está baja. La temperatura no influye.
rng = np.random.default_rng(31)
readings = pd.DataFrame(
    {"bateria": rng.uniform(0, 100, 1000).round(), "temperatura": rng.uniform(5, 35, 1000).round(1)}
)
chance = 0.15 * np.exp(-readings["bateria"] / 25)
readings["fallo"] = np.where(rng.random(1000) < chance, "sí", "no")
print(f"{len(readings)} lecturas · con fallo: {(readings['fallo'] == 'sí').mean():.1%}")
x = readings[["bateria", "temperatura"]]
x_train, x_test, y_train, y_test = train_test_split(
    x, readings["fallo"], test_size=0.3, random_state=31, stratify=readings["fallo"]
)


def show(name: str, said: np.ndarray) -> None:
    """Exactitud, equilibrada, y la precisión y exhaustividad de los fallos."""
    accuracy = accuracy_score(y_test, said)
    balanced = balanced_accuracy_score(y_test, said)
    precision = precision_score(y_test, said, pos_label="sí", zero_division=0)
    recall = recall_score(y_test, said, pos_label="sí")
    print(
        f"{name:<12} exactitud {accuracy:.3f} · equilibrada {balanced:.3f}"
        f" · precisión {precision:.2f} · exhaustividad {recall:.2f}"
    )


# ============================================
# PASO 1: Una exactitud del 95 % sin aprender nada
# ============================================
# Descomenta las siguientes líneas:
# baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train)
# show("referencia", baseline.predict(x_test))


# ============================================
# PASO 2: Un modelo que tampoco avisa
# ============================================
# Descomenta las siguientes líneas:
# model = LogisticRegression().fit(x_train, y_train)
# show("logística", model.predict(x_test))
# print(f"probabilidad de fallo más alta en prueba: {model.predict_proba(x_test)[:, 1].max():.2f}")


# ============================================
# PASO 3: Pesar las clases
# ============================================
# Descomenta las siguientes líneas:
# weighted = LogisticRegression(class_weight="balanced").fit(x_train, y_train)
# show("equilibrada", weighted.predict(x_test))
# print(f"coef_ (batería, temperatura): {weighted.coef_.round(3)[0]}")


# ============================================
# PASO 4: El objetivo disfrazado
# ============================================
# Descomenta las siguientes líneas:
# temperature = readings["temperatura"]
# level = np.where(temperature < 15, "bajo", np.where(temperature < 25, "medio", "alto"))
# others = readings[["bateria"]]
# for name, inputs in [
#     ("con temperatura", readings[["bateria", "temperatura"]]),
#     ("sin ella", others),
# ]:
#     a, b, c, d = train_test_split(inputs, level, test_size=0.3, random_state=31, stratify=level)
#     said = LogisticRegression().fit(a, c).predict(b)
#     print(f"nivel, {name}: exactitud equilibrada {balanced_accuracy_score(d, said):.3f}")


# ============================================
# PASO 5: Calcular con la prueba
# ============================================
# Descomenta las siguientes líneas:
# leaked_r2, honest_r2 = [], []
# for seed in range(20):
#     noise = np.random.default_rng(seed)
#     frame = pd.DataFrame(
#         {"sensor": noise.integers(0, 60, 300).astype(str), "valor": noise.uniform(0, 80, 300)}
#     )
#     train, test = train_test_split(frame, test_size=0.25, random_state=seed)
#     everything = frame.groupby("sensor")["valor"].mean()
#     only_train = train.groupby("sensor")["valor"].mean()
#     fallback = train["valor"].mean()
#     for means, results in [(everything, leaked_r2), (only_train, honest_r2)]:
#         x_fit = train["sensor"].map(means).fillna(fallback).to_frame()
#         x_new = test["sensor"].map(means).fillna(fallback).to_frame()
#         fitted = LinearRegression().fit(x_fit, train["valor"])
#         results.append(r2_score(test["valor"], fitted.predict(x_new)))
# for name, results in [("con fuga", leaked_r2), ("sin fuga", honest_r2)]:
#     above = sum(r > 0 for r in results)
#     print(f"{name}: R² medio {np.mean(results):.2f} · {above} de 20 repartos con R² > 0")


# ============================================
# PASO 6: Medidas repetidas
# ============================================
# Descomenta las siguientes líneas:
# signal = pd.DataFrame({"hora": rng.uniform(0, 24, 300), "valor": rng.uniform(0, 80, 300)})
# twice = pd.concat([signal, signal], ignore_index=True)
# for name, data in [("sin repetir", signal), ("cada una dos veces", twice)]:
#     a, b = train_test_split(data, test_size=0.25, random_state=31)
#     near = KNeighborsRegressor(n_neighbors=1).fit(a[["hora"]], a["valor"])
#     print(f"{name}: R² en prueba {near.score(b[['hora']], b['valor']):.3f}")
