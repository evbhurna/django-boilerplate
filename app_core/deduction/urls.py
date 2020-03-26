from django.urls import path
from . import views

urlpatterns = [
    path('deductions/', views.deductions),
    path('deductions/file_upload/', views.deductionsUpload),
    path('taxes/', views.taxes),

    path('my_taxes/', views.myTaxes),
    path('my_deductions/', views.myDeductions),
    
]