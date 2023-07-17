from django.shortcuts import render, redirect
import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from .forms import SignUpForm, LoginForm
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.http import StreamingHttpResponse, JsonResponse
import requests
import ffmpeg
import os 
from django.conf import settings
from datetime import datetime

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 회원가입 후 로그인 페이지로 이동
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
    # 홈 페이지에 필요한 로직을 작성합니다.
    return render(request, 'base.html')

def user_logout(request):
    del(request.session['username'])
    request.session['isAuthenticated'] = 'false'
    request.session.modified = True
    return redirect('home')

# def live_streaming_on(request):
#     return render(request, 'live_streaming_on.html')

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

