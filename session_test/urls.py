from django.urls import path
from . import views

app_name = 'session-test'

urlpatterns = [
    path('countup/', views.countup, name='countup'),
    path('', views.index, name='index'),
]