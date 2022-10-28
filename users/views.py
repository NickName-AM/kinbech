from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MyUser
from .forms import UserRegisterForm, UserUpdateForm, MyUserUpdateForm, UserSigninForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} created!')
        else:
            messages.error(request, f'Something went wrong')
            return redirect('user-register')
        
        return redirect('user-signin')
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

def signin(request):
    if request.method == 'GET':
        form = UserSigninForm()
        return render(request, 'users/signin.html', {'form': form})
    elif request.method == 'POST':
        uname = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username=uname, password=passwd)
        # 'user' is not a boolen value, its a user
        if user:
            # If user exists and is authenticated, log him/her in and return to home
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('products-home')
        else:
            messages.error(request, 'Something\'s wrong. I can feel it.')
            return redirect('user-signin')

@login_required
def signout(request):
    logout(request)
    return redirect('products-home')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        mu_form = MyUserUpdateForm(request.POST, request.FILES, instance=request.user.myuser)
        my_forms = {
            'u_form': u_form,
            'mu_form': mu_form
        }
        if u_form.is_valid() and mu_form.is_valid():
            u_form.save()
            mu_form.save()
            messages.success(request, 'Updated!')
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        mu_form = MyUserUpdateForm(instance=request.user.myuser)
        my_forms = {
            'u_form': u_form,
            'mu_form': mu_form
        }
        return render(request, 'users/profile.html', context=my_forms)

@login_required
def signout(request):
    logout(request)
    return redirect('products-home')