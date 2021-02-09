from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    wallet = models.IntegerField(default=10000)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.IntegerField()
    price = models.IntegerField()
    image_url = models.CharField(max_length=2083, default='url')

    def __str__(self):
        return self.name


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    stock = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product} | {self.stock}'


class PurchaseReturns(models.Model):
    product_return = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='product_return')
    product_return_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_return}'
