from django.urls import path, include
from products import views

urlpatterns = [
    path('', views.home, name='products-home'),
    path('sell/', views.sell_product, name='products-sell'),
]
