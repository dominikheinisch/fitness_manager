from datetime import date, datetime
from calendar import monthrange

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect

from .forms.forms import ActivityForm, AddMealForm, AddPortionForm, MealForm, MealTimeForm, SettingsForm, PortionsForm,\
    RegisterForm
from .models import Activity, Meal, Portion


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


def get_first_and_last_date_for_curr_month():
    today = date.today()
    _, last_day = monthrange(today.year, today.month)
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
        from_date, to_date = get_first_and_last_date_for_curr_month()
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


def get_meals_data(request, from_date, to_date):
    from_datetime = datetime.combine(from_date, datetime.min.time())
    to_datetime = datetime.combine(to_date, datetime.max.time())
    # TODO use proper query with GROUP BY here
    calories_data = Portion.objects\
        .select_related('Meal') \
        .filter(Meal__date_time__gte=from_datetime, Meal__date_time__lte=to_datetime) \
        .select_related('Meal__User') \
        .filter(Meal__User__id=request.user.id) \
        .select_related('Food') \
        .extra(select={'day_calories': 'weight * calories_per_100g / 100'}) \
        .annotate(date=TruncDate('Meal__date_time')) \
        .values('date', 'day_calories', 'weight', 'Food__calories_per_100g') \
        .order_by('-date')
    counts_data = request.user.meal_set.all(). \
        filter(date_time__gte=from_datetime, date_time__lte=to_datetime).\
        annotate(date=TruncDate('date_time')).\
        values('date').\
        annotate(count=Count('id')).\
        values('date', 'count').\
        order_by('-date')
    result = {}
    for elem in counts_data:
        result[str(elem['date'])] = {'date': str(elem['date']), 'day_calories': 0, 'count': elem['count']}
    for elem in calories_data:
        result[str(elem['date'])]['day_calories'] += elem['day_calories']
    return list(result.values())



def render_meals(request, form, add_form, formset, meals_data=[], trigger_modal=False):
    context = {
        'form': form,
        'add_form': add_form,
        'formset': formset,
        'meals_data': meals_data,
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
                meal = Meal(User=request.user, date_time=add_form.cleaned_data['date_time'])
                meal.save()
                portions = [Portion(Meal=meal, Food=form.cleaned_data['food'], weight=form.cleaned_data['weight'])
                            for form in filter(lambda x: x.is_fullfilled(), formset)]
                Portion.objects.bulk_create(portions)
                add_form = AddMealForm()
                formset = AddPortionFormSet()
            else:
                return render_meals(request, form, add_form, formset, trigger_modal=True,
                                    meals_data=get_meals_data(request, from_date, to_date))
        elif 'more' in request.POST:
            date = datetime.strptime(request.POST['more'], '%Y-%m-%d')
            return redirect('fitness_app:day_meals', year=date.year, month=date.month, day=date.day)
    else:
        form = MealForm()
        add_form = AddMealForm()
        from_date, to_date = get_first_and_last_date_for_curr_month()
        form.fields['from_date'].initial = from_date.strftime('%m/%d/%Y')
        form.fields['to_date'].initial = to_date.strftime('%m/%d/%Y')
        formset = AddPortionFormSet()

    return render_meals(request, form, add_form, formset, get_meals_data(request, from_date, to_date))


def get_meals_by_date(request, date):
    from_datetime = datetime.combine(date, datetime.min.time())
    to_datetime = datetime.combine(date, datetime.max.time())
    print(from_datetime, to_datetime)
    return request.user.meal_set.all() \
        .filter(date_time__gte=from_datetime, date_time__lte=to_datetime) \
        .order_by('date_time', 'id')


def get_portions_by_meal_id(request, meal_id):
    return Portion.objects \
        .select_related('Meal') \
        .filter(Meal__id=meal_id) \
        .select_related('Meal__User') \
        .filter(Meal__User__id=request.user.id) \
        .select_related('Food')


def get_meals_formset(meals, data=None):
    MealsFromSet = formset_factory(MealTimeForm, extra=0)
    print([meal.date_time.strftime('%H:%M') for meal in meals])
    return MealsFromSet(data=data, prefix='meals', initial=[
            {'id': meal.id, 'time': meal.date_time.strftime('%H:%M')} for meal in meals
        ])


def get_portions_formset(portions, data=None):
    PortionsFormSet = formset_factory(PortionsForm, extra=0, can_delete=True)
    return PortionsFormSet(data=data, prefix='portions', initial=[
            {'food': portion.Food, 'weight': portion.weight,
             'calories': portion.weight * portion.Food.calories_per_100g // 100} for portion in portions
        ])

def day_meals(request, year, month, day):
    if not request.user.is_authenticated:
        return redirect('fitness_app:index')

    meals_date = date(year=year, month=month, day=day)
    meals = get_meals_by_date(request, date=meals_date)
    for m in meals:
        print(m.date_time)

    if request.method == 'POST':
        meals_fromset = get_meals_formset(meals, data=request.POST)
        portions = get_portions_by_meal_id(request, meal_id=meals[0].id)
        portions_formset = get_portions_formset(portions, data=request.POST)

        for form in portions_formset:
            print(form.has_changed())
            print("The following fields changed: %s" % ", ".join(form.changed_data))
        print("Tmeals_fromset meals_fromset meals_fromset meals_fromset meals_fromset meals_fromset meals_fromset")
        for form in meals_fromset:
            print(form.fields['time'])
            print(form.has_changed())
            print("The following fields changed: %s" % ", ".join(form.changed_data))
        # TODO use curr id
    else:
        meals_fromset = get_meals_formset(meals)
        for m in meals:
            print(m.date_time)
            print(m.date_time.time())
            print(type(m.date_time))
            print(type(m.date_time.time()))
        portions = get_portions_by_meal_id(request, meal_id=meals[0].id)
        portions_formset = get_portions_formset(portions)

    total_calories = sum(portion.weight * portion.Food.calories_per_100g // 100 for portion in portions)
    context = {
        'meals_date': meals_date.strftime('%m/%d/%Y'),
        'meals_fromset': meals_fromset,
        'portions_formset': portions_formset,
        'total_calories': total_calories,
    }
    return render(request, 'meals_of_day.html', context)
