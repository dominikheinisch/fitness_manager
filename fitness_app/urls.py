from django.urls import path

from . import views

app_name = 'fitness_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('<int:user_id>/', views.detail, name='detail'),
    path('<int:user_id>/settings', views.settings, name='settings'),
]
