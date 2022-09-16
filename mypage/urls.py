from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.mypageIndex, name='mypage'),
    path('passwordUpdate/', views.passwordUpdate, name='passwordUpdate'),
    path('userinfoUpdate/', views.userinfoUpdate, name='userinfoUpdate'),
    path('userinfoUpdate/update/', views.userinfoUpdateUpdate, name='userinfoUpdateUpdate'),
    path('lecture/', views.lecture, name='lecture'),
    path('lectureDelete/', views.lectureDelete, name='lectureDelete'),
    path('mypageadmin/', views.mypageAdmin, name='mypageAdmin'),
    path('chat/chat_index/', views.chat_index, name='chat_index'),
    # path('chat/<str:room_name>/', views.room, name='room_test'),
    path('reservationChat/', views.reservationChat, name='reservationChat'),
    path("chat_view/", views.chat_view, name="chat"),  # /chat/으로 넘어오면 chat_view 함수 실행
    path("chat/<str:room_name>/<str:with_name>/", views.room_view, name="room"),  # /chat/room_number/ 으로 넘어오면 room 함수 실행
    path("api/<str:email>", views.api_create_room, name="api_create_room"),
    # path('chat_propose/<str:email>/', views.chat_propose, name='chat_propose'),
    # path('chat_cancel/<int:id>/', views.chat_cancel, name='chat_cancel'),
    # path('chat_accept/<int:id>/', views.chat_accept, name='chat_accept'),

]
