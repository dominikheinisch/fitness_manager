from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect

from .forms.forms import ActivityForm, SettingsForm, RegisterForm
from .models import Activity, MyUser, Sport


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
            # TODO rm
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


def activity(request):
    if not request.user.is_authenticated:
        return redirect('fitness_app:index')

    form = ActivityForm()

    if request.method == 'POST':
        if 'del' in request.POST:
            try:
                activity = Activity.objects.get(pk=int(request.POST['del']))
                activity.delete()
            except Activity.DoesNotExist:
                pass
        elif 'add' in request.POST:
            form = ActivityForm(is_to_add=False, data=request.POST)
            if form.is_valid():
                act = Activity(User=request.user, Sport=form.cleaned_data['sport'],
                               duration=form.cleaned_data['duration'], date=form.cleaned_data['date'])
                act.save()

    activities = request.user.activity_set.all()
    context = {
        'user': request.user,
        'activities': activities,
        'form': form
    }
    return render(request, 'activity.html', context)


def settings(request):
    if not request.user.is_authenticated:
        return redirect('fitness_app:index')
    user = request.user
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return redirect('fitness_app:index')
    else:
        form = SettingsForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    return render(request, 'settings.html', {'form': form})
