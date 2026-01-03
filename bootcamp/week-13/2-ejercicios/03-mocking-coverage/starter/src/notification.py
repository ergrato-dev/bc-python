"""
Servicio de notificaciones.

Simula un sistema que envía notificaciones por diferentes canales.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import smtplib
from email.message import EmailMessage


class NotificationChannel(Enum):
    """Canales de notificación disponibles."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


@dataclass
class Notification:
    """Representa una notificación."""

    recipient: str
    subject: str
    message: str
    channel: NotificationChannel
    sent_at: datetime | None = None

    @property
    def is_sent(self) -> bool:
        """Retorna True si la notificación fue enviada."""
        return self.sent_at is not None


class NotificationService:
    """Servicio para enviar notificaciones."""

    def __init__(
        self,
        smtp_host: str = "localhost",
        smtp_port: int = 587,
        sms_api_key: str | None = None,
    ) -> None:
        """
        Inicializa el servicio de notificaciones.

        Args:
            smtp_host: Host del servidor SMTP
            smtp_port: Puerto del servidor SMTP
            sms_api_key: API key para servicio de SMS
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sms_api_key = sms_api_key
        self._sent_notifications: list[Notification] = []

    def send(self, notification: Notification) -> bool:
        """
        Envía una notificación por el canal especificado.

        Args:
            notification: La notificación a enviar

        Returns:
            True si se envió correctamente

        Raises:
            ValueError: Si el canal no está soportado
            NotificationError: Si falla el envío
        """
        match notification.channel:
            case NotificationChannel.EMAIL:
                success = self._send_email(notification)
            case NotificationChannel.SMS:
                success = self._send_sms(notification)
            case NotificationChannel.PUSH:
                success = self._send_push(notification)
            case _:
                raise ValueError(f"Unsupported channel: {notification.channel}")

        if success:
            notification.sent_at = datetime.now()
            self._sent_notifications.append(notification)

        return success

    def _send_email(self, notification: Notification) -> bool:
        """Envía notificación por email."""
        try:
            msg = EmailMessage()
            msg["Subject"] = notification.subject
            msg["To"] = notification.recipient
            msg["From"] = "noreply@example.com"
            msg.set_content(notification.message)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.send_message(msg)

            return True
        except smtplib.SMTPException:
            return False

    def _send_sms(self, notification: Notification) -> bool:
        """Envía notificación por SMS."""
        if not self.sms_api_key:
            raise ValueError("SMS API key not configured")

        # Simulación de llamada a API de SMS
        # En producción, esto llamaría a Twilio, AWS SNS, etc.
        import requests

        try:
            response = requests.post(
                "https://api.sms.example.com/send",
                json={
                    "to": notification.recipient,
                    "message": notification.message,
                    "api_key": self.sms_api_key,
                },
                timeout=10,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _send_push(self, notification: Notification) -> bool:
        """Envía notificación push."""
        # Simulación de push notification
        # En producción, esto usaría Firebase, APNs, etc.
        import requests

        try:
            response = requests.post(
                "https://api.push.example.com/notify",
                json={
                    "device_token": notification.recipient,
                    "title": notification.subject,
                    "body": notification.message,
                },
                timeout=10,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_sent_count(self) -> int:
        """Retorna el número de notificaciones enviadas."""
        return len(self._sent_notifications)

    def get_sent_by_channel(self, channel: NotificationChannel) -> list[Notification]:
        """Retorna notificaciones enviadas por un canal específico."""
        return [n for n in self._sent_notifications if n.channel == channel]

    def clear_history(self) -> None:
        """Limpia el historial de notificaciones enviadas."""
        self._sent_notifications.clear()
