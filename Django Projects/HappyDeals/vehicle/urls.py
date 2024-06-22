# vehicle/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),  # Admin login
    path('vehicle/', views.vehicle_list, name='vehicle_list'),
    path('add/', views.vehicle_add, name='vehicle_add'),
    path('edit/<int:pk>/', views.vehicle_edit, name='vehicle_edit'),
    path('delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
    path('rent/<int:vehicle_id>/', views.rent_vehicle, name='rent_vehicle'),
    path('register/', views.register, name='register'),
    path('customer/', views.user_login, name='customer'),  # Customer login
]


