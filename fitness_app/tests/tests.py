from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.test import Client, TestCase

from ..models import Activity


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
        response = self.client.post(reverse('fitness_app:activity'), {
            **activity_data, 'add': '', 'from_date': '01/01/2020', 'to_date': '01/31/2020',
        })
        self.assertTrue(get_activity_from_db())


class MealsTests(LoginSetUp):
    def test_view_get(self):
        self.assert_success_get('fitness_app:meals')


class MealsOfDay(LoginSetUp):
    def test_view_get(self):
        url = reverse('fitness_app:meals_of_day', args=[2020, 1, 1])
        response = self.client.get(url)
