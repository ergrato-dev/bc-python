"""Ejercicio 04 · Agrupar y reducir: KMeans y PCA, sin respuestas que acertar.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

print("Ejercicio 04 · Agrupar y reducir")

# Cuarenta sensores de PM2.5, cada uno con su perfil: la media de cada hora del día. Hay
# tres tipos de sitio, pero el archivo no lo dice: junto a una avenida (dos picos, al ir y
# al volver del trabajo), en un barrio (un pico por la noche, calefacciones y cocinas) y
# en un parque (bajo y plano).
rng = np.random.default_rng(33)
hours = np.arange(24)


def peak(center: float, width: float) -> np.ndarray:
    return np.exp(-(((hours - center) / width) ** 2))


shapes = {
    "avenida": 15 + 20 * peak(8, 1.5) + 18 * peak(19, 1.5),
    "barrio": 12 + 16 * peak(21, 2.5),
    "parque": 9 + 2 * peak(14, 4),
}
kinds = rng.choice(list(shapes), 40)
profiles = pd.DataFrame(
    [shapes[kind] * rng.uniform(0.8, 1.2) + rng.normal(0, 1.5, 24) for kind in kinds],
    index=[f"sensor {number:02}" for number in range(1, 41)],
    columns=[f"h{hour:02}" for hour in hours],
).round(1)
print(f"{profiles.shape[0]} sensores · {profiles.shape[1]} horas por perfil")


# ============================================
# PASO 1: Mirar los perfiles
# ============================================
# Descomenta las siguientes líneas:
# print(profiles[["h03", "h08", "h14", "h19", "h21"]].head(6).to_string())


# ============================================
# PASO 2: Tres grupos
# ============================================
# Descomenta las siguientes líneas:
# kmeans = KMeans(3, n_init=10, random_state=33)
# groups = kmeans.fit_predict(profiles)
# print(pd.crosstab(pd.Series(kinds, name="sitio"), pd.Series(groups, name="grupo")).to_string())


# ============================================
# PASO 3: ¿Cuántos grupos?
# ============================================
# Descomenta las siguientes líneas:
# for k in range(2, 7):
#     model = KMeans(k, n_init=10, random_state=33).fit(profiles)
#     silhouette = silhouette_score(profiles, model.labels_)
#     print(f"k={k} · inercia {model.inertia_:7.0f} · silueta {silhouette:.2f}")


# ============================================
# PASO 4: Una columna en otra escala
# ============================================
# Descomenta las siguientes líneas:
# height = profiles.assign(altitud=rng.uniform(0, 2500, 40).round())
# for name, model in [
#     ("sin escalar", KMeans(3, n_init=10, random_state=33)),
#     ("escalando", make_pipeline(StandardScaler(), KMeans(3, n_init=10, random_state=33))),
# ]:
#     found = model.fit_predict(height)
#     table = pd.crosstab(pd.Series(kinds, name="sitio"), pd.Series(found, name="grupo"))
#     print(f"{name}:\n{table.to_string()}")


# ============================================
# PASO 5: De 24 columnas a 2
# ============================================
# Descomenta las siguientes líneas:
# pca = PCA(n_components=5).fit(profiles)
# print("varianza explicada:", pca.explained_variance_ratio_.round(3))
# plane = pd.DataFrame(pca.transform(profiles)[:, :2], columns=["pc1", "pc2"])
# print(plane.groupby(kinds).mean().round(1).to_string())


# ============================================
# PASO 6: Grupos en el ruido
# ============================================
# Descomenta las siguientes líneas:
# flat = pd.DataFrame(rng.normal(20, 3, (40, 24)), columns=profiles.columns)
# found = KMeans(3, n_init=10, random_state=33).fit_predict(flat)
# silhouette = silhouette_score(flat, found)
# print(f"ruido: grupos de {np.bincount(found).tolist()} sensores · silueta {silhouette:.2f}")
