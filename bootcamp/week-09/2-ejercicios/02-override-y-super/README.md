# 🔄 Ejercicio 02: Override y super()

## 🎯 Objetivo

Practicar la sobrescritura (override) de métodos y el uso de `super()` para extender funcionalidad de clases padre.

---

## 📋 Instrucciones

En este ejercicio crearás un sistema de notificaciones donde diferentes canales sobrescriben el método de envío.

### Paso 1: Clase Base Notification

Define la clase padre con el método que será sobrescrito.

```python
class Notification:
    def __init__(self, recipient: str, message: str) -> None:
        self.recipient = recipient
        self.message = message
        self.sent = False

    def send(self) -> bool:
        """Método base - debe ser sobrescrito."""
        raise NotImplementedError("Subclasses must implement send()")

    def get_status(self) -> str:
        status = "✓ Sent" if self.sent else "⏳ Pending"
        return f"{status}: {self.message[:30]}..."
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: EmailNotification (Override Completo)

Sobrescribe `send()` completamente con implementación específica de email.

```python
class EmailNotification(Notification):
    def __init__(
        self,
        recipient: str,
        message: str,
        subject: str
    ) -> None:
        super().__init__(recipient, message)
        self.subject = subject

    def send(self) -> bool:
        """Override completo - implementación de email."""
        print(f"📧 Sending email to {self.recipient}")
        print(f"   Subject: {self.subject}")
        print(f"   Body: {self.message}")
        self.sent = True
        return True
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: SMSNotification (Override con Validación)

Sobrescribe `send()` añadiendo validación específica de SMS.

```python
class SMSNotification(Notification):
    MAX_LENGTH = 160

    def __init__(self, recipient: str, message: str) -> None:
        # Validar longitud antes de inicializar
        if len(message) > self.MAX_LENGTH:
            message = message[:self.MAX_LENGTH - 3] + "..."
        super().__init__(recipient, message)

    def send(self) -> bool:
        """Override con validación de formato de teléfono."""
        if not self.recipient.startswith("+"):
            print(f"❌ Invalid phone format: {self.recipient}")
            return False

        print(f"📱 Sending SMS to {self.recipient}")
        print(f"   Message ({len(self.message)} chars): {self.message}")
        self.sent = True
        return True
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: PushNotification (Extender con super())

Usa `super()` para extender funcionalidad en lugar de reemplazarla.

```python
class PushNotification(Notification):
    def __init__(
        self,
        recipient: str,
        message: str,
        app_name: str,
        icon: str = "🔔"
    ) -> None:
        super().__init__(recipient, message)
        self.app_name = app_name
        self.icon = icon

    def send(self) -> bool:
        """Override que EXTIENDE la funcionalidad base."""
        print(f"{self.icon} Push notification from {self.app_name}")
        print(f"   To device: {self.recipient}")
        print(f"   Message: {self.message}")
        self.sent = True
        return True

    def get_status(self) -> str:
        """Extiende get_status() añadiendo el icono."""
        base_status = super().get_status()
        return f"{self.icon} [{self.app_name}] {base_status}"
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: SlackNotification (Override Condicional)

Sobrescribe con lógica condicional basada en el contenido.

```python
class SlackNotification(Notification):
    def __init__(
        self,
        recipient: str,  # Canal de Slack
        message: str,
        mention_all: bool = False
    ) -> None:
        super().__init__(recipient, message)
        self.mention_all = mention_all

    def send(self) -> bool:
        """Override con lógica condicional."""
        channel = self.recipient

        # Añadir mención si está habilitada
        if self.mention_all:
            formatted_msg = f"@channel {self.message}"
        else:
            formatted_msg = self.message

        print(f"💬 Posting to Slack #{channel}")
        print(f"   Message: {formatted_msg}")

        # Simular verificación de canal
        if not channel.replace("-", "").replace("_", "").isalnum():
            print(f"   ❌ Invalid channel name")
            return False

        self.sent = True
        return True
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Probar Override

Crea instancias y verifica que cada clase usa su propia implementación.

```python
# Crear notificaciones de cada tipo
email = EmailNotification(
    "user@example.com",
    "Your order has been shipped!",
    "Order Update"
)

sms = SMSNotification(
    "+1234567890",
    "Your verification code is 123456"
)

push = PushNotification(
    "device_token_abc",
    "New message received",
    "MyApp",
    "💬"
)

# Enviar todas
email.send()
sms.send()
push.send()
```

**Descomenta** la sección del Paso 6.

---

### Paso 7: Sistema de Envío Polimórfico

Crea una función que envíe cualquier tipo de notificación.

```python
def send_all(notifications: list[Notification]) -> dict[str, int]:
    """Envía todas las notificaciones y retorna estadísticas."""
    stats = {"sent": 0, "failed": 0}

    for notification in notifications:
        if notification.send():  # Cada una usa SU implementación
            stats["sent"] += 1
        else:
            stats["failed"] += 1

    return stats
```

**Descomenta** la sección del Paso 7.

---

### Paso 8: Verificar get_status() Override

Observa cómo `PushNotification` extiende `get_status()`.

```python
notifications = [email, sms, push]

print("\nStatus de cada notificación:")
for n in notifications:
    print(f"  {n.get_status()}")

# PushNotification muestra el icono y app_name
# Las otras usan el get_status() base
```

**Descomenta** la sección del Paso 8.

---

## ✅ Resultado Esperado

```
=== Paso 6: Probar Override ===
📧 Sending email to user@example.com
   Subject: Order Update
   Body: Your order has been shipped!

📱 Sending SMS to +1234567890
   Message (36 chars): Your verification code is 123456

💬 Push notification from MyApp
   To device: device_token_abc
   Message: New message received

=== Paso 8: get_status() Override ===
Status de cada notificación:
  ✓ Sent: Your order has been shipped...
  ✓ Sent: Your verification code is 123...
  💬 [MyApp] ✓ Sent: New message received...
```

---

## 🔑 Conceptos Clave

| Patrón | Descripción | Uso |
|--------|-------------|-----|
| **Override completo** | Reemplaza totalmente el método padre | Email, SMS |
| **Override con super()** | Extiende la funcionalidad | PushNotification.get_status() |
| **Override condicional** | Añade lógica antes/después | SlackNotification |
| **Validación en __init__** | Modifica datos antes de super() | SMSNotification |

---

## 🔗 Siguiente

Continúa con [03-polimorfismo](../03-polimorfismo/) para practicar polimorfismo y duck typing.
