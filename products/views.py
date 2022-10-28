from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    products = Product.objects.all()
    if request.method == 'GET':
        return render(request, 'products/home.html', {'products': products})
    elif request.method == 'POST':
        search_text = request.POST['search-data']
        search_products = [product for product in products if search_text.lower() in product.name.lower()]
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

