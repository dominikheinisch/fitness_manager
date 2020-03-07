from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..views import get_meals_data, get_portions_by_meal_id, get_summary_of_consume


class QueryTests(TestCase):
    fixtures = ['default_db.yaml']

    def setUp(self):
        self.request = self.get_default_request()

    def test_get_portions_by_meal_id(self):
        portions = get_portions_by_meal_id(request=self.request, meal_id=1)
        self.assertEquals(len(portions), 1)
        portion = portions[0]
        self.assertEquals(portion.Food.__str__(), 'rice')
        self.assertEquals(portion.weight, 100)

    def test_empty_get_summary_of_consume(self):
        date = datetime.strptime('1900-01-01', '%Y-%m-%d')
        daily_totals = get_summary_of_consume(request=self.request, date=date)
        self.assertEquals(list(daily_totals), [0] * 4)

    def test_get_summary_of_consume(self):
        date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        daily_totals = get_summary_of_consume(request=self.request, date=date)
        self.assertEquals(list(daily_totals), [546, 21, 176, 7])

    def test_get_meals_data(self):
        from_date = datetime.strptime('1900-01-01', '%Y-%m-%d')
        to_date = datetime.strptime('2100-01-01', '%Y-%m-%d')
        meals_data = get_meals_data(request=self.request, from_date=from_date, to_date=to_date)
        result = [
            {'count': 1, 'date': '2020-02-02', 'day_calories': 2000},
            {'count': 2, 'date': '2020-01-01', 'day_calories': 546},
        ]
        self.assertEquals(meals_data, result)

    def get_default_request(self):
        self.factory = RequestFactory()
        request = self.factory.get(reverse('fitness_app:index'))
        request.user = get_user_model().objects.all().filter(username='TestUser')[0]
        return request
