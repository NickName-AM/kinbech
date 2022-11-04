from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Bookmark, Comment
from .forms import ProductRegisterForm, ProductEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    products = Product.objects.all()
    if request.method == 'GET':
        return render(request, 'products/home.html', {'products': products})
    else:
        return redirect('products-home')

def search(request):
    if request.method == 'GET':
        search_text = request.GET['search-data']
        search_products = Product.objects.filter(name__icontains=search_text)
        return render(request, 'products/search.html', {'products': search_products})
    else:
        return redirect('products-home')

def product_page(request, p_id):
    product = Product.objects.get(id=p_id)
    comments = Comment.objects.filter(product=product)
    if request.method == 'POST':
        if request.user.is_authenticated:
            cmnt = request.POST['mycomment']
            c = Comment.objects.create(comment=cmnt, product=product, user=request.user)
            messages.success(request, 'Comment sent.')
        else:
            messages.error(request, 'Sign-in to comment')
        return redirect('products-view', p_id=p_id)
    else:
        return render(request, 'products/product_page.html', {'product': product, 'comments': comments})

@login_required
def sell_product(request):
    if not request.user.myuser.phone:
        messages.error(request, 'You need to register your phone number first. Go to Profile to register.')
        return redirect('user-profile')
    if request.method == 'POST':
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
    else:
        form = ProductRegisterForm()
        return render(request, 'products/sell.html', {'form': form})

@login_required
def my_products(request):
    products = Product.objects.filter(seller_id=request.user.id)
    return render(request, 'products/my_products.html', {'products': products})

@login_required
def product_by(request, u_id):
    products = Product.objects.filter(seller_id=u_id)
    try:
        seller = User.objects.get(id=u_id).username
    except:
        seller = 'secret'
    return render(request, 'products/user_products.html', {'products': products, 'seller': seller})

@login_required
def delete_my_product(request, p_id):
    try:
        product = Product.objects.get(id=p_id, seller=request.user)
        product.delete()
        messages.success(request, 'Product Removed.')
    except:
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

@login_required
def bookmark(request, p_id):
    product = Product.objects.get(id=p_id)
    bookmarks = Bookmark.objects.filter(user=request.user)
    for mark in bookmarks:
        if mark.product_id == p_id:
            messages.warning(request, 'Already Bookmarked')
            return redirect('products-home')
    
    if product:
        Bookmark.objects.create(user=request.user, product_id=p_id)
        messages.success(request, 'Product Bookmarked')
    else:
        messages.error(request, 'Failed to Bookmark')
    
    return redirect('products-home')

@login_required
def unbookmark(request, p_id):
    bookmark = Bookmark.objects.get(user=request.user, product_id=p_id)
    if bookmark:
        bookmark.delete()
        messages.success(request, 'Bookmark removed')
    else:
        messages.error(request, 'Failed to remove bookmark')
    return redirect('products-my-bookmarks')
        

@login_required
def get_bookmarks(request):
    my_bookmarks = Bookmark.objects.filter(user=request.user)
    products = [Product.objects.get(id=bookmark_id.product_id) for bookmark_id in my_bookmarks]

    return render(request, 'products/bookmarks.html', {'products': products})

@login_required
def delete_comment(request, c_id):
    try:
        comment = Comment.objects.get(id=c_id, user=request.user)
        messages.success(request, 'Comment Deleted')
        p_id = comment.product.id
        comment.delete()
        return redirect('products-view', p_id=p_id)
    except:
        messages.error(request, 'Comment Not Deleted')

    return redirect('products-home')