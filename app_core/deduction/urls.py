from django.urls import path
from . import views

urlpatterns = [
    path('deductions/', views.deductions),
    path('deductions/file_upload/', views.deductions),
    path('taxes/', views.taxes),
]