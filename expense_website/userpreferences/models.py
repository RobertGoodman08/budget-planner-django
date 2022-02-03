from django.db import models
from django.contrib.auth.models import User


class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True, default='TMT - Turkmenistani Manat')

    def __str__(self):
        return str(self.user)+'s' + 'preferences'