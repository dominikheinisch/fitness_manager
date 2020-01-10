from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.test import Client, TestCase

from ..models import Activity, Meal


class RegisterTests(TestCase):
    def test_view_get(self):
        url = reverse('fitness_app:register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_register_view_create_user(self):
        username = 'RegisterTestUser'

        def get_user_from_db():
            return len(get_user_model().objects.all().filter(username=username)) == 1

        self.assertFalse(get_user_from_db())
        client = Client()
        response = client.post(reverse('fitness_app:register'),
                               {'username': username, 'password1': 'TestPassword', 'password2': 'TestPassword'})
        self.assertEquals(response.status_code, 302)
        self.assertTrue(get_user_from_db())


class DefaultSetUp(TestCase):
    fixtures = ['default_db.yaml']

    def setUp(self):
        self.User = get_user_model()
        # setting encrypted passwords from plaintext
        for user in self.User.objects.all():
            user.set_password(user.password)
            user.save()

    def assert_success_get(self, url_reverse):
        url = reverse(url_reverse)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class LoginTests(DefaultSetUp):
    def test_login_view_post_success(self):
        response = Client().post(reverse('fitness_app:login'), {'username': 'TestUser', 'password': 'TestUserPassword'})
        self.assertRedirects(response, reverse('fitness_app:index'))

    def test_view_get(self):
        self.assert_success_get('fitness_app:login')


class LoginSetUp(DefaultSetUp):
    def setUp(self):
        super().setUp()
        login_status = self.client.login(username='TestUser', password='TestUserPassword')
        self.assertTrue(login_status)


class LogoutTests(LoginSetUp):
    def test_logout_view(self):
        url = reverse('fitness_app:logout')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('fitness_app:index'), target_status_code=302)


class IndexTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:index')


class SettingsTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:settings')


class GoalsTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:goals')


class PasswordTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:password')


class ActivityTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:activity')

    def test_view_activity_addition_success(self):
        activity_data = {'date': '2020-01-01', 'duration': '15', 'Sport': 'running'}

        def get_activity_from_db():
            return Activity.objects.all().get(**activity_data)

        with self.assertRaises(ObjectDoesNotExist):
            get_activity_from_db()
        self.client.post(reverse('fitness_app:activity'), {
            **activity_data, 'add': '', 'from_date': '01/01/2020', 'to_date': '01/31/2020',
        })
        self.assertTrue(get_activity_from_db())


class MealsTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:meals')

    def test_view_meal_addition_success(self):
        meal_data = {'date_time': '2020-01-01T12:00'}

        def get_meal_from_db():
            return Meal.objects.all().get(**meal_data)

        with self.assertRaises(ObjectDoesNotExist):
            get_meal_from_db()
        self.client.post(reverse('fitness_app:meals'), {
            **meal_data, 'add': '', 'from_date': '01/01/2020', 'to_date': '01/31/2020',
            'form-TOTAL_FORMS': ['0'], 'form-INITIAL_FORMS': ['0'],
        })
        self.assertTrue(get_meal_from_db())

    def test_view_more_success(self):
        response = self.client.post(reverse('fitness_app:meals'), {
            'more': '2020-01-01', 'from_date': '01/01/2020', 'to_date': '01/31/2020',
            'form-TOTAL_FORMS': ['0'], 'form-INITIAL_FORMS': ['0'],
        })
        self.assertRedirects(response, reverse('fitness_app:meals_of_day', kwargs={'year': 2020, 'month': 1, 'day': 1}))


class MealsOfDay(LoginSetUp):
    def test_view_get(self):
        url = reverse('fitness_app:meals_of_day', kwargs={'year': 2020, 'month': 1, 'day': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def post_set_up(self, post_data):
        url = reverse('fitness_app:meals_of_day', kwargs={'year': 2020, 'month': 1, 'day': 1})
        return self.client.post(url, {
            **post_data, 'current_meal_id': '1', 'from_date': '01/01/2020', 'to_date': '01/31/2020',
            'meals-TOTAL_FORMS': ['1'], 'meals-INITIAL_FORMS': ['1'],
            'portions-TOTAL_FORMS': ['0'], 'portions-INITIAL_FORMS': ['0'],
        })

    def test_view_choose_meal_success(self):
        response = self.post_set_up({'choose_meal': '1'})
        self.assertEquals(response.status_code, 200)

    def test_view_save_portion_nothing_to_do(self):
        response = self.post_set_up({'save': ''})
        self.assertEquals(response.status_code, 200)

    def test_view_del_portion_success(self):
        response = self.post_set_up({'del_portion': '0'})
        self.assertEquals(response.status_code, 200)

    def test_view_del_meal_success(self):
        response = self.post_set_up({'del_meal': '1'})
        self.assertRedirects(response, reverse('fitness_app:meals'))
