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

    def __str__(self):
        return self.name

class Activity(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    date = models.DateField('start date')
    duration = models.IntegerField()


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


def add_sports():
    for sport in [
        Sport(name='cycling', calories_per_hour=62),
        Sport(name='running', calories_per_hour=81),
        Sport(name='gym', calories_per_hour=112),
    ]:
        sport.save()


def fill_default_database():
    # TODO rm
    # for user in [
    #     MyUser(first_name='Jan', surname='Nowak', birth_date='1999-9-9', email='a@o2.pl', gender='M'),
    #     MyUser(first_name='Dominik', surname='Nowak', birth_date='1999-9-9', email='Dominik.Nowak@gmail.com'),
    #     MyUser(first_name='Michal', surname='Kowalski-Nowak', birth_date='2000-1-1', email='aaa@wp.pl'),
    # ]:
    #     user.save()

    for activity in [
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(id=1), duration=90, date='1999-9-10'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(id=2), duration=45, date='2019-9-10'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(id=3), duration=120, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=2), duration=90, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=2), duration=60, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=1), duration=60, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), duration=60, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=2), duration=60, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=1), duration=60, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), duration=75, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), duration=75, date='2019-9-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), duration=75, date='2019-1-31'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), duration=75, date='2019-9-30'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(id=3), duration=75, date='2019-9-30'),
        Activity(User=User.objects.get(id=3), Sport=Sport.objects.get(id=3), duration=150, date='2019-9-11'),
    ]:
        activity.save()


# add_users()
# add_sports()
# fill_default_database()
