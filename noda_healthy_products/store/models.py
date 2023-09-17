from django.db import models
from User.models import User
# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=1000)
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000000)
    price = models.FloatField()
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    in_the_main_page = models.BooleanField(blank=True)
    def __str__(self):
        return self.name

class ConfirmedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.FloatField
    status = models.CharField(choices=(('1' , 'pending'),(2, 'shipping'), (3, 'delivered')) ,default=1, max_length=1000)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    conf_order = models.ManyToManyField(ConfirmedOrder)
    count = models.IntegerField()
    price = models.FloatField()
    is_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return f"-{self.user.id}- {self.user} ==> {self.count}  {self.product.name}"
