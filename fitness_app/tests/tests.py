from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase


class RegisterTests(TestCase):
    def test_register_view_get(self):
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
    def test_login_view__post_success(self):
        response = Client().post(reverse('fitness_app:login'), {'username': 'TestUser', 'password': 'TestUserPassword'})
        self.assertRedirects(response, reverse('fitness_app:index'))

    def test_login_view_get(self):
        self.assert_success_get('fitness_app:login')


class LoginSetUp(DefaultSetUp):
    def setUp(self):
        super().setUp()
        login_status = self.client.login(username='TestUser', password='TestUserPassword')
        self.assertTrue(login_status)


class IndexTests(LoginSetUp):
    def test_index_view_get(self):
        self.assert_success_get('fitness_app:index')


class ActivityTests(LoginSetUp):
    def test_index_view_get(self):
        self.assert_success_get('fitness_app:activity')


class MealsTests(LoginSetUp):
    def test_index_view_get(self):
        self.assert_success_get('fitness_app:meals')


class MealsOfDay(LoginSetUp):
    def test_index_view_get(self):
        url = reverse('fitness_app:meals_of_day', args=[2020, 1, 1])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
