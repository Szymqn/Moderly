from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_status/<int:order_id>/', views.order_status, name='order_status'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
]
