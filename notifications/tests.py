from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.conf import settings
from notifications.tasks import (
    notify_users_through_sms,
    send_otp,
)

class SMSTestCase(TestCase):
    @patch('notifications.service.BongaSMS')
    def test_send_otp(self, mock_bonga_sms):
        phone_number = "+254708085128"
        otp = "1234"
        message_content = f"Your password reset code is {otp}"
        
        # Mock the BongaSMS instance
        sms_instance = MagicMock()
        mock_bonga_sms.return_value = sms_instance

        # Call the function to send OTP SMS
        send_otp(phone_number, otp, message_content)

        # Assert that the sendOTPSMS method was called with the correct parameters
        sms_instance.sendOTPSMS.assert_called_once_with(message_content, phone_number)

    @patch('notifications.service.BongaSMS')
    def test_notify_users_through_sms(self, mock_bonga_sms):
        message = "Test notification message"
        recipients = ["+254708085128", "+254708085128"]
        kwargs = {}
        
        # Mock the BongaSMS instance
        sms_instance = MagicMock()
        mock_bonga_sms.return_value = sms_instance

        # Call the function to notify users through SMS
        notify_users_through_sms(message, recipients, kwargs)

        # Assert that the send method was called with the correct parameters
        sms_instance.send.assert_called_once_with(message, recipients)
