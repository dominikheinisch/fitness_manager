import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from fitness_app.models import *


class Command(BaseCommand):
    help = 'Populate hardcoded data to db'

    def handle(self, *args, **options):
        add_users()
        add_goals()
        add_sports()
        add_activities()
        add_foods()
        add_meals()
        add_portions()
        add_todays_meal()
        print('populating has finished')


def add_users():
    for user in [
        User.objects.create_user(username='JanNowak', password='pwrpwr123'),
        User.objects.create_user(username='DominikNowak', password='pwrpwr123'),
    ]:
        user.save()


def add_goals():
    Goals.objects.all().filter(pk=2).update(daily_calories=3000, daily_proteins=150, daily_carbs=330, daily_fats=100)


def add_sports():
    for sport in [
        Sport(name='cycling', calories_per_hour=62),
        Sport(name='running', calories_per_hour=81),
        Sport(name='gym', calories_per_hour=112),
    ]:
        sport.save()


def add_foods():
    for food in [
        Food(name='rice', calories_per_100g=220, carbs_per_100g=70, fats_per_100g=3, proteins_per_100g=8),
        Food(name='apple', calories_per_100g=86, carbs_per_100g=80, fats_per_100g=2, proteins_per_100g=4),
        Food(name='orange', calories_per_100g=92, carbs_per_100g=75, fats_per_100g=1, proteins_per_100g=5),
        Food(name='chicken meat', calories_per_100g=367, carbs_per_100g=5, fats_per_100g=10, proteins_per_100g=19),
    ]:
        food.save()


def add_meals():
    for meal in [
        Meal(User=User.objects.get(id=1), date_time='2020-1-19T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T17:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T19:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-20T13:00:00'),
        Meal(User=User.objects.get(id=3), date_time='2020-1-19T13:00:00'),
        Meal(User=User.objects.get(id=3), date_time='2020-1-19T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-20T13:00:00'),

        Meal(User=User.objects.get(id=2), date_time='2020-1-17T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T17:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T19:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T21:00:00'),

        Meal(User=User.objects.get(id=2), date_time='2020-1-13T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T17:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T19:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T21:00:00'),

        Meal(User=User.objects.get(id=2), date_time='2020-1-31T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-30T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-28T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-26T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-24T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-23T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-22T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-21T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-20T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-18T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-11T21:00:00'),
    ]:
        meal.save()


def add_portions():
    for portion in [
        Portion(Meal=Meal.objects.get(id=1), Food=Food.objects.get(name='rice'), weight=100),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='apple'), weight=120),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='orange'), weight=30),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='chicken meat'), weight=330),
        Portion(Meal=Meal.objects.get(id=3), Food=Food.objects.get(name='rice'), weight=250),
        Portion(Meal=Meal.objects.get(id=3), Food=Food.objects.get(name='chicken meat'), weight=550),
        Portion(Meal=Meal.objects.get(id=4), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=5), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=6), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=7), Food=Food.objects.get(name='rice'), weight=1000),
        Portion(Meal=Meal.objects.get(id=8), Food=Food.objects.get(name='apple'), weight=111),
        Portion(Meal=Meal.objects.get(id=9), Food=Food.objects.get(name='apple'), weight=111),
    ]:
        portion.save()


def add_activities():
    for activity in [
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(name='cycling'), duration=90, date='2020-1-10'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(name='running'), duration=45, date='2020-1-10'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(name='gym'), duration=120, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='running'), duration=90, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='running'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='cycling'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='running'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='cycling'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2019-1-31'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-30'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-30'),
        Activity(User=User.objects.get(id=3), Sport=Sport.objects.get(name='gym'), duration=150, date='2020-1-11'),
    ]:
        activity.save()


def add_todays_meal():
    datetimes = [datetime.datetime.combine(datetime.date.today(), datetime.time()).replace(hour=hour)
                 for hour in [9, 12, 15, 18]]
    meals = [Meal(User=User.objects.get(id=2), date_time=dt) for dt in datetimes]
    for meal in meals:
        meal.save()

    for meal in meals:
        p1 = Portion(Meal=meal, Food=Food.objects.get(name='rice'), weight=100)
        p2 = Portion(Meal=meal, Food=Food.objects.get(name='chicken meat'), weight=150)
        p1.save()
        p2.save()
