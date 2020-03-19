from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Rate, Employee


@login_required
def createRate(request):
    user = Employee.objects.get(user=request.user)
    name = request.POST['name']
    is_taken = Rate.objects.filter(
        name__iexact=name, company=user.company).exists()
    data = {'is_taken': is_taken}
    return JsonResponse(data)


@login_required
def updateRate(request):
    user = Employee.objects.get(user=request.user)
    name = request.POST['name']
    id = request.POST['id']
    is_taken = Rate.objects.filter(
        name__iexact=name, company=user.company).exclude(id=id).exists()
    data = {'is_taken': is_taken}
    return JsonResponse(data)


@login_required
def createEmployee(request):
    user = Employee.objects.get(user=request.user)
    employee_number = request.POST['employee_number']
    is_taken = Employee.objects.filter(
        employee_number__iexact=employee_number, company=user.company).exists()
    data = {'is_taken': is_taken}
    return JsonResponse(data)


@login_required
def updateEmployee(request):
    user = Employee.objects.get(user=request.user)
    name = request.POST['name']
    id = request.POST['id']
    employee_number = request.POST['employee_number']
    is_taken = Employee.objects.filter(
        employee_number__iexact=employee_number, company=user.company).exclude(
            id=id).exists()
    data = {'is_taken': is_taken}
    return JsonResponse(data)
