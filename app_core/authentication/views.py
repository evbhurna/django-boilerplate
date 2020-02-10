from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.timezone import now

from django.contrib.auth.models import User

@login_required
def home(request):
    pass

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
        else:
            messages.warning(request, 'Incorrect username or password. Please try again.')
            return redirect('/login/') 
    else:
        return render(request, 'authentication/login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'You are successfully logged out.')
    return redirect('/login/')