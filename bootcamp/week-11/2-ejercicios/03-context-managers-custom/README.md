# 💻 Ejercicio 03: Context Managers Personalizados

## 🎯 Objetivo

Aprender a crear context managers propios para gestionar recursos de forma segura.

---

## 📋 Descripción

En este ejercicio aprenderás a:

1. Implementar `__enter__` y `__exit__`
2. Usar el decorador `@contextmanager`
3. Manejar excepciones en context managers
4. Crear context managers reutilizables

---

## 🗂️ Estructura

```
03-context-managers-custom/
├── README.md          ← Estás aquí
└── starter/
    └── main.py        ← Código para descomentar
```

---

## 📝 Instrucciones

### Paso 1: Context Manager con Clase

Implementa `__enter__` y `__exit__` para crear un context manager.

```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        return False  # No suprimir excepciones
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: @contextmanager

Usa el decorador para crear context managers más simples.

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name}: {time.time() - start:.2f}s")
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: Manejo de Recursos

Crea context managers que gestionen recursos correctamente.

**Descomenta** la sección del Paso 3.

---

### Paso 4: Context Managers Anidados

Combina múltiples context managers.

**Descomenta** la sección del Paso 4.

---

## ✅ Criterios de Éxito

- [ ] Implementas `__enter__` y `__exit__` correctamente
- [ ] Usas `try/finally` en `@contextmanager`
- [ ] No suprimes excepciones sin motivo
- [ ] Garantizas liberación de recursos

---

## 🚀 Ejecución

```bash
cd bootcamp/week-11/2-ejercicios/03-context-managers-custom/starter
python main.py
```
