from django.db import models
from .views import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here
# 

class UserLogRe(models.Model):
    username = models.CharField(max_length=50,null=False,blank=False,unique=True)
    phone = models.PositiveIntegerField(unique=True)
    mail = models.EmailField(max_length=30,null=False,blank=False,unique=True)
    pas1 = models.CharField(max_length=15,null=False,blank=False,unique=True)
    pas2 = models.CharField(max_length=15,null=False,blank=False)
    def __str__(self):
        return self.mail

state_choice=(
    ('MyCityAHM','MyCityAHM'),
    ('Mumbai','Mumbai'),
    ('Delhi','Delhi'),
    ('Gujarat','Gujarat'),
)

class Customer(models.Model):
    user = models.ForeignKey(UserLogRe,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=state_choice,max_length=50)

    def __str__(self):
        return str(self.id)

catogory_choice=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear')
)

class Products(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    catogory = models.CharField(choices=catogory_choice,max_length=4)
    teak = models.CharField(max_length=200,null=True,blank=True)
    product_img = models.ImageField(upload_to='product_img')
    
    def __str__(self):
       return self.brand    
   

class Cart(models.Model):
    user = models.ForeignKey(UserLogRe,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=False)
    add_on = models.DateTimeField(auto_now=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

status_choice = (
    ('Accepted','Accepted'),
    ('Packed','packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)


class Orderplaced(models.Model):
    user = models.ForeignKey(UserLogRe,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,default='Pending',choices=status_choice)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


# Create your models here.


    