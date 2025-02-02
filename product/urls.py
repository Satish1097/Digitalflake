from django.urls import path
from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,SubcategoryListCreateAPIView,SubcategoryRetrieveUpdateDestroyAPIView,ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('subcategories/', SubcategoryListCreateAPIView.as_view(), name='subcategory-list-create'),
    path('subcategories/<int:pk>/', SubcategoryRetrieveUpdateDestroyAPIView.as_view(), name='subcategory-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-retrieve-update-destroy'),
]

