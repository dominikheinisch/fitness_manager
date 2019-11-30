from django.http import HttpResponse
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Activity, User


def index(request):
    user_list = User.objects.order_by('birth_date')[::-1]
    context = {
        'user_list': user_list,
    }
    return render(request, 'index.html', context)


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    activities = Activity.objects.filter(User_id=user_id)
    a = activities[0]
    context = {
        'user': user,
        'activities': activities,
    }
    return render(request, 'detail.html', context)
