from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms.forms import SettingsForm
from .models import Activity, User


def index(request):
    user_list = User.objects.order_by('birth_date')[::-1]
    context = {
        'user_list': user_list,
    }
    return render(request, 'index.html', context)


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    activities = user.activity_set.all()
    context = {
        'user': user,
        'activities': activities,
    }
    return render(request, 'detail.html', context)


def settings(request, user_id):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.POST['id'])
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.surname = request.POST['surname']
            user.save()
            return HttpResponseRedirect('/fitness')
    else:
        user = get_object_or_404(User, pk=user_id)
        form = SettingsForm(initial={
            'email': user.email,
            'first_name': user.first_name,
            'surname': user.surname,
            'id': user.id,
        })

    return render(request, 'settings.html', {'form': form})
