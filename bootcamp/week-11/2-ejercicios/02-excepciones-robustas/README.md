# 💻 Ejercicio 02: Excepciones Robustas

## 🎯 Objetivo

Dominar el manejo de excepciones para crear código robusto y resiliente.

---

## 📋 Descripción

En este ejercicio aprenderás a:

1. Capturar excepciones específicas
2. Usar try/except/else/finally correctamente
3. Crear excepciones personalizadas
4. Implementar logging de errores
5. Aplicar patrones de retry

---

## 🗂️ Estructura

```
02-excepciones-robustas/
├── README.md          ← Estás aquí
└── starter/
    └── main.py        ← Código para descomentar
```

---

## 📝 Instrucciones

### Paso 1: Captura de Excepciones Específicas

Siempre captura excepciones específicas, no genéricas.

```python
try:
    value = int(user_input)
except ValueError:
    print("El valor debe ser un número")
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Múltiples Excepciones

Maneja diferentes tipos de errores de forma diferenciada.

```python
try:
    result = data[key] / divisor
except KeyError:
    print("Clave no encontrada")
except ZeroDivisionError:
    print("No se puede dividir por cero")
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: else y finally

Usa `else` para código que solo debe ejecutarse si no hay error, y `finally` para limpieza.

```python
try:
    file = open("data.txt")
except FileNotFoundError:
    print("Archivo no encontrado")
else:
    content = file.read()
    print("Lectura exitosa")
finally:
    print("Operación completada")
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: Excepciones Personalizadas

Crea tus propias excepciones para errores de dominio.

```python
class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: Re-lanzar Excepciones

Loguea y re-lanza excepciones cuando sea necesario.

```python
try:
    process_data()
except Exception as e:
    logger.error(f"Error: {e}")
    raise  # Re-lanza la misma excepción
```

**Descomenta** la sección del Paso 5.

---

## ✅ Criterios de Éxito

- [ ] Capturas excepciones específicas
- [ ] Usas else y finally apropiadamente
- [ ] Creas excepciones personalizadas
- [ ] No silencias errores sin justificación

---

## 🚀 Ejecución

```bash
cd bootcamp/week-11/2-ejercicios/02-excepciones-robustas/starter
python main.py
```
