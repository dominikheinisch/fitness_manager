from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField('birth date')

