from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Add any other fields you need for statuses

    def __str__(self):
        return self.name