from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('friends/', views.friends, name='friends'),
    path('profile/', views.profile, name='profile'),
]