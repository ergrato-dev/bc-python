"""Ejercicio 03 · Clasificar y medir: probabilidades, umbral y matriz de confusión.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

print("Ejercicio 03 · Clasificar y medir")

# Cuatrocientos días con su temperatura máxima y su humedad. "aviso" dice si ese día hubo
# aviso por calor: es más probable con calor y con humedad, pero no es seguro.
rng = np.random.default_rng(31)
days = pd.DataFrame(
    {"temperatura": rng.uniform(15, 40, 400).round(1), "humedad": rng.uniform(20, 90, 400).round()}
)
chance = 1 / (1 + np.exp(-(0.5 * (days["temperatura"] - 33) + 0.05 * (days["humedad"] - 55))))
days["aviso"] = np.where(rng.random(400) < chance, "sí", "no")
print(f"{len(days)} días · con aviso: {(days['aviso'] == 'sí').mean():.0%}")
x = days[["temperatura", "humedad"]]
x_train, x_test, y_train, y_test = train_test_split(
    x, days["aviso"], test_size=0.25, random_state=31, stratify=days["aviso"]
)


# ============================================
# PASO 1: Probabilidades
# ============================================
# Descomenta las siguientes líneas:
# model = LogisticRegression().fit(x_train, y_train)
# print(f"classes_: {list(model.classes_)}")
# probabilities = model.predict_proba(x_test)
# print(x_test.head(3).assign(p_no=probabilities[:3, 0].round(2), p_si=probabilities[:3, 1].round(2)))
# print(f"cada fila suma 1: {np.allclose(probabilities.sum(axis=1), 1)}")
# predicted = model.predict(x_test)
# same = (predicted == np.where(probabilities[:, 1] >= 0.5, "sí", "no")).all()
# print(f"predict es 'sí' desde 0,5: {same}")


# ============================================
# PASO 2: La matriz de confusión
# ============================================
# Descomenta las siguientes líneas:
# matrix = confusion_matrix(y_test, predicted, labels=["sí", "no"])
# print(matrix)
# (tp, fn), (fp, tn) = matrix
# print(f"VP {tp} · FN {fn} · FP {fp} · VN {tn}")


# ============================================
# PASO 3: Exactitud, precisión, exhaustividad y F1
# ============================================
# Descomenta las siguientes líneas:
# print(
#     f"exactitud     a mano {(tp + tn) / matrix.sum():.3f} · {accuracy_score(y_test, predicted):.3f}"
# )
# precision = precision_score(y_test, predicted, pos_label="sí")
# recall = recall_score(y_test, predicted, pos_label="sí")
# print(f"precisión     a mano {tp / (tp + fp):.3f} · {precision:.3f}")
# print(f"exhaustividad a mano {tp / (tp + fn):.3f} · {recall:.3f}")
# f1 = f1_score(y_test, predicted, pos_label="sí")
# print(f"F1            a mano {2 * precision * recall / (precision + recall):.3f} · {f1:.3f}")


# ============================================
# PASO 4: Mover el umbral
# ============================================
# Descomenta las siguientes líneas:
# print("umbral  avisos  precisión  exhaustividad")
# for threshold in [0.2, 0.35, 0.5, 0.65, 0.8]:
#     said = np.where(probabilities[:, 1] >= threshold, "sí", "no")
#     p = precision_score(y_test, said, pos_label="sí", zero_division=0)
#     r = recall_score(y_test, said, pos_label="sí")
#     print(f"{threshold:>6}  {(said == 'sí').sum():>6}  {p:>9.2f}  {r:>13.2f}")


# ============================================
# PASO 5: La referencia y la exactitud equilibrada
# ============================================
# Descomenta las siguientes líneas:
# baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train)
# guessed = baseline.predict(x_test)
# for name, said in [("modelo", predicted), ("referencia", guessed)]:
#     accuracy = accuracy_score(y_test, said)
#     balanced = balanced_accuracy_score(y_test, said)
#     print(f"{name:<10} exactitud {accuracy:.3f} · equilibrada {balanced:.3f}")


# ============================================
# PASO 6: Tres clases
# ============================================
# Descomenta las siguientes líneas:
# score = 0.5 * (days["temperatura"] - 33) + 0.05 * (days["humedad"] - 55) + rng.normal(0, 1.5, 400)
# colour = pd.cut(score, [-np.inf, -1, 2.5, np.inf], labels=["verde", "amarillo", "rojo"]).astype(str)
# three = LogisticRegression().fit(x_train, colour.loc[x_train.index])
# print(classification_report(colour.loc[x_test.index], three.predict(x_test), zero_division=0))
