from django.shortcuts import redirect
from django.urls import reverse
from authentication.models import Profile
from django.contrib import messages


class EmailUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            email = Profile.objects.get(user=request.user).email
            if email is None:
                if (request.path != reverse('update_profile')) and (request.path != reverse('logout')):
                    messages.error(
                        request, f"Email needs to be added")
                    return redirect(reverse('update_profile'))

        response = self.get_response(request)
        return response
