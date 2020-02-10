from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.loginUser),
    path('logout/', views.logoutUser),
]
