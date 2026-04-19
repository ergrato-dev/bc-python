"""
Tests para NotificationService usando mocking.

Ejercicio: Descomenta cada sección para mejorar la cobertura.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

from src.notification import (
    NotificationService,
    Notification,
    NotificationChannel,
)


# ============================================
# PASO 7: Tests de Notificaciones
# ============================================
print("--- Paso 7: Tests de notificaciones ---")

# Descomenta las siguientes líneas:
# class TestNotification:
#     """Tests para la clase Notification."""
#
#     def test_notification_not_sent_initially(self):
#         """Test que una notificación nueva no está enviada."""
#         notification = Notification(
#             recipient="user@example.com",
#             subject="Test",
#             message="Hello",
#             channel=NotificationChannel.EMAIL,
#         )
#
#         assert notification.is_sent is False
#         assert notification.sent_at is None
#
#     def test_notification_is_sent_after_setting_sent_at(self):
#         """Test que is_sent es True después de setear sent_at."""
#         notification = Notification(
#             recipient="user@example.com",
#             subject="Test",
#             message="Hello",
#             channel=NotificationChannel.EMAIL,
#         )
#         notification.sent_at = datetime.now()
#
#         assert notification.is_sent is True


# class TestNotificationServiceEmail:
#     """Tests para envío de emails."""
#
#     @patch("src.notification.smtplib.SMTP")
#     def test_send_email_success(self, mock_smtp, notification_service):
#         """Test envío de email exitoso."""
#         # Configurar mock del servidor SMTP
#         mock_server = MagicMock()
#         mock_smtp.return_value.__enter__.return_value = mock_server
#
#         notification = Notification(
#             recipient="user@example.com",
#             subject="Test Subject",
#             message="Test message",
#             channel=NotificationChannel.EMAIL,
#         )
#
#         result = notification_service.send(notification)
#
#         assert result is True
#         assert notification.is_sent
#         mock_server.send_message.assert_called_once()
#
#     @patch("src.notification.smtplib.SMTP")
#     def test_send_email_failure(self, mock_smtp, notification_service):
#         """Test que retorna False si falla el envío."""
#         import smtplib
#         mock_smtp.return_value.__enter__.side_effect = smtplib.SMTPException("Error")
#
#         notification = Notification(
#             recipient="user@example.com",
#             subject="Test",
#             message="Message",
#             channel=NotificationChannel.EMAIL,
#         )
#
#         result = notification_service.send(notification)
#
#         assert result is False
#         assert not notification.is_sent


# class TestNotificationServiceSMS:
#     """Tests para envío de SMS."""
#
#     @patch("src.notification.requests.post")
#     def test_send_sms_success(self, mock_post, notification_service):
#         """Test envío de SMS exitoso."""
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_post.return_value = mock_response
#
#         notification = Notification(
#             recipient="+1234567890",
#             subject="SMS",
#             message="Test SMS",
#             channel=NotificationChannel.SMS,
#         )
#
#         result = notification_service.send(notification)
#
#         assert result is True
#         mock_post.assert_called_once()
#
#     @patch("src.notification.requests.post")
#     def test_send_sms_api_error(self, mock_post, notification_service):
#         """Test que maneja errores de API de SMS."""
#         mock_response = Mock()
#         mock_response.status_code = 500
#         mock_post.return_value = mock_response
#
#         notification = Notification(
#             recipient="+1234567890",
#             subject="SMS",
#             message="Test",
#             channel=NotificationChannel.SMS,
#         )
#
#         result = notification_service.send(notification)
#
#         assert result is False
#
#     def test_send_sms_without_api_key_raises(self):
#         """Test que SMS sin API key lanza error."""
#         service = NotificationService(sms_api_key=None)
#
#         notification = Notification(
#             recipient="+1234567890",
#             subject="SMS",
#             message="Test",
#             channel=NotificationChannel.SMS,
#         )
#
#         with pytest.raises(ValueError, match="SMS API key not configured"):
#             service.send(notification)


# class TestNotificationServicePush:
#     """Tests para push notifications."""
#
#     @patch("src.notification.requests.post")
#     def test_send_push_success(self, mock_post, notification_service):
#         """Test envío de push exitoso."""
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_post.return_value = mock_response
#
#         notification = Notification(
#             recipient="device-token-123",
#             subject="Push Title",
#             message="Push body",
#             channel=NotificationChannel.PUSH,
#         )
#
#         result = notification_service.send(notification)
#
#         assert result is True
#
#     @patch("src.notification.requests.post")
#     def test_send_push_network_error(self, mock_post, notification_service):
#         """Test que maneja errores de red en push."""
#         import requests
#         mock_post.side_effect = requests.ConnectionError()
#
#         notification = Notification(
#             recipient="device-token",
#             subject="Push",
#             message="Test",
#             channel=NotificationChannel.PUSH,
#         )
#
#         result = notification_service.send(notification)
#
#         assert result is False


# class TestNotificationServiceHistory:
#     """Tests para el historial de notificaciones."""
#
#     @patch("src.notification.smtplib.SMTP")
#     def test_get_sent_count(self, mock_smtp, notification_service):
#         """Test contador de notificaciones enviadas."""
#         mock_server = MagicMock()
#         mock_smtp.return_value.__enter__.return_value = mock_server
#
#         # Enviar 3 notificaciones
#         for i in range(3):
#             notification = Notification(
#                 recipient=f"user{i}@example.com",
#                 subject="Test",
#                 message="Message",
#                 channel=NotificationChannel.EMAIL,
#             )
#             notification_service.send(notification)
#
#         assert notification_service.get_sent_count() == 3
#
#     @patch("src.notification.smtplib.SMTP")
#     @patch("src.notification.requests.post")
#     def test_get_sent_by_channel(self, mock_post, mock_smtp, notification_service):
#         """Test filtrar por canal."""
#         mock_server = MagicMock()
#         mock_smtp.return_value.__enter__.return_value = mock_server
#         mock_response = Mock(status_code=200)
#         mock_post.return_value = mock_response
#
#         # Enviar emails
#         for i in range(2):
#             notification_service.send(Notification(
#                 recipient=f"user{i}@example.com",
#                 subject="Email",
#                 message="Test",
#                 channel=NotificationChannel.EMAIL,
#             ))
#
#         # Enviar SMS
#         notification_service.send(Notification(
#             recipient="+123",
#             subject="SMS",
#             message="Test",
#             channel=NotificationChannel.SMS,
#         ))
#
#         emails = notification_service.get_sent_by_channel(NotificationChannel.EMAIL)
#         sms = notification_service.get_sent_by_channel(NotificationChannel.SMS)
#
#         assert len(emails) == 2
#         assert len(sms) == 1
#
#     def test_clear_history(self, notification_service):
#         """Test limpiar historial."""
#         notification_service._sent_notifications = [Mock(), Mock()]
#
#         notification_service.clear_history()
#
#         assert notification_service.get_sent_count() == 0
