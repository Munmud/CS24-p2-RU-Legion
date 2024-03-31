from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from .models import Profile
from django.contrib.auth import authenticate


class CaptchaLoginForm(AuthenticationForm):
    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            group_names = [
                settings.GROUP_NAME_SYSTEM_ADMIN,
                settings.GROUP_NAME_STS_MANAGER,
                settings.GROUP_NAME_LANDFILL_MANAGER
            ]
            user_groups = Group.objects.filter(user=user, name__in=group_names)
            if not user_groups.exists():
                raise forms.ValidationError(
                    "User is not assigned to any group. Please contact system admin.")
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email']
