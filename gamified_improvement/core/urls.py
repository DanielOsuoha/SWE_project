from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('goals/', views.goals, name='goals'),
    path('plans/', views.plans, name='plans'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
]