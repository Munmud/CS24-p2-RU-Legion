from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from authentication import views as auth_app
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('auth/login', auth_app.user_login, name='login'),
    path('auth/logout', auth_app.user_logout, name='logout'),
    path('auth/create', auth_app.register, name='register'),

    path('', dashboard, name='dashboard'),

]


# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
