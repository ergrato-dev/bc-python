"""
Ejercicio 03: Validación con Expresiones Regulares
==================================================

Aprende a validar y extraer datos usando regex.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta para verificar
"""

import re
from typing import NamedTuple


# ============================================
# PASO 1: Validación de Email
# ============================================
print("=== PASO 1: Email Validation ===")

# Patrón de email básico:
# - Usuario: letras, números, puntos, guiones, guiones bajos
# - @
# - Dominio: letras, números, puntos
# - TLD: 2-6 letras

# Descomenta las siguientes líneas:

# EMAIL_PATTERN = re.compile(
#     r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# )
#
#
# def is_valid_email(email: str) -> bool:
#     """Valida formato de email."""
#     return bool(EMAIL_PATTERN.match(email))
#
#
# # Pruebas
# test_emails = [
#     "user@example.com",
#     "test.user@domain.co.uk",
#     "name+tag@gmail.com",
#     "invalid.email",
#     "@nodomain.com",
#     "spaces in@email.com",
#     "user@.com",
# ]
#
# for email in test_emails:
#     status = "✅ Valid" if is_valid_email(email) else "❌ Invalid"
#     print(f"  {email:30} {status}")

print()


# ============================================
# PASO 2: Validación de Teléfono
# ============================================
print("=== PASO 2: Phone Validation ===")

# Patrones de teléfono aceptados:
# - +52 55 1234 5678 (internacional)
# - 55-1234-5678 (con guiones)
# - (55) 1234-5678 (con paréntesis)
# - 5512345678 (solo números)

# Descomenta las siguientes líneas:

# PHONE_PATTERNS = [
#     # Internacional: +XX XX XXXX XXXX
#     re.compile(r"^\+\d{1,3}\s?\d{2,3}\s?\d{4}\s?\d{4}$"),
#     # Con paréntesis: (XX) XXXX-XXXX
#     re.compile(r"^\(\d{2,3}\)\s?\d{4}[-\s]?\d{4}$"),
#     # Con guiones: XX-XXXX-XXXX
#     re.compile(r"^\d{2,3}[-\s]?\d{4}[-\s]?\d{4}$"),
#     # Solo números: 10 dígitos
#     re.compile(r"^\d{10}$"),
# ]
#
#
# def is_valid_phone(phone: str) -> bool:
#     """Valida formato de teléfono."""
#     return any(pattern.match(phone) for pattern in PHONE_PATTERNS)
#
#
# # Pruebas
# test_phones = [
#     "+52 55 1234 5678",
#     "+1 800 555 1234",
#     "(55) 1234-5678",
#     "55-1234-5678",
#     "5512345678",
#     "123",
#     "abc1234567",
# ]
#
# for phone in test_phones:
#     status = "✅ Valid" if is_valid_phone(phone) else "❌ Invalid"
#     print(f"  {phone:20} {status}")

print()


# ============================================
# PASO 3: Validación de Contraseña
# ============================================
print("=== PASO 3: Password Validation ===")

# Requisitos de contraseña segura:
# - Mínimo 8 caracteres
# - Al menos una mayúscula
# - Al menos una minúscula
# - Al menos un número
# - Al menos un carácter especial

# Descomenta las siguientes líneas:

# class PasswordRequirement(NamedTuple):
#     """Requisito de contraseña."""
#     pattern: re.Pattern
#     description: str
#
#
# PASSWORD_REQUIREMENTS = [
#     PasswordRequirement(re.compile(r".{8,}"), "At least 8 characters"),
#     PasswordRequirement(re.compile(r"[A-Z]"), "At least one uppercase"),
#     PasswordRequirement(re.compile(r"[a-z]"), "At least one lowercase"),
#     PasswordRequirement(re.compile(r"\d"), "At least one number"),
#     PasswordRequirement(re.compile(r"[!@#$%^&*(),.?\":{}|<>]"), "At least one special char"),
# ]
#
#
# def check_password_strength(password: str) -> tuple[bool, list[str]]:
#     """
#     Verifica fortaleza de contraseña.
#
#     Returns:
#         (is_strong, missing_requirements)
#     """
#     missing = []
#     for req in PASSWORD_REQUIREMENTS:
#         if not req.pattern.search(password):
#             missing.append(req.description)
#
#     return len(missing) == 0, missing
#
#
# # Pruebas
# test_passwords = [
#     "SecureP@ss123",
#     "Abc123!@",
#     "password",
#     "PASSWORD123",
#     "Short1!",
#     "NoSpecial123",
# ]
#
# for pwd in test_passwords:
#     is_strong, missing = check_password_strength(pwd)
#     if is_strong:
#         print(f"  {pwd:20} ✅ Strong")
#     else:
#         print(f"  {pwd:20} ❌ Weak - Missing: {', '.join(missing)}")

print()


# ============================================
# PASO 4: Extracción de Datos
# ============================================
print("=== PASO 4: Data Extraction ===")

# Usar grupos de captura para extraer información.
# Los paréntesis () crean grupos que podemos recuperar.

# Descomenta las siguientes líneas:

# def extract_emails(text: str) -> list[str]:
#     """Extrae todos los emails de un texto."""
#     pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
#     return re.findall(pattern, text)
#
#
# def extract_phones(text: str) -> list[str]:
#     """Extrae todos los teléfonos de un texto."""
#     pattern = r"\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}"
#     return re.findall(pattern, text)
#
#
# def extract_urls(text: str) -> list[str]:
#     """Extrae URLs de un texto."""
#     pattern = r"https?://[^\s<>\"']+"
#     return re.findall(pattern, text)
#
#
# # Texto de prueba
# sample_text = """
# Contact us:
# - Email: john@example.com or support@company.org
# - Phone: +1 555-123-4567 or (55) 9876-5432
# - Website: https://example.com and http://test.org/page
# """
#
# print(f"Emails found: {extract_emails(sample_text)}")
# print(f"Phones found: {extract_phones(sample_text)}")
# print(f"URLs found: {extract_urls(sample_text)}")
#
#
# # Extracción con grupos nombrados
# def parse_log_entry(line: str) -> dict | None:
#     """Parsea entrada de log con formato: [DATE] LEVEL: message"""
#     pattern = r"\[(?P<date>[^\]]+)\]\s+(?P<level>\w+):\s+(?P<message>.+)"
#     match = re.match(pattern, line)
#     if match:
#         return match.groupdict()
#     return None
#
#
# log_line = "[2024-01-15 10:30:45] ERROR: Connection timeout"
# parsed = parse_log_entry(log_line)
# print(f"\nParsed log: {parsed}")

print()


# ============================================
# PASO 5: Transformación de Texto
# ============================================
print("=== PASO 5: Text Transformation ===")

# re.sub() reemplaza patrones en texto.
# Puede usar funciones para transformaciones complejas.

# Descomenta las siguientes líneas:

# def mask_email(text: str) -> str:
#     """Enmascara emails en texto (user@domain -> u***@domain)."""
#     def replacer(match: re.Match) -> str:
#         email = match.group(0)
#         user, domain = email.split("@")
#         masked_user = user[0] + "*" * (len(user) - 1)
#         return f"{masked_user}@{domain}"
#
#     pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
#     return re.sub(pattern, replacer, text)
#
#
# def mask_phone(text: str) -> str:
#     """Enmascara teléfonos dejando últimos 4 dígitos."""
#     def replacer(match: re.Match) -> str:
#         phone = match.group(0)
#         digits = re.sub(r"\D", "", phone)  # Solo dígitos
#         return "*" * (len(digits) - 4) + digits[-4:]
#
#     pattern = r"\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}"
#     return re.sub(pattern, replacer, text)
#
#
# def normalize_whitespace(text: str) -> str:
#     """Normaliza espacios en blanco múltiples a uno solo."""
#     return re.sub(r"\s+", " ", text).strip()
#
#
# # Pruebas
# text1 = "Contact: secret.user@private.com for info"
# print(f"Original: {text1}")
# print(f"Masked:   {mask_email(text1)}")
#
# text2 = "Call me at +52 55 1234 5678"
# print(f"\nOriginal: {text2}")
# print(f"Masked:   {mask_phone(text2)}")
#
# text3 = "Too    many     spaces   here"
# print(f"\nOriginal: '{text3}'")
# print(f"Normalized: '{normalize_whitespace(text3)}'")

print()


# ============================================
# PASO 6: Validador Completo
# ============================================
print("=== PASO 6: Complete Validator ===")

# Crear clase validadora que combina múltiples reglas.

# Descomenta las siguientes líneas:

# from dataclasses import dataclass, field
#
#
# @dataclass
# class ValidationResult:
#     """Resultado de validación."""
#     field: str
#     is_valid: bool
#     message: str
#
#
# class DataValidator:
#     """Validador de datos con múltiples reglas regex."""
#
#     # Patrones predefinidos
#     PATTERNS = {
#         "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
#         "phone": re.compile(r"^\+?\d{10,15}$"),
#         "username": re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$"),
#         "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
#         "time": re.compile(r"^\d{2}:\d{2}(:\d{2})?$"),
#         "url": re.compile(r"^https?://[^\s<>\"']+$"),
#         "integer": re.compile(r"^-?\d+$"),
#         "decimal": re.compile(r"^-?\d+\.?\d*$"),
#     }
#
#     def validate_field(
#         self,
#         name: str,
#         value: str,
#         pattern_name: str
#     ) -> ValidationResult:
#         """Valida un campo contra un patrón."""
#         pattern = self.PATTERNS.get(pattern_name)
#         if not pattern:
#             return ValidationResult(name, False, f"Unknown pattern: {pattern_name}")
#
#         is_valid = bool(pattern.match(value))
#         message = "Valid" if is_valid else f"Invalid {pattern_name} format"
#         return ValidationResult(name, is_valid, message)
#
#     def validate_range(
#         self,
#         name: str,
#         value: str,
#         min_val: int,
#         max_val: int
#     ) -> ValidationResult:
#         """Valida que un número esté en rango."""
#         if not self.PATTERNS["integer"].match(value):
#             return ValidationResult(name, False, "Must be an integer")
#
#         num = int(value)
#         is_valid = min_val <= num <= max_val
#         message = f"Valid ({min_val}-{max_val})" if is_valid else f"Out of range ({min_val}-{max_val})"
#         return ValidationResult(name, is_valid, message)
#
#
# # Usar el validador
# validator = DataValidator()
#
# # Validar datos de formulario
# form_data = {
#     "email": "user@example.com",
#     "phone": "+5215512345678",
#     "username": "john_doe",
#     "age": "25",
#     "website": "https://mysite.com",
# }
#
# print("Validation results:")
# print(f"  email: {validator.validate_field('email', form_data['email'], 'email')}")
# print(f"  phone: {validator.validate_field('phone', form_data['phone'], 'phone')}")
# print(f"  username: {validator.validate_field('username', form_data['username'], 'username')}")
# print(f"  age: {validator.validate_range('age', form_data['age'], 18, 120)}")
# print(f"  website: {validator.validate_field('website', form_data['website'], 'url')}")

print()


# ============================================
# RESUMEN
# ============================================
print("=" * 50)
print("RESUMEN DE REGEX")
print("=" * 50)
print(r"""
Metacaracteres comunes:
  \d  - Dígito [0-9]
  \w  - Word char [a-zA-Z0-9_]
  \s  - Whitespace
  .   - Cualquier char
  ^   - Inicio de string
  $   - Fin de string

Cuantificadores:
  *   - 0 o más
  +   - 1 o más
  ?   - 0 o 1
  {n} - Exactamente n
  {n,m} - Entre n y m

Funciones re:
  re.match()   - Busca al inicio
  re.search()  - Busca en cualquier parte
  re.findall() - Encuentra todos
  re.sub()     - Reemplaza

Tip: Usa re.compile() para patrones reutilizables
""")
