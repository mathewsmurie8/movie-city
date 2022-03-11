# Create your models for accounts app here.
from django.db import models
from django.contrib.auth.models import User


class BDSGUser(models.Model):
    user =  models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

