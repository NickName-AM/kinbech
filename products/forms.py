from django import forms
from .models import Product

class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image']
        exclude = ['seller',]