import uuid
from django.db import models
from authentication.models import User

# Create your models here.



class SMS(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    msisdn = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    message = models.TextField(help_text='What you want the customers message notification to read')
    # Indicates which user triggered the SMS notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sent_on = models.DateTimeField(auto_now=True, verbose_name='sent on')

    class Meta:
        ordering = ['-sent_on']
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS'

    def __str__(self):
        return f'{self.message}'

class DeliveryReports(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, primary_key=True)
    callback_identifier = models.CharField(max_length=100, null=True)
    msisdn = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    message = models.CharField(max_length=200, null=True, blank=True)
    added_on = models.DateTimeField(auto_now=True, verbose_name='sent on')

    def __str__(self):
        return f'{self.msisdn}'