from django.db import models

# Create your models here.
class Record(models.Model):
    username = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
