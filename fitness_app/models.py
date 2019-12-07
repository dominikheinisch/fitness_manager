from django.db import models

from django.contrib.auth.models import User


class MyUser(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    birth_date = models.DateField('birth date')
    MALE = 'M'
    FEMALE = 'F'
    gender = models.CharField(
        max_length=1,
        choices=[(MALE, 'male'), (FEMALE, 'female')],
    )


class Sport(models.Model):
    name = models.CharField(max_length=50)
    calories_per_hour = models.IntegerField()


class Activity(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    start = models.DateTimeField('start time')
    stop = models.DateTimeField('stop time')


class Food(models.Model):
    name = models.CharField(max_length=50)
    calories_per_100g = models.IntegerField()


class Portion(models.Model):
    Food = models.ForeignKey(Food, on_delete=models.CASCADE)
    weight = models.IntegerField()


class Meal(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Portion = models.ForeignKey(Portion, on_delete=models.CASCADE)
    data_time = models.DateTimeField('stop time')


def add_users():
    for user in [
        User.objects.create_user(username='JanNowak', password='pwrpwr123'),
        User.objects.create_user(username='DominikNowak', password='pwrpwr123'),
    ]:
        user.save()


# add_users()


def fill_default_database():
    for user in [
        MyUser(first_name='Jan', surname='Nowak', birth_date='1999-9-9', email='a@o2.pl', gender='M'),
        MyUser(first_name='Dominik', surname='Nowak', birth_date='1999-9-9', email='Dominik.Nowak@gmail.com'),
        MyUser(first_name='Michal', surname='Kowalski-Nowak', birth_date='2000-1-1', email='aaa@wp.pl'),
    ]:
        user.save()

    for sport in [
        Sport(name='cycling', calories_per_hour=62),
        Sport(name='running', calories_per_hour=81),
        Sport(name='gym', calories_per_hour=112),
    ]:
        sport.save()

    for activity in [
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(id=1), start='1999-9-9T13:00', stop='1999-9-10T13:15'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(id=2), start='2019-9-9T13:00', stop='2019-9-10T13:15'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(id=3), start='2019-9-9', stop='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=2), start='2019-9-9', stop='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=2), start='2019-9-9T13:00', stop='2019-9-10T13:55'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=1), start='2019-9-9T13:00', stop='2019-9-10T13:55'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), start='2019-9-9T13:00', stop='2019-9-10T13:55'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=2), start='2019-9-9T13:00', stop='2019-9-10T13:55'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=1), start='2019-9-9T13:00', stop='2019-9-10T13:05'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), start='2019-9-9T12:00', stop='2019-9-10T13:55'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), start='2019-9-9T12:00', stop='2019-9-10T15:00'),
        Activity(User=User.objects.get(id=3), Sport=Sport.objects.get(id=3), start='2019-9-11', stop='2019-9-11'),
    ]:
        activity.save()


# fill_default_database()
