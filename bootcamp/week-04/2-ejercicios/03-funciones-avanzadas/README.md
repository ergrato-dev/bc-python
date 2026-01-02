# 🏋️ Ejercicio 03: Funciones Avanzadas

## 🎯 Objetivo

Practicar conceptos avanzados de funciones: `*args`, `**kwargs`, scope de variables y closures básicos.

---

## 📋 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y descomenta el código correspondiente
3. Ejecuta el archivo para verificar los resultados
4. Compara tu output con el esperado

---

## 📚 Conceptos Cubiertos

- `*args` para argumentos posicionales variables
- `**kwargs` para argumentos keyword variables
- Desempaquetado con `*` y `**`
- Scope de variables (LEGB)
- `global` y `nonlocal`
- Closures básicos
- Funciones como objetos

---

## ✅ Resultado Esperado

```
=== PASO 1: *args Básico ===
Suma de 1, 2: 3
Suma de 1, 2, 3, 4, 5: 15
Suma de ninguno: 0
Args es tipo: <class 'tuple'>

=== PASO 2: *args con Parámetros Regulares ===
[INFO] Sistema iniciado
[WARNING] Memoria baja, Disco lleno
[ERROR] Conexión perdida

=== PASO 3: **kwargs Básico ===
name: Ana
age: 25
city: Madrid
---
role: developer
Kwargs es tipo: <class 'dict'>

=== PASO 4: Combinar *args y **kwargs ===
[INFO] {tags: auth,login}
[DEBUG] {user_id: 123, ip: 192.168.1.1}

=== PASO 5: Desempaquetado en Llamadas ===
Suma: 6
Saludo: Hello, Alice!

=== PASO 6: Scope - Variables Locales ===
Dentro: local
Fuera: global

=== PASO 7: La Palabra global ===
Antes: 0
Después de incrementar: 3

=== PASO 8: Closure Básico ===
Doble de 5: 10
Triple de 5: 15
Doble de 10: 20

=== PASO 9: Closure con Estado ===
Contador 1: 1
Contador 1: 2
Contador 1: 3
Contador 2: 1

=== PASO 10: Funciones como Objetos ===
Con add: 15
Con multiply: 50
Operaciones: [15, 50]
```

---

## 🚀 Ejecución

```bash
cd bootcamp/week-04/2-ejercicios/03-funciones-avanzadas/starter
python main.py
```

---

## 💡 Tips

- `*args` captura argumentos posicionales extra como **tupla**
- `**kwargs` captura argumentos keyword extra como **diccionario**
- `*lista` desempaqueta una lista en argumentos posicionales
- `**dict` desempaqueta un diccionario en argumentos keyword
- Un closure "recuerda" variables del scope donde fue creado
- Las funciones son objetos: puedes pasarlas como argumentos

---

## 📖 Referencia

- [Teoría: Parámetros Avanzados](../../1-teoria/04-parametros-avanzados.md)
- [Teoría: Return y Scope](../../1-teoria/05-return-scope.md)
