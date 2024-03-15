from __future__ import unicode_literals, absolute_import
from .service import BongaSMS

from constance import config
from django.conf import settings



# @shared_task(name='notify_users_through_sms')
def notify_users_through_sms(message: str, recipients: list, kwargs, reply=False):
    if not config.USE_BONGA:
        return
    
    sms = BongaSMS()
    if reply:
        sms.reply(message, recipients, kwargs)
    sms.send(message, recipients)

# @shared_task()
def send_otp(phone, otp, message=None):
    phone_number = phone.lstrip('+')
    message_content = message or f"Your password reset code is {otp}"
    
    if config.USE_BONGA:
        sms = BongaSMS()
        sms.sendOTPSMS(message_content, phone_number)





