from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryName

class Item(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")    

    def __str__(self):
        return f"{self.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="user")
    product = models.ManyToManyField(Item)

    def __str__(self):
        return f"{self.user}"