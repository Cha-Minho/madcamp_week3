from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import ChatRoom
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import chat_dict_module

def index(request):
    return render(request, 'chat/index.html', {})

@csrf_exempt
def room(request, room_name):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        chat_dict_module.chatDict[room_name] = []
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
        chat_dict_module.chatDict[room_name] = []
        if room_name:
            chat_room = ChatRoom.objects.create(name=room_name, url=f'/chat/{room_name}/')
            chat_room.save()
            return redirect(chat_room.url)
    return render(request, 'chat/index.html')

def chat_list(request):
    if 'live' in chat_dict_module.chatDict:
        del chat_dict_module.chatDict['live']
    chat_rooms = chat_dict_module.chatDict.items() 
    active_rooms = []
    for room in chat_rooms:
        if len(room[1]):
            active_rooms.append(room)
    return render(request, 'chat/chat_list.html', {'chat_rooms': active_rooms}) 
