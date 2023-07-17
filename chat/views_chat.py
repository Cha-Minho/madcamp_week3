from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import ChatRoom
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})

@csrf_exempt
def room(request, room_name):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        if room_name:
            chat_room = ChatRoom.objects.create(name=room_name, url=f'/chat/{room_name}/')
            chat_room.save()
            return redirect(chat_room.url)
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

@csrf_exempt
def create_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        if room_name:
            chat_room = ChatRoom.objects.create(name=room_name, url=f'/chat/{room_name}/')
            chat_room.save()
            return redirect(chat_room.url)
    return render(request, 'chat/index.html')

def chat_list(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/chat_list.html', {'chat_rooms': chat_rooms})