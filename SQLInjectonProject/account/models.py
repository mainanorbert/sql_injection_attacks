from django.db import models

# Create your models here.

class User(models.Model):
    """This class defines user model"""
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
