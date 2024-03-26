from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import re_path

from authentication import views as auth_app
from waste import views as waste_app
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_dashboard'),

    # auth
    path('auth/login', auth_app.user_login, name='login'),
    path('auth/logout', auth_app.user_logout, name='logout'),
    path('auth/create', auth_app.register, name='register'),
    path('auth/forget-password/', auth_app.ForgetPassword, name="forget_password"),
    path('auth/change-password/<token>/',
         auth_app.ChangePassword, name="change_password"),

    # Ststem Admin
    path('system_admin/add_vehicle/', waste_app.add_vehicle, name="add_vehicle"),

    # STS Manager
    path('sts_manager/transfer_waste/',
         waste_app.add_waste_transfer, name="add_waste_transfer"),


    path('', dashboard, name='dashboard'),

]


# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
