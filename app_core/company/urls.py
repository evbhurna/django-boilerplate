from django.urls import path

from . import views, ajax

urlpatterns = [
    path('employees/', views.employees),
    path('employees/<slug:id>/view/', views.employeesView),
    path('rates/', views.rates),
    path('rates/<slug:id>/view/', views.ratesView),


    path('ajax/create_employee/', ajax.createEmployee),
    path('ajax/create_rate/', ajax.createRate),
    path('ajax/update_employee/', ajax.updateEmployee),
    path('ajax/update_rate/', ajax.updateRate),

    path('my_profile/', views.myProfile)
]
