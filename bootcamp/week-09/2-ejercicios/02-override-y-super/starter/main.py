"""
Ejercicio 02: Override y super()
================================
Practica la sobrescritura de métodos y uso de super().

Instrucciones:
1. Lee cada sección comentada
2. Descomenta el código paso a paso
3. Ejecuta para ver los resultados
"""


# ============================================
# PASO 1: Clase Base Notification
# ============================================
print("=== Paso 1: Clase Base Notification ===")

# Notification es la clase base con métodos que serán sobrescritos
# send() lanza NotImplementedError para forzar override
# Descomenta las siguientes líneas:

# class Notification:
#     """Clase base para todas las notificaciones."""
#
#     def __init__(self, recipient: str, message: str) -> None:
#         self.recipient = recipient
#         self.message = message
#         self.sent = False
#
#     def send(self) -> bool:
#         """Método base - debe ser sobrescrito por subclases."""
#         raise NotImplementedError("Subclasses must implement send()")
#
#     def get_status(self) -> str:
#         """Retorna el estado de la notificación."""
#         status = "✓ Sent" if self.sent else "⏳ Pending"
#         return f"{status}: {self.message[:30]}..."
#
# print("Notification class defined")

print()


# ============================================
# PASO 2: EmailNotification (Override Completo)
# ============================================
print("=== Paso 2: EmailNotification ===")

# EmailNotification sobrescribe send() completamente
# Añade subject como atributo específico de email
# Descomenta las siguientes líneas:

# class EmailNotification(Notification):
#     """Notificación por email."""
#
#     def __init__(
#         self,
#         recipient: str,
#         message: str,
#         subject: str
#     ) -> None:
#         super().__init__(recipient, message)
#         self.subject = subject
#
#     def send(self) -> bool:
#         """Override completo - implementación específica de email."""
#         print(f"📧 Sending email to {self.recipient}")
#         print(f"   Subject: {self.subject}")
#         print(f"   Body: {self.message}")
#         self.sent = True
#         return True
#
# # Probar EmailNotification
# email = EmailNotification(
#     "test@example.com",
#     "Hello from Python!",
#     "Test Email"
# )
# email.send()

print()


# ============================================
# PASO 3: SMSNotification (Override con Validación)
# ============================================
print("=== Paso 3: SMSNotification ===")

# SMSNotification valida el formato del teléfono
# También trunca mensajes largos en __init__
# Descomenta las siguientes líneas:

# class SMSNotification(Notification):
#     """Notificación por SMS con validación."""
#
#     MAX_LENGTH = 160  # Límite estándar de SMS
#
#     def __init__(self, recipient: str, message: str) -> None:
#         # Validar y truncar ANTES de llamar a super()
#         if len(message) > self.MAX_LENGTH:
#             message = message[:self.MAX_LENGTH - 3] + "..."
#         super().__init__(recipient, message)
#
#     def send(self) -> bool:
#         """Override con validación de formato de teléfono."""
#         # Validar formato de teléfono
#         if not self.recipient.startswith("+"):
#             print(f"❌ Invalid phone format: {self.recipient}")
#             print("   Phone must start with +")
#             return False
#
#         print(f"📱 Sending SMS to {self.recipient}")
#         print(f"   Message ({len(self.message)} chars): {self.message}")
#         self.sent = True
#         return True
#
# # Probar con número válido
# sms_valid = SMSNotification("+1234567890", "Your code is 123456")
# sms_valid.send()
#
# print()
#
# # Probar con número inválido
# sms_invalid = SMSNotification("1234567890", "Test message")
# sms_invalid.send()

print()


# ============================================
# PASO 4: PushNotification (Extender con super())
# ============================================
print("=== Paso 4: PushNotification ===")

# PushNotification extiende get_status() usando super()
# No reemplaza, sino que añade información adicional
# Descomenta las siguientes líneas:

# class PushNotification(Notification):
#     """Notificación push con icono personalizado."""
#
#     def __init__(
#         self,
#         recipient: str,
#         message: str,
#         app_name: str,
#         icon: str = "🔔"
#     ) -> None:
#         super().__init__(recipient, message)
#         self.app_name = app_name
#         self.icon = icon
#
#     def send(self) -> bool:
#         """Implementación de push notification."""
#         print(f"{self.icon} Push notification from {self.app_name}")
#         print(f"   To device: {self.recipient}")
#         print(f"   Message: {self.message}")
#         self.sent = True
#         return True
#
#     def get_status(self) -> str:
#         """EXTIENDE get_status() del padre añadiendo icono y app."""
#         # Llamar al método del padre
#         base_status = super().get_status()
#         # Añadir información adicional
#         return f"{self.icon} [{self.app_name}] {base_status}"
#
# # Probar PushNotification
# push = PushNotification(
#     "device_abc123",
#     "New message received",
#     "MyApp",
#     "💬"
# )
# push.send()
# print(f"\nStatus: {push.get_status()}")

print()


# ============================================
# PASO 5: SlackNotification (Override Condicional)
# ============================================
print("=== Paso 5: SlackNotification ===")

# SlackNotification tiene lógica condicional en send()
# Puede mencionar @channel si mention_all es True
# Descomenta las siguientes líneas:

# class SlackNotification(Notification):
#     """Notificación para canal de Slack."""
#
#     def __init__(
#         self,
#         recipient: str,  # Nombre del canal
#         message: str,
#         mention_all: bool = False
#     ) -> None:
#         super().__init__(recipient, message)
#         self.mention_all = mention_all
#
#     def send(self) -> bool:
#         """Override con lógica condicional."""
#         channel = self.recipient
#
#         # Formatear mensaje según configuración
#         if self.mention_all:
#             formatted_msg = f"@channel {self.message}"
#         else:
#             formatted_msg = self.message
#
#         # Validar nombre de canal
#         clean_channel = channel.replace("-", "").replace("_", "")
#         if not clean_channel.isalnum():
#             print(f"❌ Invalid channel name: #{channel}")
#             return False
#
#         print(f"💬 Posting to Slack #{channel}")
#         print(f"   Message: {formatted_msg}")
#         self.sent = True
#         return True
#
# # Probar sin mención
# slack1 = SlackNotification("general", "Daily standup in 5 minutes")
# slack1.send()
#
# print()
#
# # Probar con mención @channel
# slack2 = SlackNotification("alerts", "Server is down!", mention_all=True)
# slack2.send()

print()


# ============================================
# PASO 6: Probar Override de Diferentes Tipos
# ============================================
print("=== Paso 6: Probar Override ===")

# Crear y enviar notificaciones de cada tipo
# Cada una usa SU implementación de send()
# Descomenta las siguientes líneas:

# # Crear notificaciones variadas
# email = EmailNotification(
#     "user@example.com",
#     "Your order has been shipped!",
#     "Order Update"
# )
#
# sms = SMSNotification(
#     "+1234567890",
#     "Your verification code is 123456"
# )
#
# push = PushNotification(
#     "device_token_abc",
#     "New message received",
#     "MyApp",
#     "💬"
# )
#
# slack = SlackNotification(
#     "dev-team",
#     "PR #42 ready for review"
# )
#
# # Enviar todas - cada una usa su implementación
# print("Sending all notifications:\n")
# email.send()
# print()
# sms.send()
# print()
# push.send()
# print()
# slack.send()

print()


# ============================================
# PASO 7: Sistema de Envío Polimórfico
# ============================================
print("=== Paso 7: Sistema Polimórfico ===")

# Función que trabaja con CUALQUIER tipo de Notification
# El polimorfismo permite código genérico y extensible
# Descomenta las siguientes líneas:

# def send_all(notifications: list[Notification]) -> dict[str, int]:
#     """Envía todas las notificaciones y retorna estadísticas."""
#     stats = {"sent": 0, "failed": 0}
#
#     for notification in notifications:
#         print(f"Processing {type(notification).__name__}...")
#         # Cada una usa SU implementación de send()
#         if notification.send():
#             stats["sent"] += 1
#         else:
#             stats["failed"] += 1
#         print()
#
#     return stats
#
#
# # Crear lista mixta de notificaciones
# notifications = [
#     EmailNotification("boss@company.com", "Report attached", "Weekly Report"),
#     SMSNotification("+9876543210", "Meeting reminder"),
#     PushNotification("iphone_xyz", "App update available", "AppStore", "📲"),
#     SMSNotification("invalid_number", "This will fail"),  # Sin +
# ]
#
# # Enviar todas y ver estadísticas
# stats = send_all(notifications)
# print(f"Results: {stats['sent']} sent, {stats['failed']} failed")

print()


# ============================================
# PASO 8: Verificar get_status() Override
# ============================================
print("=== Paso 8: get_status() Override ===")

# PushNotification extiende get_status() con super()
# Las otras clases usan el get_status() base
# Descomenta las siguientes líneas:

# # Crear notificaciones y enviarlas
# notifications = [
#     EmailNotification("test@test.com", "Email test message", "Test"),
#     SMSNotification("+1111111111", "SMS test message"),
#     PushNotification("device", "Push test message", "TestApp", "🔔")
# ]
#
# for n in notifications:
#     n.send()
#
# print("\n" + "=" * 40)
# print("Status de cada notificación:")
# print("=" * 40)
#
# for n in notifications:
#     class_name = type(n).__name__
#     print(f"\n{class_name}:")
#     print(f"  {n.get_status()}")
#
# # Observa cómo PushNotification incluye icono y app_name


print("\n✅ Ejercicio completado!")
