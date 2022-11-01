from django.db import models
from django.contrib.auth.models import User

from PIL import Image

# Create your models here.

CATEGORIES = [
    ('HA', 'home-appliance'),
    ('HW', 'hardware'),
    ('SW', 'software'),
    ('OT', 'other')
]

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, help_text='Name of the product')
    description = models.TextField(help_text='Features/Characteristics of the product.')
    category = models.CharField(max_length=2, choices=CATEGORIES, default='OT')
    price = models.PositiveIntegerField(help_text='Price of the product. In NPR')
    image = models.ImageField(default='default_product.jpg', upload_to='product_pics')

    def __str__(self):
        return f'{self.name} by {self.seller}'

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_id} bookmarked by {self.user.username}'


