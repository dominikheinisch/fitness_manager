from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'fitness_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('activity', views.activity, name='activity'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
]
