from django.db import models

# Create your models here.
class Customers(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    father = models.CharField(max_length=100)
    email = models.EmailField()
    pass1 = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    profile_pic = models.FileField(upload_to='profile/', null=True)

class Category(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=100)
    des = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    pname = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    des = models.CharField(max_length=100)
    image = models.FileField(upload_to='products/')

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cus_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('product', 'cus_id')
