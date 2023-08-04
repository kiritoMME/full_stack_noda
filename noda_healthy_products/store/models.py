from django.db import models

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
