from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_book, name='add_book'),
    path('order/<int:book_id>/', views.order_book, name='order_book'),
    path('orders/', views.list_orders, name='list_orders'),
]