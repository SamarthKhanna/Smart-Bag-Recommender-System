from django.db import models
import random

def random_string():
    return str(random.randint(1000, 1999))

class User(models.Model):
    email_id = models.EmailField(max_length=254,blank=False,default='')
    password = models.CharField(max_length=25,blank=False,default='password')
    user_id = models.CharField(primary_key=True,default=random_string,max_length=24)

class Products(models.Model):
    item_id = models.CharField(blank=False,max_length=150)
    major = models.CharField(blank=False,max_length=150)
    minor = models.CharField(blank=False,max_length=150)
    typeP = models.CharField(blank=False,max_length=150)
    name = models.CharField(blank=False,max_length=150)
    dprice = models.CharField(blank=False,max_length=150)
    oprice = models.CharField(blank=False,max_length=150)
    discount = models.CharField(blank=False,default=0,max_length=150)
    quantity = models.CharField(blank=False,default=0,max_length=150)
    sponsored = models.CharField(blank=False,default=False,max_length=150)

class Orders(models.Model):
    order_id = models.CharField(blank=False,max_length=150)
    user_id = models.CharField(blank=False,unique=False,max_length=150)
    item_id = models.CharField(blank=False,unique=False,max_length=150)
    day_of_month = models.CharField(blank=False,max_length=150)