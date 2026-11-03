from django.contrib import admin
from foodapp import views
from django.urls import path


urlpatterns = [
    path('',views.home,name='home'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.view_cart, name='cart'),
path('payment/', views.payment, name='payment'),
path('place-order/', views.place_order, name='place_order'),
path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]