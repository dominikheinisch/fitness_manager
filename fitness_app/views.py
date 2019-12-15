import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect

from .forms.forms import ActivityForm, SettingsForm, RegisterForm
from .models import Activity, MyUser


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


def get_days_range(from_date, to_date):
    return (to_date - from_date).days + 1


def render_activity(request, form, activities, avg_cal):
    context = {
        'form': form,
        'activities': activities,
        'avg_cal': avg_cal,
    }
    return render(request, 'activity.html', context)


def activity(request):
    if not request.user.is_authenticated:
        return redirect('fitness_app:index')

    form = ActivityForm()

    if request.method == 'POST':
        if 'del' in request.POST:
            # form = ActivityForm(data=request.POST)
            try:
                activity = Activity.objects.get(pk=int(request.POST['del']))
                activity.delete()
            except Activity.DoesNotExist:
                pass
        elif 'add' in request.POST:
            form = ActivityForm(is_to_add=True, data=request.POST)
            if form.is_valid():
                act = Activity(User=request.user, Sport=form.cleaned_data['sport'],
                               duration=form.cleaned_data['duration'], date=form.cleaned_data['date'])
                act.save()
            # else:
            #     form = ActivityForm(data=request.POST)
        # elif 'select' in request.POST:
        form = ActivityForm(data=request.POST)
        if form.is_valid():
            from_date, to_date = form.cleaned_data['from_date'], form.cleaned_data['to_date']
        else:
            return render_activity(request, form, activities=[], avg_cal=0)
    else:
        from_date, to_date = datetime.date.today(), datetime.date.today()
        form.fields['from_date'].initial = from_date.strftime('%m/%d/%Y')
        form.fields['to_date'].initial = to_date.strftime('%m/%d/%Y')

    activities = request.user.activity_set.all().filter(date__gte=from_date, date__lte=to_date).order_by('date')
    i = 0
    for activ in activities:
        i += 1
        activ.counter = i
        activ.calories = activ.Sport.calories_per_hour * activ.duration // 60
    return render_activity(request, form, activities=activities,
                           avg_cal=sum(activ.calories for activ in activities) // get_days_range(from_date, to_date))


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
