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

from waste.models import *
from .utils import is_sts_manager, is_system_admin, is_landfill_manager
from .utils import aws_map_route_api


def dashboard(request):
    if is_system_admin(request.user):
        sts_list = STS.objects.all()
        landfill_list = Landfill.objects.all()
        return render(request, 'system_admin/dashboard.html', {
            'sts_list': sts_list,
            'landfill_list': landfill_list
        })

    elif is_sts_manager(request.user):
        sts = STSManager.objects.get(user=request.user).sts
        waste_transfers = WasteTransfer.objects.exclude(
            status='Completed').order_by('-id').all()
        return render(request, 'sts_manager/dashboard.html', {
            'sts': sts,
            'waste_transfers': waste_transfers
        })

    elif is_landfill_manager(request.user):
        landfill = LandfillManager.objects.get(user=request.user).landfill
        waste_transfers = WasteTransfer.objects.exclude(
            status='Completed').order_by('-id').all()
        return render(request, 'landfill_manager/dashboard.html', {
            'landfill': landfill,
            'waste_transfers': waste_transfers
        })

    return render(request, 'common/dashboard.html')
