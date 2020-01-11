from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Goals(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_calories = models.IntegerField(blank=True, null=True)
    daily_proteins = models.IntegerField(blank=True, null=True)
    daily_carbs = models.IntegerField(blank=True, null=True)
    daily_fats = models.IntegerField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_goals(sender, instance, created, **kwargs):
    if created:
        Goals.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_goals(sender, instance, **kwargs):
    instance.goals.save()


class Sport(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    calories_per_hour = models.IntegerField()

    def __str__(self):
        return self.name


class Activity(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    date = models.DateField('start date')
    duration = models.IntegerField()


class Food(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    calories_per_1kg = models.IntegerField()
    carbs_per_1kg = models.IntegerField()
    fats_per_1kg = models.IntegerField()
    proteins_per_1kg = models.IntegerField()

    def __str__(self):
        return self.name

class Meal(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField('meal datetime')


class Portion(models.Model):
    Meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    Food = models.ForeignKey(Food, on_delete=models.CASCADE)
    weight = models.IntegerField()
