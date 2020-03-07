from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..views import get_portions_by_meal_id, get_summary_of_consume


class QueryTests(TestCase):
    fixtures = ['default_db.yaml']

    def test_get_portions_by_meal_id(self):
        portions = get_portions_by_meal_id(request=self.get_index_request(), meal_id=1)
        self.assertEquals(len(portions), 1)
        portion = portions[0]
        self.assertEquals(portion.Food.__str__(), 'rice')
        self.assertEquals(portion.weight, 100)

    def test_empty_get_summary_of_consume(self):
        date = datetime.strptime('1900-01-01', '%Y-%m-%d')
        daily_totals = get_summary_of_consume(request=self.get_index_request(), date=date)
        self.assertEquals(list(daily_totals), [0] * 4)

    def test_get_summary_of_consume(self):
        date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        daily_totals = get_summary_of_consume(request=self.get_index_request(), date=date)
        self.assertEquals(list(daily_totals), [546, 21, 176, 7])

    def get_index_request(self):
        self.factory = RequestFactory()
        request = self.factory.get(reverse('fitness_app:index'))
        request.user = get_user_model().objects.all().filter(username='TestUser')[0]
        return request
