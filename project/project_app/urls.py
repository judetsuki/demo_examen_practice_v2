from django.urls import path
from . import views

app_name = 'project_app'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),

    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name ='delete_product'),

    path('orders/edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('orders/delete/<int:pk>/', views.delete_order, name = 'delete_order')
]