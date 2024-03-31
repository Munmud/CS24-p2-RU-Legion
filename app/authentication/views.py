# myapp/views.py
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from captcha.fields import CaptchaField

from core.utils import is_system_admin
from .tasks import send_forget_password_mail
from .forms import CustomUserCreationForm, ProfileUpdateForm, CaptchaLoginForm
from .models import Profile


@user_passes_test(is_system_admin)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            # login(request, user)
            # Redirect to dashboard or any other page after registration
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'common/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CaptchaLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('dashboard')
    elif request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CaptchaLoginForm()
    return render(request, 'common/login.html', {'form': form})


def user_logout(request):
    logout(request)
    # Redirect to dashboard or any other page after logout
    return redirect('dashboard')


def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(
            forget_password_token=token).first()
        if profile_obj is None:
            messages.error(request, 'Not a valid Token')
            return redirect('login')

        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.error(request, 'No user id found.')
                return redirect(f'change_password', token=token)

            if new_password != confirm_password:
                messages.error(request, 'both should  be equal.')
                return redirect(f'change_password', token=token)

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password change successful')
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.error(request, 'Not user found with this username.')
                return redirect('forget_password')
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            result = send_forget_password_mail.delay(profile_obj.email, token)
            print(result)
            messages.success(request, 'An email is sent.')
            return redirect('forget-password')

    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')


@login_required
def ChangePasswordByUser(request):
    context = {}
    try:
        context = {'user_id': request.user.id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if new_password != confirm_password:
                messages.error(request, 'both should  be equal.')
                return redirect(f'change_user_password')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password change successful')
            return redirect('dashboard')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)


@login_required
def update_profile(request):
    user = request.user
    groups = user.groups.all()
    if request.method == 'POST':
        Profile.objects.get(user=user)
        form = ProfileUpdateForm(
            request.POST, instance=Profile.objects.get(user=user))
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile Update Successful")
            return redirect('update_profile')
    else:
        form = ProfileUpdateForm(instance=Profile.objects.get(user=user))
    return render(request, 'common/update_profile.html', {'form': form, 'groups': groups})
