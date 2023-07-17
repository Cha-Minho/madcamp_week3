import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import InvalidChannelLayerError
from channels.db import database_sync_to_async
from .models import Donation, ChatRoom
import time
import chat_dict_module

viewer_cnt = 0
# 비동기식
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if self.room_name != "live":
            chat_dict_module.chatDict[self.room_name] += 1
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.room_name != "live":
            chat_dict_module.chatDict[self.room_name] -= 1
            if chat_dict_module.chatDict[self.room_name] == 0:
                await self.delete_room_if_empty(self.room_name)
                del chat_dict_module.chatDict[self.room_name]


        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # username = text_data_json.get('username', 'anonymous')  # 유저 이름을 가져오되, 없으면 'anonymous'를 기본값으로 사용
        username = self.scope["session"]["username"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{username}: {message}'  # 유저 이름과 메시지 함께 보내기
            }
        )

    @database_sync_to_async
    def delete_room_if_empty(self, room_name):
        try:
            room = ChatRoom.objects.get(name=room_name)
            room.delete()
        except ChatRoom.DoesNotExist:
            pass
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class DonationConsumer(AsyncJsonWebsocketConsumer):
    drawing_rights = {}
    
    async def connect(self):
        self.room_group_name = 'donations'
        self.drawing_rights[self.scope["session"]["username"]] = [0, time.time()]
        global viewer_cnt
        viewer_cnt += 1
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        d = {'type': "update_viewer", 'count': viewer_cnt}
        json_data = json.dumps(d)
        await self.receive(json_data)

    async def disconnect(self, close_code):
        # Leave room group
        print("disconnectig")
        global viewer_cnt
        viewer_cnt -= 1
        username = self.scope["session"]["username"]
        # if username in self.drawing_rights:
        #     del self.drawing_rights[username]  # new
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        d = {'type': "update_viewer", 'count': viewer_cnt}
        json_data = json.dumps(d)
        await self.receive(json_data)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        if message_type == 'donation':
            username = self.scope["session"]["username"]
            donation_amount = text_data_json.get('amount', '0')
            donation_message = text_data_json.get('dM', '')

            if int(donation_amount) > 0:
                # Create a new donation object
                donation = Donation(donor=username, amount=donation_amount)
                # Save the donation object in the database
                await database_sync_to_async(donation.save)()
                token = self.drawing_rights[username][0]
                # Grant drawing rights
                self.drawing_rights[username] = [token + int(donation_amount) // 1000, time.time()]  # new

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'donation_message',
                        'message': f'{username}님 {int(donation_amount)//100} 누들 후원 감사합니다! <br> {donation_message}',
                    }
                )

        elif message_type == 'draw':
            username = self.scope["session"]["username"]
            if self.drawing_rights[username][0] > 0:
                time_cha = time.time() - self.drawing_rights[username][1]
                if  time_cha > 1:
                    self.drawing_rights[username][0] -= time_cha // 1
                    self.drawing_rights[username][1] = time.time()
                    print("draw", self.drawing_rights[username][0])
                # else:
                #     self.drawing_rights[username][0] = 0
                #     self.drawing_rights[username][1] = time.time()
                x = text_data_json.get('x')
                y = text_data_json.get('y')
                radius = text_data_json.get('radius')
                color = text_data_json.get('color')
                if self.drawing_rights[username][0] <= 0:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'draw',
                            'x': x,
                            'y': y,
                            'radius': radius,
                            'color': color,
                            'done': "true"
                        }
                    )
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'draw',
                            'x': x,
                            'y': y,
                            'radius': radius,
                            'color': color,
                            'done' : "false",
                        }
                    )
        elif message_type == "update_viewer":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'viewer_update',
                    'message': str(text_data_json.get('count')),
                }
            )

    async def viewer_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'viewer_update',
            'message': message
        }))
    # Receive message from room group
    async def donation_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': "donation",
            'message': message
        }))

    async def draw(self, event):
        x = event['x']
        y = event['y']
        radius = event['radius']
        color = event['color']
        done = event['done']

        await self.send(text_data=json.dumps({
            'type': "draw",
            'x': x,
            'y': y,
            'radius': radius,
            'color': color,
            'done' : done,
        }))
