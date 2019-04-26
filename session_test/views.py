from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

# Create your views here.


def index(request):
    #return HttpResponse('Hello')
    session = request.session
    count = session.get('count')
    
    return render(request, 'session_test/home.html', {'count': count, 'session_key': session.session_key})


def countup(request):
    session = request.session
    count = session.setdefault('count', 0)
    session['count'] += 1

    return render(request, 'session_test/home.html', {'count': count, 'session_key': session.session_key})
