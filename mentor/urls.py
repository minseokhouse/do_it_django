from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mentor, name='mentor'),
    path('mentor_up/', views.mentor_up, name='upload_mento'),
    path('mentor_content/', views.mentor_content, name='mentor_content'),
    path('mentor_profile/<str:email>/', views.mentor_profile, name='mentor_profile'),
    path('mentor_chat_propose/<str:email>/', views.chat_propose, name='mentor_chat_propose'),
    path('mentor_chatrooms/<str:myEmail>/<str:id>/', views.mentor_chatrooms, name='mentor_chatrooms'),
    path('search', views.search, name='search'),
    path("api/<str:email>", views.api_create_room, name="api_create_room")
]