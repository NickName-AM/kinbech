from django.urls import path, include
from products import views

urlpatterns = [
    path('', views.home, name='products-home'),
    path('product/search/', views.search, name='products-search'),
    path('product/sell/', views.sell_product, name='products-sell'),
    path('product/<int:p_id>', views.product_page, name='products-view'),
    path('product/my', views.my_products, name='products-my'),
    path('product/by/<int:u_id>', views.product_by, name='products-by'),
    path('product/my/edit/<int:p_id>', views.edit_my_product, name='products-my-edit'),
    path('product/my/delete/<int:p_id>', views.delete_my_product, name='products-my-delete'),
]
