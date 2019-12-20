import datetime
import calendar

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect

from .forms.forms import ActivityForm, AddMealForm, AddPortionForm, MealForm, SettingsForm, RegisterForm
from .models import Activity


def index(request):
    return render(request, 'index.html')


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


def get_first_and_last_date_form_curr_month():
    today = datetime.date.today()
    _, last_day = calendar.monthrange(today.year, today.month)
    return today.replace(day=1), today.replace(day=last_day)


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
                activity = request.user.activity_set.all().get(pk=int(request.POST['del']))
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
        from_date, to_date = get_first_and_last_date_form_curr_month()
        form.fields['from_date'].initial = from_date.strftime('%m/%d/%Y')
        form.fields['to_date'].initial = to_date.strftime('%m/%d/%Y')

    activities = request.user.activity_set.all().filter(date__gte=from_date, date__lte=to_date).order_by('date')
    for activ in activities:
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


def get_meals_count_by_days(request, from_date, to_date):
    return request.user.meal_set.all().\
        filter(date_time__gte=from_date, date_time__lte=to_date).\
        annotate(date=TruncDate('date_time')).\
        values('date').\
        annotate(count=Count('id')).\
        values('date', 'count').\
        order_by('-date')


def render_meals(request, form, add_form, formset, meals_count_by_days=[], trigger_modal=False):
    context = {
        'form': form,
        'add_form': add_form,
        'formset': formset,
        'meals_count_by_days': meals_count_by_days,
        'trigger_modal': trigger_modal,
    }
    return render(request, 'meals.html', context)


def meals(request):
    if not request.user.is_authenticated:
        return redirect('fitness_app:index')

    AddPortionFormSet = formset_factory(AddPortionForm, extra=0)

    if request.method == 'POST':
        form = MealForm(data=request.POST)
        add_form = AddMealForm()
        formset = AddPortionFormSet()
        if form.is_valid():
            from_date, to_date = form.cleaned_data['from_date'], form.cleaned_data['to_date']
        else:
            return render_meals(request, form, add_form, formset)
        if 'add' in request.POST:
            add_form = AddMealForm(data=request.POST)
            formset = AddPortionFormSet(data=request.POST)
            is_formset_valid = formset.is_valid()
            is_add_form_valid = add_form.is_valid()
            if is_add_form_valid and add_form.are_fields_filled and is_formset_valid:
                pass # TODO save Meal
            else:
                # TODO fix always wrong datetime input
                return render_meals(request, form, add_form, formset, trigger_modal=True,
                                    meals_count_by_days=get_meals_count_by_days(request, from_date, to_date))
    else:
        form = MealForm()
        add_form = AddMealForm()
        from_date, to_date = get_first_and_last_date_form_curr_month()
        form.fields['from_date'].initial = from_date.strftime('%m/%d/%Y')
        form.fields['to_date'].initial = to_date.strftime('%m/%d/%Y')
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        formset = AddPortionFormSet(data)

    return render_meals(request, form, add_form, formset, get_meals_count_by_days(request, from_date, to_date))
