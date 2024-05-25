from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm

# Create your views here.
def SignUpView(request):
    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        #create user instance if form data is valid
        if (form.is_valid()):
            user = form.save()            
            login(request, user)
            # return redirect('')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', { 'form': form })


def LogInView(request):
    if (request.method == 'POST'):
        form = AuthenticationForm(data=request.POST)
        if (form.is_valid()):
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', { 'form': form })


def LogOutView(request):
    if (request.method == 'POST'):
        logout(request)
        return redirect('login')
