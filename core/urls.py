from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
]

