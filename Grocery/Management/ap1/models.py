from django.db import models

# main/models.py
from django.db import models

from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    remaining = models.IntegerField(default=0)  # Set a default value here
   

    def __str__(self):
        return self.name

class Bill(models.Model):
    transaction_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    amount= models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f'{self.name} - {self.transaction_id}'

class TotalAmount(models.Model):
    transaction_id = models.IntegerField()
    total_amount = models.IntegerField(default =0)

    def __str__(self):
        return f'Transaction ID: {self.transaction_id} - Total Amount: {self.total_amount}'

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.username


class Shop(models.Model):
    name = models.CharField(max_length=20)
    shop_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=20)
    owner = models.CharField(max_length=20)
    manager = models.CharField(max_length=20)
    phone = models.IntegerField()
    license_no = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Employee(models.Model):
    emp_id = models.CharField(max_length=20, primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    phone = models.IntegerField()
    address = models.CharField(max_length=200)
    shop_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

