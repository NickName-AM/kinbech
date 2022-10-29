from django import forms
from .models import Product

CATEGORIES = [
('HA', 'home-appliance'),
('HW', 'hardware'),
('SW', 'software'),
('OT', 'other')
]
    
class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']
        exclude = ['seller',]

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']
        exclude = ['seller',]