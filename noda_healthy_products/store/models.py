from django.db import models
from User.models import User, City
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
    price = models.FloatField(default=0)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=100000)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(choices=(('confirmed' , 'confirmed'),('pending', 'pending'),('shipping', 'shipping'), ('delivered', 'delivered')) ,default='confirmed', max_length=1000)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    conf_order = models.ForeignKey(ConfirmedOrder, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
    price = models.FloatField()
    is_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return f"-{self.user.id}- {self.user} ==> {self.count}  {self.product.name}"

