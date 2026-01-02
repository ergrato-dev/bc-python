# 🏋️ Ejercicio 02: Slicing Avanzado

## 🎯 Objetivo

Dominar la técnica de slicing en Python para extraer, modificar y manipular secuencias de forma eficiente.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y descomenta el código correspondiente
3. Ejecuta el archivo para verificar que funciona
4. Observa los resultados y comprende cada operación

---

## 📚 Conceptos Cubiertos

### Sintaxis Básica
```
sequence[start:stop:step]
```

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `start` | Índice inicial (incluido) | 0 |
| `stop` | Índice final (excluido) | len(seq) |
| `step` | Incremento entre elementos | 1 |

### Índices Positivos y Negativos
```
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
   0   1   2   3   4   5    ← Positivos
  -6  -5  -4  -3  -2  -1    ← Negativos
```

---

## 🔑 Patrones Comunes

| Expresión | Resultado | Descripción |
|-----------|-----------|-------------|
| `a[2:5]` | Elementos 2,3,4 | Rango básico |
| `a[:3]` | Primeros 3 | Desde inicio |
| `a[3:]` | Desde índice 3 | Hasta final |
| `a[:]` | Copia completa | Todos |
| `a[-3:]` | Últimos 3 | Desde -3 |
| `a[:-2]` | Todo menos últimos 2 | Excluir final |
| `a[::2]` | Cada 2 elementos | Con step |
| `a[::-1]` | Invertir | Step negativo |

---

## ⏱️ Duración Estimada

~45 minutos

---

## ✅ Checklist

- [ ] Paso 1: Slicing básico [start:stop]
- [ ] Paso 2: Omitir start o stop
- [ ] Paso 3: Índices negativos
- [ ] Paso 4: Slicing con step
- [ ] Paso 5: Step negativo (invertir)
- [ ] Paso 6: Slicing con strings
- [ ] Paso 7: Modificar listas con slicing
- [ ] Paso 8: Copiar con slicing
- [ ] Paso 9: Casos de uso comunes
- [ ] Paso 10: Ejercicio integrador

---

[← Volver a Semana 05](../../README.md)
