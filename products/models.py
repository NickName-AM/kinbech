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
    name = models.CharField(max_length=30)
    description = models.TextField(help_text='Features/Characteristics of the product.')
    category = models.CharField(max_length=2, choices=CATEGORIES, default='OT')
    image = models.ImageField(default='default_product.jpg', upload_to='product_pics')

    def __str__(self):
        return f'{self.name} by {self.seller}'

