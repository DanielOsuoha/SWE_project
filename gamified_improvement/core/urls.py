from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('friends/', views.friends, name='friends'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('plan/<int:pk>/', views.plan_detail, name='plan_detail'),
    ]