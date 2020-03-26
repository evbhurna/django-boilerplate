from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('company.urls')),
    path('', include('deduction.urls')),
    path('', include('attendance.urls')),
    path('', include('payroll.urls')),
]
