# chat/consumers.py
from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from mentor.room import Room
from mentor.message import Message

# 동기식 방법으로 진행
from user.models import User


def message_to_json(message):
    return {
        'author': message.email.name,
        'content': message.message,
        'timestamp': str(message.created_at + timedelta(hours=9))
    }


def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))
    return result


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        room_id = int(self.room_name)
        messages = Message.last_30_messages(self, room_id)
        content = {
            'command': 'messages',
            'messages': messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user_email = data['user']
        room_id = int(self.room_name)
        user_contact = User.objects.filter(email=user_email)[0]
        room_contact = Room.objects.filter(id=room_id)[0]
        message_creat = Message.objects.create(
            email=user_contact,
            room_id=room_contact,
            message=data['message']
        )
        content = {
            'command': 'new_message',
            'message': message_to_json(message_creat)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    # websocket 연결
    def connect(self):
        # room_name 파라미터를 chat/routing.py URl 에서 얻고, 열러있는 websocket에 접속
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # 인용이나 이스케이프 없이 사용자 지정 방 이름에서 직접 채널 그룹 이름을 구성
        # 그룹 이름에는 문자, 숫자, 하이픈 및 마침표만 사용할 수 있어서 튜토리얼 예제 코드는 다른 문자가 있는 방이름 에서는 실패
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group / 그룹에 참여
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # websocket 연결을 수락 / connect() 메서드 내에서 accept()를 호출하지 않으면 연결이 거부되고 닫힌다.
        self.accept()

    # websocket 연결 해제
    def disconnect(self, close_code):
        # Leave room group / 그룹에서 탈퇴
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
