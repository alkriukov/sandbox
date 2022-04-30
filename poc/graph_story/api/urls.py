from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/<str:user_name>/', views.user),
    path('graph/<str:graph_name>/', views.graph),
]
