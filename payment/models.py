from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import (
    Model, CharField, OneToOneField, DateTimeField
)

# Create your models here.
class UserWallet(Model):
    user: OneToOneField = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    currency: CharField = models.CharField(max_length=10, default='GHS')
    created: DateTimeField = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self) -> str:
        return self.user
    