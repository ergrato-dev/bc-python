# 💻 Ejercicio 01: Lectura y Escritura de Archivos

## 🎯 Objetivo

Dominar las operaciones básicas de lectura y escritura de archivos usando las mejores prácticas de Python moderno.

---

## 📋 Descripción

En este ejercicio aprenderás a:

1. Leer archivos de texto con diferentes encodings
2. Escribir archivos de forma segura
3. Procesar archivos línea por línea
4. Trabajar con `pathlib` para manejo de rutas
5. Procesar archivos CSV y JSON

---

## 🗂️ Estructura

```
01-lectura-escritura/
├── README.md          ← Estás aquí
└── starter/
    └── main.py        ← Código para descomentar
```

---

## 📝 Instrucciones

### Paso 1: Lectura Básica de Archivos

Aprende a leer archivos de texto con encoding explícito.

```python
from pathlib import Path

# SIEMPRE especificar encoding
content = Path("data.txt").read_text(encoding="utf-8")
print(content)
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Escritura de Archivos

Escribe contenido a archivos de forma segura.

```python
from pathlib import Path

# Escritura simple
Path("output.txt").write_text("Hola mundo!", encoding="utf-8")

# Con open() para más control
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Línea 1\n")
    f.write("Línea 2\n")
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: Lectura Línea por Línea

Procesa archivos grandes de manera eficiente.

```python
# Eficiente para archivos grandes
with open("large_file.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip() elimina \n
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: Modos de Apertura

Entiende los diferentes modos de apertura de archivos.

| Modo | Descripción |
|------|-------------|
| `'r'` | Solo lectura (default) |
| `'w'` | Escritura (crea/sobrescribe) |
| `'a'` | Append (agrega al final) |
| `'x'` | Creación exclusiva |

**Descomenta** la sección del Paso 4.

---

### Paso 5: Trabajando con pathlib

Usa `pathlib` para manejo moderno de rutas.

```python
from pathlib import Path

# Crear rutas de forma portable
data_dir = Path("data")
file_path = data_dir / "input.txt"

# Verificar existencia
if file_path.exists():
    content = file_path.read_text(encoding="utf-8")
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Archivos CSV

Procesa archivos CSV con el módulo `csv`.

```python
import csv

# Lectura de CSV como diccionarios
with open("data.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["nombre"], row["email"])
```

**Descomenta** la sección del Paso 6.

---

### Paso 7: Archivos JSON

Trabaja con archivos JSON.

```python
import json

# Lectura
with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Escritura
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**Descomenta** la sección del Paso 7.

---

## ✅ Criterios de Éxito

- [ ] Todos los archivos se abren con `encoding="utf-8"`
- [ ] Usas `with` para todas las operaciones de archivo
- [ ] Los archivos grandes se procesan línea por línea
- [ ] Usas `pathlib` para manejo de rutas
- [ ] Los CSV se leen con `newline=""`

---

## 🚀 Ejecución

```bash
cd bootcamp/week-11/2-ejercicios/01-lectura-escritura/starter
python main.py
```

---

## 📚 Recursos

- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html)
- [pathlib Documentation](https://docs.python.org/3/library/pathlib.html)
- [csv Module](https://docs.python.org/3/library/csv.html)
