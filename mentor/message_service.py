from django.db.models import QuerySet

from mentor.message import Message


def creat_an_message(email: str, room_id: int, message: str) -> Message:
    return Message.objects.create(email=email, room_id=room_id, message=message)


def get_an_message_list(room_id: int) -> QuerySet[Message]:
    return Message.objects.filter(room_id=room_id)
