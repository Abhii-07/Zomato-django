# models.py

from django.db import models

class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='received')
    dishes = models.ManyToManyField(Dish)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
