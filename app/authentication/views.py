# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test

from core.utils import is_system_admin


@user_passes_test(is_system_admin)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            # Redirect to dashboard or any other page after registration
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'common/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Login Successful")
            # Redirect to dashboard or any other page after login
            return redirect('dashboard')
    elif request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'common/login.html', {'form': form})


def user_logout(request):
    logout(request)
    # Redirect to dashboard or any other page after logout
    return redirect('dashboard')
