from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    price = models.FloatField(default=0)
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.code + " - " + self.name

class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)   
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    amount_balance = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    total_qty = models.IntegerField(default=0)
    def __str__(self):
        return self.code

class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return f"Sale ID: {self.sale_id}, Product ID: {self.product_id}"

class Inventory(models.Model):
    code = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    items_purchased = models.TextField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_number = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=255)
    def __str__(self):
        return self.customer_name


class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secretary_name = models.CharField(max_length=255)
    secretary_number = models.CharField(max_length=20)
    # Add any additional fields specific to secretaries

    def __str__(self):
        return self.secretary_name