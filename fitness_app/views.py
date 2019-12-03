from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms.forms import SettingsForm, RegisterForm
from .models import User as MyUser


def index(request):
    user_list = MyUser.objects.order_by('birth_date')[::-1]
    context = {
        'user_list': user_list,
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('fitness_app:index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('fitness_app:index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('fitness_app:index')


def detail(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)

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
            user = MyUser.objects.get(pk=request.POST['id'])
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.surname = request.POST['surname']
            user.save()
            return HttpResponseRedirect(reverse('fitness_app:index'))
    else:
        user = get_object_or_404(MyUser, pk=user_id)
        form = SettingsForm(initial={
            'email': user.email,
            'first_name': user.first_name,
            'surname': user.surname,
            'id': user.id,
        })

    return render(request, 'settings.html', {'form': form})
