
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/auth/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)

    return True
