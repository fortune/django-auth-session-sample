

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('mylogin/', views.login, name='mylogin'),
]