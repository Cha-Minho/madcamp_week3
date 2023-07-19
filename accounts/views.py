from django.shortcuts import render, redirect
import json
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm
from .models import User, Broadcast
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.http import StreamingHttpResponse, JsonResponse
import requests
import ffmpeg
import os 
from django.conf import settings
from datetime import datetime
from django.urls import reverse

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
        else:
            form.add_error('username', '이미 존재하는 아이디거나 비밀번호가 일치하지 않습니다.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            if password == user.password:
                request.session['username'] = user.username
                request.session['isAuthenticated'] = 'true'
                response = redirect('home')
                return response
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'base.html')

def user_logout(request):
    del(request.session['username'])
    request.session['isAuthenticated'] = 'false'
    request.session.modified = True
    return redirect('home')


def get_session_data(request):
    username = request.session.get('username')
    isAuthenticated = request.session.get('isAuthenticated')

    data = {
        'username': username,
        'isAuthenticated': isAuthenticated,
    }

    return JsonResponse(data)

def live(request):
    return render(request, 'live.html')

def proxy_view(request, path=''):
    url = f"http://10.10.20.103/stream/hls/{path}"

    req = requests.get(url, stream=True)

    response = StreamingHttpResponse((chunk for chunk in req.iter_content(chunk_size=512)), content_type=req.headers['content-type'])

    return response

@csrf_exempt
def replay(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video = request.FILES.get('video')
        name = request.session['username']
        if title and video: 
            Broadcast.objects.create(title=title, video=video, name = name)
            return HttpResponseRedirect(reverse('replay')) 
    
    broadcasts = Broadcast.objects.all().order_by('-id')
    return render(request, 'abc.html', {'broadcasts': broadcasts})