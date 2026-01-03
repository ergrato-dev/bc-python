# 🔍 Ejercicio 03: Validación con Expresiones Regulares

## 📋 Objetivo

Aprender a usar expresiones regulares para validar y extraer datos de texto: emails, teléfonos, URLs, contraseñas y más.

---

## 📚 Conceptos Clave

- Módulo `re` de Python
- Patrones de validación comunes
- Grupos de captura
- `re.match`, `re.search`, `re.findall`, `re.sub`

---

## 🔧 Instrucciones

Abre el archivo `starter/main.py` y descomenta el código paso a paso.

---

## 📝 Pasos

### Paso 1: Validación de Email

Crear validador de emails con regex:

```python
is_valid_email("user@example.com")   # ✅ True
is_valid_email("invalid.email")      # ❌ False
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Validación de Teléfono

Validar diferentes formatos de teléfono:

```python
is_valid_phone("+52 55 1234 5678")   # ✅ True
is_valid_phone("5512345678")          # ✅ True
is_valid_phone("123")                 # ❌ False
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: Validación de Contraseña

Verificar requisitos de seguridad:

```python
# Debe tener: 8+ chars, mayúscula, minúscula, número, especial
is_strong_password("Abc123!@")       # ✅ True
is_strong_password("password")        # ❌ False
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: Extracción de Datos

Extraer información de texto con grupos de captura:

```python
text = "Contact: john@email.com, Tel: 555-1234"
extract_contacts(text)
# [('john@email.com', '555-1234')]
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: Transformación de Texto

Usar `re.sub` para transformar texto:

```python
text = "Mi email es secret@mail.com"
mask_emails(text)
# "Mi email es s*****@mail.com"
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Validador Completo

Crear clase validadora con múltiples reglas:

```python
validator = DataValidator()
result = validator.validate({
    "email": "user@example.com",
    "phone": "555-1234",
    "age": "25"
})
```

**Descomenta** la sección del Paso 6.

---

## ✅ Verificación

```bash
python main.py
```

---

## 🎯 Resultado Esperado

```
=== PASO 1: Email Validation ===
user@example.com     ✅ Valid
test.user@domain.co  ✅ Valid
invalid.email        ❌ Invalid
@nodomain.com        ❌ Invalid

=== PASO 2: Phone Validation ===
+52 55 1234 5678     ✅ Valid
5512345678           ✅ Valid
123                  ❌ Invalid

=== PASO 3: Password Validation ===
SecureP@ss123        ✅ Strong
password             ❌ Weak (missing requirements)

=== PASO 4: Data Extraction ===
Emails found: ['john@email.com', 'jane@company.org']
Phones found: ['555-1234', '(555) 987-6543']

=== PASO 5: Text Transformation ===
Original: Contact me at secret@mail.com
Masked: Contact me at s*****@mail.com

=== PASO 6: Complete Validator ===
Validation results:
  email: ✅ Valid
  phone: ✅ Valid
  age: ✅ Valid (18-120)
```
