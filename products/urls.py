from django.urls import path, include
from products.views import (ProductListView, 
                            ProductDetailView, 
                            ProductCreateView, 
                            ProductUpdateView, 
                            ProductDeleteView, 
                            MyProductsListView,
                            SearchListView,
                            UserProductsListView,
                            
                            )
from products import views

urlpatterns = [
    path('', ProductListView.as_view(), name='products-home'),
    path('product/search/', SearchListView.as_view(), name='products-search'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='products-view'),
    path('product/sell/', ProductCreateView.as_view(), name='products-sell'),
    
    path('product/my', MyProductsListView.as_view(), name='products-my'),
    path('product/my/edit/<int:pk>', ProductUpdateView.as_view(), name='products-my-edit'),
    path('product/my/delete/<int:pk>', ProductDeleteView.as_view(), name='products-my-delete'),
    path('product/my/bookmarks/', views.get_bookmarks, name='products-my-bookmarks'),
    
    path('product/bookmark/<int:pk>', views.bookmark, name='products-bookmark'),
    path('product/unbookmark/<int:pk>', views.unbookmark, name='products-unbookmark'),
    
    path('product/by/<int:pk>', UserProductsListView.as_view(), name='products-by'),
    
    path('product/comment/delete/<int:pk>', views.delete_comment, name='products-comment-delete'),
    
]
