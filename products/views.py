from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Bookmark, Comment
from .forms import ProductRegisterForm, ProductEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'

class SearchListView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(name__icontains=self.request.GET['search-data'])
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_page.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['comments'] = Comment.objects.filter(product=context['product'])
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'category', 'price', 'quantity', 'image']
    template_name = 'products/sell.html'
    exclude = ['seller',]

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class MyProductsListView(ListView):
    model = Product
    template_name = 'products/my_products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(seller=self.request.user)
        return context

class UserProductsListView(ListView):
    model = Product
    template_name = 'products/user_products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(seller_id=self.kwargs['pk'])
        return context

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'category', 'price', 'quantity', 'image']
    template_name = 'products/sell.html'
    exclude = ['seller',]

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False

@login_required
def bookmark(request, pk):
    product = Product.objects.get(id=pk)
    bookmarks = Bookmark.objects.filter(user=request.user)
    for mark in bookmarks:
        if mark.product_id == pk:
            messages.warning(request, 'Already Bookmarked')
            return redirect('products-home')
    
    if product:
        Bookmark.objects.create(user=request.user, product_id=pk)
        messages.success(request, 'Product Bookmarked')
    else:
        messages.error(request, 'Failed to Bookmark')
    
    return redirect('products-home')

@login_required
def unbookmark(request, pk):
    bookmark = Bookmark.objects.get(user=request.user, product_id=pk)
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
        pk = comment.product.id
        comment.delete()
        return redirect('products-view', pk=pk)
    except:
        messages.error(request, 'Comment Not Deleted')

    return redirect('products-home')