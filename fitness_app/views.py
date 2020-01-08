from datetime import date, datetime, timedelta
from calendar import monthrange

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncDate
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect

from .forms.forms import ActivityForm, MealDateTimeForm, AddPortionForm, GoalsForm, MetadataForm, FromToDateForm, \
    MealTimeForm, PortionsForm, RegisterForm, SettingsForm
from .models import Activity, Meal, Portion


def get_summary_of_consume(request, date):
    from_datetime = datetime.combine(date, datetime.min.time())
    to_datetime = datetime.combine(date, datetime.max.time())
    daily_totals = Portion.objects \
        .select_related('Meal') \
        .filter(Meal__date_time__gte=from_datetime, Meal__date_time__lte=to_datetime) \
        .select_related('Meal__User') \
        .filter(Meal__User__id=request.user.id) \
        .select_related('Food') \
        .values('Meal__User') \
        .annotate(
            total_calories=Sum(F('weight') * F('Food__calories_per_100g') / 100),
            total_proteins=Sum(F('weight') * F('Food__proteins_per_100g') / 100),
            total_carbs=Sum(F('weight') * F('Food__carbs_per_100g') / 100),
            total_fats=Sum(F('weight') * F('Food__fats_per_100g') / 100),
        ) \
        .values('total_calories', 'total_proteins', 'total_carbs', 'total_fats')
    if len(daily_totals) > 0:
        return daily_totals[0].values()
    else:
        return [0] * 4


def are_goals_filled(request):
    goals = request.user.goals
    return not any(f is None for f in [goals.daily_calories, goals.daily_proteins, goals.daily_carbs, goals.daily_fats])


def get_daily_goals(request):
    goals = request.user.goals
    return goals.daily_calories, goals.daily_proteins, goals.daily_carbs, goals.daily_fats


def prepare_summary(consumed, goal):
    return {'label': f'{consumed}/{goal}', 'by_percentage': 100 * consumed // goal}


def render_index(request, view_date, are_goals_known, calories_summary=None, consume_summary=None):
    context = {
        'date_today': view_date.strftime('%m/%d/%Y'),
        'are_goals_known': are_goals_known,
        'calories_summary': calories_summary,
        'consume_summary': consume_summary,
    }
    return render(request, 'index.html', context)


def get_new_view_date(date, days):
    return datetime.strptime(date, '%m/%d/%Y') + timedelta(days=days)


@login_required
def index(request):
    if request.method == 'POST':
        if 'prev' in request.POST:
            view_date = get_new_view_date(request.POST['prev'], -1)
        elif 'next' in request.POST:
            view_date = get_new_view_date(request.POST['next'], 1)
        else:
            view_date = None
    else:
        view_date = datetime.today()

    are_goals_known = are_goals_filled(request)
    if are_goals_known:
        calories_consumed, proteins_consumed, carbs_consumed, fats_consumed = \
            get_summary_of_consume(request, date=view_date)
        calories_goal, proteins_goal, carbs_goal, fats_goal = get_daily_goals(request)
        return render_index(
            request, view_date, are_goals_known,
            calories_summary={'Calories': prepare_summary(calories_consumed, calories_goal)},
            consume_summary = {
                name: prepare_summary(consumed, goal) for name, consumed, goal in [
                    ('Proteins', proteins_consumed, proteins_goal),
                    ('Carbs', carbs_consumed, carbs_goal),
                    ('Fats', fats_consumed, fats_goal),
                ]
            })
    else:
        return render_index(request, view_date, are_goals_known)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('fitness_app:index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('fitness_app:index')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password.html', {'form': form})


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


@login_required
def goals(request):
    if request.method == 'POST':
        form = GoalsForm(data=request.POST, instance=request.user.goals)
        if form.is_valid():
            form.save()
            return redirect('fitness_app:index')
    else:
        form = GoalsForm(instance=request.user.goals)
    return render(request, 'goals.html', {'form': form})


def get_first_and_last_date_for_curr_month():
    today = date.today()
    _, last_day = monthrange(today.year, today.month)
    return today.replace(day=1), today.replace(day=last_day)


def get_days_range(from_date, to_date):
    return (to_date - from_date).days + 1


def render_activity(request, from_to_date_form, activity_form, activities, avg_cal):
    context = {
        'from_to_date_form': from_to_date_form,
        'activity_form': activity_form,
        'activities': activities,
        'avg_cal': avg_cal,
    }
    return render(request, 'activity.html', context)


@login_required
def activity(request):
    activity_form = ActivityForm()
    from_to_date_form = FromToDateForm()
    if request.method == 'POST':
        if 'del' in request.POST:
            try:
                activity = request.user.activity_set.all().get(pk=int(request.POST['del']))
                activity.delete()
            except Activity.DoesNotExist:
                pass
        elif 'add' in request.POST:
            activity = Activity(User=request.user)
            activity_form = ActivityForm(data=request.POST, instance=activity)
            if activity_form.is_valid():
                activity_form.save()
        from_to_date_form = FromToDateForm(data=request.POST)
        if from_to_date_form.is_valid():
            from_date, to_date = from_to_date_form.cleaned_data['from_date'], from_to_date_form.cleaned_data['to_date']
        else:
            return render_activity(request, from_to_date_form, activity_form, activities=[], avg_cal=0)
    else:
        from_date, to_date = get_first_and_last_date_for_curr_month()
        from_to_date_form.fields['from_date'].initial = from_date.strftime('%m/%d/%Y')
        from_to_date_form.fields['to_date'].initial = to_date.strftime('%m/%d/%Y')

    activities = request.user.activity_set.all().filter(date__gte=from_date, date__lte=to_date).order_by('date')
    for activ in activities:
        activ.calories = activ.Sport.calories_per_hour * activ.duration // 60
    return render_activity(request, from_to_date_form, activity_form, activities=activities,
                           avg_cal=sum(activ.calories for activ in activities) // get_days_range(from_date, to_date))


@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # user.email = request.POST['email']
            # user.first_name = request.POST['first_name']
            # user.last_name = request.POST['last_name']
            # user.save()
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



def render_meals(request, from_to_date_form, datetime_form, formset, meals_data=[], trigger_modal=False):
    context = {
        'from_to_date_form': from_to_date_form,
        'datetime_form': datetime_form,
        'formset': formset,
        'meals_data': meals_data,
        'trigger_modal': trigger_modal,
    }
    return render(request, 'meals.html', context)


@login_required
def meals(request):
    AddPortionFormSet = formset_factory(AddPortionForm, extra=0)
    if request.method == 'POST':
        from_to_date_form = FromToDateForm(data=request.POST)
        datetime_form = MealDateTimeForm()
        formset = AddPortionFormSet()
        if from_to_date_form.is_valid():
            from_date, to_date = from_to_date_form.cleaned_data['from_date'], from_to_date_form.cleaned_data['to_date']
        else:
            return render_meals(request, from_to_date_form, datetime_form, formset)
        if 'add' in request.POST:
            datetime_form = MealDateTimeForm(data=request.POST)
            formset = AddPortionFormSet(data=request.POST)
            is_formset_valid = formset.is_valid()
            is_datetime_form_valid = datetime_form.is_valid()
            if is_datetime_form_valid and is_formset_valid:
                meal = Meal(User=request.user, date_time=datetime_form.cleaned_data['date_time'])
                meal.save()
                portions = [Portion(Meal=meal, Food=form.cleaned_data['food'], weight=form.cleaned_data['weight'])
                            for form in filter(lambda x: x.is_fullfilled(), formset)]
                Portion.objects.bulk_create(portions)
                datetime_form = MealDateTimeForm()
                formset = AddPortionFormSet()
            else:
                return render_meals(request, from_to_date_form, datetime_form, formset, trigger_modal=True,
                                    meals_data=get_meals_data(request, from_date, to_date))
        elif 'more' in request.POST:
            date = datetime.strptime(request.POST['more'], '%Y-%m-%d')
            return redirect('fitness_app:meals_of_day', year=date.year, month=date.month, day=date.day)
    else:
        from_to_date_form = FromToDateForm()
        datetime_form = MealDateTimeForm()
        from_date, to_date = get_first_and_last_date_for_curr_month()
        from_to_date_form.fields['from_date'].initial = from_date.strftime('%m/%d/%Y')
        from_to_date_form.fields['to_date'].initial = to_date.strftime('%m/%d/%Y')
        formset = AddPortionFormSet()

    return render_meals(request, from_to_date_form, datetime_form, formset, get_meals_data(request, from_date, to_date))


def get_meals_by_date(request, date):
    from_datetime = datetime.combine(date, datetime.min.time())
    to_datetime = datetime.combine(date, datetime.max.time())
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
    return MealsFromSet(data=data, prefix='meals', initial=[
            {'id': meal.id, 'time': meal.date_time.strftime('%H:%M')} for meal in meals
        ])


def get_portions_formset(portions, data=None):
    PortionsFormSet = formset_factory(PortionsForm, extra=0, can_delete=True)
    return PortionsFormSet(data=data, prefix='portions', initial=[{
            'food': portion.Food, 'weight': portion.weight,
            'calories': portion.weight * portion.Food.calories_per_100g // 100,
            'carbohydrates': portion.weight * portion.Food.carbs_per_100g // 100,
            'fats': portion.weight * portion.Food.fats_per_100g // 100,
            'proteins': portion.weight * portion.Food.proteins_per_100g // 100,
        } for portion in portions])

def highlight_choosen(meals_formset, chosen_id):
    for form in meals_formset:
        if form.cleaned_data['id'] == chosen_id:
            form.is_to_highlight = True


def highlight_first(meals_formset):
    meals_formset[0].is_to_highlight = True


def update_portions(portions_formset, portions):
    to_update = list(filter(lambda elem: elem[0].has_changed(), zip(portions_formset, portions)))
    for form, portion in to_update:
        portion.Food = form.cleaned_data['food']
        portion.weight = form.cleaned_data['weight']
    if len(to_update) != 0:
        _, portions_to_update = zip(*to_update)
        Portion.objects.bulk_update(portions_to_update, ['Food', 'weight'])


def insert_new_portions(request, portions_formset, meal_id):
    meal = request.user.meal_set.all().get(pk=meal_id)
    portions = [Portion(Meal=meal, Food=form.cleaned_data['food'], weight=form.cleaned_data['weight'])
                for form in filter(lambda x: x.is_fullfilled(), portions_formset.extra_forms)]
    if len(portions) != 0:
        Portion.objects.bulk_create(portions)
        return True
    else:
        return False


def delete_portions(portions_formset, portions):
    to_delete = list(filter(lambda elem: elem[0] in portions_formset.deleted_forms, zip(portions_formset, portions)))
    if len(to_delete) == 0:
        return False
    for form, portion in to_delete:
        portion.delete()
    return True


@login_required
def meals_of_day(request, year, month, day):
    meals_date = date(year=year, month=month, day=day)
    meals = get_meals_by_date(request, date=meals_date)

    if request.method == 'POST':
        metadata_form = MetadataForm(data=request.POST)
        meals_formset = get_meals_formset(meals, data=request.POST)
        if metadata_form.is_valid() and meals_formset.is_valid():
            if 'choose_meal' in request.POST:
                if not meals_formset.has_changed():
                    chosen_id = int(request.POST['choose_meal'])
                    metadata_form = MetadataForm(initial={'current_meal_id': chosen_id})
                    highlight_choosen(meals_formset, chosen_id=chosen_id)
                    portions = get_portions_by_meal_id(request, meal_id=chosen_id)
                    portions_formset = get_portions_formset(portions)
            elif 'save' in request.POST:
                chosen_id = int(request.POST['current_meal_id'])
                highlight_choosen(meals_formset, chosen_id=chosen_id)
                portions = get_portions_by_meal_id(request, meal_id=chosen_id)
                portions_formset = get_portions_formset(portions, data=request.POST)
                if portions_formset.is_valid():
                    update_portions(portions_formset, portions)
                    if insert_new_portions(request, portions_formset, meal_id=chosen_id):
                        portions = get_portions_by_meal_id(request, meal_id=chosen_id)
                    # TODO remove unused
                    if delete_portions(portions_formset, portions):
                        portions = get_portions_by_meal_id(request, meal_id=chosen_id)
                    portions_formset = get_portions_formset(portions)
            elif 'del_portion' in request.POST:
                chosen_id = int(request.POST['current_meal_id'])
                highlight_choosen(meals_formset, chosen_id=chosen_id)
                portions = get_portions_by_meal_id(request, meal_id=chosen_id)
                index = int(request.POST['del_portion'])
                if index < len(portions):
                    to_remove = Portion.objects.get(pk=portions[index].id)
                    to_remove.delete()
                    portions = get_portions_by_meal_id(request, meal_id=chosen_id)
                portions_formset = get_portions_formset(portions)
            elif 'del_meal' in request.POST:
                meal_id = int(request.POST['del_meal'])
                meal = request.user.meal_set.all().get(pk=meal_id)
                meal.delete()
                if len(meals) == 1:
                    return redirect('fitness_app:meals')
                else:
                    return redirect('fitness_app:meals_of_day', year=year, month=month, day=day)
    else:
        chosen_id = meals[0].id
        metadata_form = MetadataForm(initial={'current_meal_id': chosen_id})
        meals_formset = get_meals_formset(meals)
        highlight_first(meals_formset)
        portions = get_portions_by_meal_id(request, meal_id=chosen_id)
        portions_formset = get_portions_formset(portions)

    sums = {
        'total_calories': sum(portion.weight * portion.Food.calories_per_100g // 100 for portion in portions),
        'total_carbohydrates': sum(portion.weight * portion.Food.carbs_per_100g // 100 for portion in portions),
        'total_fats': sum(portion.weight * portion.Food.fats_per_100g // 100 for portion in portions),
        'total_proteins': sum(portion.weight * portion.Food.proteins_per_100g // 100 for portion in portions),
    }
    total_calories = sum(portion.weight * portion.Food.calories_per_100g // 100 for portion in portions)
    context = {
        'metadata_form': metadata_form,
        'meals_date': meals_date.strftime('%m/%d/%Y'),
        'meals_formset': meals_formset,
        'portions_formset': portions_formset,
        'total_calories': total_calories,
        'sums': sums,
    }
    return render(request, 'meals_of_day.html', context)
