from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    desctiption = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
