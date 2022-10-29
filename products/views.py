from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductRegisterForm, ProductEditForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    products = Product.objects.all()
    if request.method == 'GET':
        return render(request, 'products/home.html', {'products': products})
    elif request.method == 'POST':
        search_text = request.POST['search-data']
        search_products = Product.objects.filter(name__icontains=search_text)
        return render(request, 'products/search.html', {'products': search_products})

def product_page(request, p_id):
    product = Product.objects.get(id=p_id)
    return render(request, 'products/product_page.html', {'product': product})

@login_required
def sell_product(request):
    if request.method == 'GET':
        form = ProductRegisterForm()
        return render(request, 'products/sell.html', {'form': form})
    elif request.method == 'POST':
        form = ProductRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.seller = request.user
            p.save()
            # form.save()
            messages.success(request, 'Product Registered!')
            return redirect('products-home')
        else:
            messages.error(request, 'Form is not valid. Check again!')
            return redirect('products-sell')

@login_required
def my_products(request):
    products = Product.objects.filter(seller_id=request.user.id)
    return render(request, 'products/my_products.html', {'products': products})

@login_required
def delete_my_product(request, p_id):
    product = Product.objects.get(id=p_id)
    if product.seller.id == request.user.id:
        product.delete()
        messages.success(request, 'Product Removed.')
    else:
        messages.error(request, 'You are not the seller.')

    return redirect('products-my')

@login_required
def edit_my_product(request, p_id):
    product = Product.objects.get(id=p_id)
    if product.seller.id == request.user.id:
        if request.method == 'POST':
            form = ProductEditForm(request.POST,request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product Editted.')
            else:
                messages.error(request, 'Form is not valid.')
                return redirect('products-my-edit')

        else:
            form =  ProductEditForm(instance=product)
            return render(request, 'products/edit_my_product.html', {'form': form})
        
    else:
        messages.error(request, 'You are not the seller.')
    
    return redirect('products-my')