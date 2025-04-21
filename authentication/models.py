from django.db import models

# Create your models here.


class Otp(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6,  blank=True)
