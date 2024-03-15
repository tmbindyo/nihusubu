from constance import config
from django.conf import settings

from .models import SMS, DeliveryReports
from authentication.models import User

import logging
import requests

# logger = logging.getLogger('sms-logger')

class BongaSMS:
    def __init__(self):
        self.url = config.OUTGOING_BONGA_SMS_URL
        self.outgoing_client_id = config.OUTGOING_BONGA_SMS_CLIENT_ID
        self.outgoing_api_key = config.OUTGOING_BONGA_SMS_API_KEY
        self.outgoing_secret = config.OUTGOING_BONGA_SMS_SECRET
        self.outgoing_service_id = config.OUTGOING_BONGA_SMS_SERVICE_ID

    def sendOTPSMS(self, message, phone):
        payload = self._build_payload(message, phone)
        self._send(payload)

    def send(self, message, recipients):
        if not isinstance(recipients, list):
            recipients = [recipients]
        for msisdn in recipients:
            if len(msisdn) > 8:
                payload = self._build_payload(message, msisdn)
                self._send(payload)
                is_user = User.objects.filter(phone_number=msisdn).first()
                if is_user:
                    SMS.objects.create(message=payload['txtMessage'], user=is_user, msisdn=msisdn)

    def _build_payload(self, message, msisdn):
        return {
            "apiClientID": self.outgoing_client_id,
            "key": self.outgoing_api_key,
            "secret": self.outgoing_secret,
            "txtMessage": message,
            "MSISDN": msisdn,
            "serviceID": self.outgoing_service_id,
        }

    def _send(self, payload):
        url = self.url
        SMS.objects.create(message=payload['txtMessage'], msisdn=payload['MSISDN'])
        res = requests.post(url, payload)
        if res.status_code == 200:
            data = res.json()
            DeliveryReports.objects.create(
                msisdn=payload['MSISDN'],
                callback_identifier=data.get("unique_id"),
                status=data.get("status", "Sent"),
                message=data.get("status_message", "")
            )
            if data.get("status") == 222:
                # logger.info(f'BongaSMS: Successfully sent message to: {payload["MSISDN"]} =>'
                #             f' identifier: {data["unique_id"]}')
                pass
            else:
                # logger.info(f'BongaSMS: Failed to send to: {payload["MSISDN"]}')
                pass
        else:
            # logger.error(f'BongaSMS: Failed to send SMS: {res.status_code}')
            pass
