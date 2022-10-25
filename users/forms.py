from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # Required
    phone = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() # Required

    class Meta:
        model = User
        fields = ['username', 'email']

class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['image', 'phone']