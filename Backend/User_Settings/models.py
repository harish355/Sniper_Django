from statistics import mode
from django.db import models
from Register.models import Account


class Api_table(models.Model):
    User = models.ForeignKey(Account, on_delete=models.CASCADE)
    userid = models.CharField(max_length=64)
    api_key = models.CharField(max_length=513)
    MWN=models.CharField(max_length=32,default="None")
