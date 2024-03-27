from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from waste.models import STS

from .utils import is_sts_manager, is_system_admin


@login_required()
def dashboard(request):
    if is_system_admin(request.user):
        sts_list = STS.objects.all()
        return render(request, 'system_admin/dashboard.html', {'sts_list': sts_list})
    return render(request, 'common/dashboard.html')
