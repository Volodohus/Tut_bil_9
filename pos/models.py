from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Chel(models.Model):
    id = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE
    )
    tgid = models.BigIntegerField(unique=True)
    tgni = models.CharField(max_length=100)
    tgna = models.CharField(max_length=100, null=True, blank= True)
    na   = models.CharField(max_length=100, help_text='Как себя назовёшь, так и поплывёшь.',null=True,blank=True)
    po   = models.CharField(max_length=1000, help_text = 'Твоё посланице. 1000 символов.',null=True,blank=True)

    def __str__(self):
        return self.na + ''' сказал(а) ''' + self.po