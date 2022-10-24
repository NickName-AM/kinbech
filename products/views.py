from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    if request.method == 'GET':
        return render(request, 'products/home.html', {'products': products})
    elif request.method == 'POST':
        search_text = request.POST['search-data']
        search_products = []
        for product in products:
            if search_text in product.name:
                search_products.append(product)
        return render(request, 'products/search.html', {'products': search_products})

