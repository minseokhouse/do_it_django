from typing import Tuple

from django.db.models import QuerySet

from mentor.room import Room
from mentor.room_join import RoomJoin


def creat_an_chat_room() -> Room:
    return Room.objects.create()


def get_an_chat_room(room_id: int) -> Room:
    return Room.objects.get(id=room_id)


def get_an_chat_room_list(email: str) -> QuerySet[RoomJoin]:
    return RoomJoin.objects.filter(email=email)


def get_chat_room_user(room_id: int) -> QuerySet[RoomJoin]:
    return RoomJoin.objects.filter(room_id=room_id)


def creat_an_room_join(user_id1: str, user_id2: str, room_id: int) -> Tuple[RoomJoin, RoomJoin]:
    room_join1 = RoomJoin.objects.create(email=user_id1, room_id=room_id)
    room_join2 = RoomJoin.objects.create(email=user_id2, room_id=room_id)
    return room_join1, room_join2


def confirm_user_chat_room_join(user_id: str, room_id: int) -> RoomJoin:
    return RoomJoin.objects.get(email=user_id, room_id=room_id)