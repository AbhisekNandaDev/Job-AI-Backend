from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OTP(models.Model):
    user = models.ForeignKey(User,unique=True,on_delete=models.CASCADE)
    otp = models.CharField(max_length=20)
