from collections import Counter

import bcrypt
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

from user.models import User
from mentor.chat_room_service import get_an_chat_room_list, get_chat_room_user, confirm_user_chat_room_join, \
    creat_an_chat_room, creat_an_room_join
from mentor.message_service import get_an_message_list
# from .models import Chat_Propose
from mentor.room_join import RoomJoin


# Create your views here.
def mypageIndex(request):
    return render(request, 'mypage/mypage.html')


def lecture(request, ):
    return render(request, "mypage/lecture.html")


def lectureDelete(request, ):
    return render(request, "mypage/lectureDelete.html")


def mypageAdmin(request):
    return render(request, 'mypage/myadminmain.html')


def passwordUpdate(request):
    session_user = request.session['user']
    print("session_user", session_user)

    if request.method == 'POST':
        if User.objects.filter(email=session_user).exists():
            user = User.objects.get(email=session_user)
            user_password = user.password.encode('utf=8')

            if bcrypt.checkpw(request.POST['nowpwd'].encode('utf=8'), user_password):
                update_password = request.POST['updatepwd']
                hashed_password = bcrypt.hashpw(update_password.encode('utf=8'), bcrypt.gensalt())
                user.password = hashed_password.decode('utf=8')
                user.save()
                return redirect('passwordUpdate')

            return render(request, "mypage/password.html")
    else:
        return render(request, 'mypage/password.html')


def userinfoUpdate(request):
    userinfo_object = User.objects.get(email=request.session['user'])
    return render(request, 'mypage/userinfo.html', {'userinfo': userinfo_object})


def userinfoUpdateUpdate(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.session['user']):
            user = User.objects.get(email=request.session['user'])
            user.name = request.POST['name']
            user.nickname = request.POST['nickname']
            user.tel = request.POST['tel']
            user.save()
            return redirect('userinfoUpdate')
        return render(request, 'mypage/userinfo.html')
    else:
        return render(request, 'mypage/userinfoUpdate.html')


def reservationChat(request):
    mentoUser = User.objects.filter(role='Mentor')
    session_user = request.session['user']
    login_user = User.objects.get(email=session_user)
    if login_user.role == 'Parents':
        isParents = True
        bothPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=1)
    else:
        isParents = False
        bothPropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=1)

    myPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=0)
    receivePropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=0, Parents_number=1)

    return render(request, 'mypage/reservationChat.html',
                  {'mentoUser': mentoUser, 'isParents': isParents, 'myPropose': myPropose,
                   'receivePropose': receivePropose, 'bothPropose': bothPropose})


def chat_index(request):
    return render(request, 'mypage/chat/chat_index.html', {})


def room(request, room_name):
    userinfo_object = User.objects.get(email=request.session['user'])
    return render(request, 'mypage/chat/room.html', {'room_name': room_name, 'userinfo_object': userinfo_object})


# Create your views here. / views 호출하려면 매핑되는 URLconf 필요
# chat_view 함수를 호출하면 chat.html 을 렌더해주는 함수
def chat_view(request: HttpRequest) -> HttpResponse:
    # 사용자가 있는지 없는지 판단
    user = request.User.is_authenticated
    # 사용자가 있으면 사용자가 속해있는 채팅방 list 표시
    if user:
        # 유저가 참여하고 있는 채팅방 목록(roomJoin 쿼리)
        chat_room_list = get_an_chat_room_list(request.User.email)

        chat_info = {}
        for chat_room in chat_room_list:
            room_id = chat_room.room_id.id
            # 채팅방에 참여중인 유저 list(roomJoin 쿼리)
            chat_user_list = get_chat_room_user(room_id)

            username_list = []
            for chat_user in chat_user_list:
                username = chat_user.email.username
                username_list.append(username)

            # chat_info 변수에 딕셔너리 형태로 저장
            chat_info[room_id] = username_list

        if chat_info == {}:
            chat_info = None

        return render(request, "mypage/chat/chat.html", {'chat_info': chat_info})
    # 사용자가 없으면 로그인화면
    else:
        return redirect(("login"))


# room 함수를 호출하면 room.html 을 렌더해주는 함수 / dict 형태로 room_name value 를 전송
def room_view(request: HttpRequest, room_name: str, with_name: str) -> HttpResponse:
    room_id = str(room_name)
    session_user = request.session['user']
    login_user = User.objects.get(email=session_user)
    print(room_id)
    try:

        # confirm_user_chat_room_join(request.user.id, room_id)
        confirm_user_chat_room_join(with_name, room_id)

        message = get_an_message_list(room_id)

        return render(request, "mypage/chat/room.html",
                      {"room_name": room_name, "message": message, "login_user": login_user})

    except:
        return redirect(("/"))


def api_create_room(request: HttpRequest, email: str) -> HttpResponse:
    print('여기 입장')
    user1 = User.objects.get(email=email)
    session = request.session['user']
    user2 = User.objects.get(email=session)

    find_room_qs = RoomJoin.objects.filter(email__in=[user1.email, user2.email])
    # 이러면 1번 유저가 참여한 모든 방, 2번 유저가 모두 참여한 방 가져옴

    find_room_list = []
    for find_room in find_room_qs:
        find_room_list.append(find_room.room_id)

    result = Counter(find_room_list)
    for key, value in result.items():
        if value >= 2:
            print('이미 있다')
            print(str(key.id))
            print(user1.email)
            return redirect("../chat/" + str(key.id) + "/" + str(user1.email))

    room = creat_an_chat_room()
    room_id = room.id
    creat_an_room_join(user1, user2, room)
    print('여기도 입장')
    return redirect(("../chat/" + str(room_id) + "/" + str(user1.email)))
    # return redirect(("/chat/" + str(room_id)))


# def chat_propose(request, email):
#     print('입장')
#     session_email = request.session['user']
#     mentoUser = User.objects.filter(role='Mentor')
#     session_user = request.session['user']
#     login_user = User.objects.get(email=session_user)
#     if login_user.role == 'Parents':
#         isParents = True
#         bothPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=1)
#     else:
#         isParents = False
#         bothPropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=1)
#
#     myPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=0)
#     receivePropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=0, Parents_number=1)
#     # conn = MySQLdb.connect(host='localhost', user='root', passwd='Fleur0320!@#', db='django_insta')
#     # cur = conn.cursor()
#     # cur.nextset()
#     # cur.execute('call propose_chat(%s, %s)', {session_email, email})
#     if Chat_Propose.objects.filter(my_email=session_email, email=email).exists():
#         return redirect('../../../mentor/')
#         # return render(request, 'mypage/reservationChat.html',
#         #               {'mentoUser': mentoUser, 'isParents': isParents, 'myPropose': myPropose,
#         #                'receivePropose': receivePropose, 'bothPropose': bothPropose})
#     else:
#         login_user = User.objects.get(email=session_email)
#         Chat_Propose(
#             email_id=email,
#             name=login_user.name,
#             nickname=login_user.nickname,
#             my_email=session_email,
#             Parents_number=1,
#             Mentor_number=0
#         ).save()
#         return redirect('../../../mentor/')
#         # return render(request, 'mypage/reservationChat.html',
#         #               {'mentoUser': mentoUser, 'isParents': isParents, 'myPropose': myPropose,
#         #                'receivePropose': receivePropose, 'bothPropose': bothPropose})
#         # # return redirect('mypage')
#         # return redirect('reservationChat')


# def chat_cancel(request, id):
#     print('취소')
#     chat_id = get_object_or_404(Chat_Propose, id=id)
#     chat_id.delete()
#     mentoUser = User.objects.filter(role='Mentor')
#     session_user = request.session['user']
#     login_user = User.objects.get(email=session_user)
#     if login_user.role == 'Parents':
#         isParents = True
#         bothPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=1)
#     else:
#         isParents = False
#         bothPropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=1)
#
#     myPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=0)
#     receivePropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=0, Parents_number=1)
#
#     return render(request, 'mypage/reservationChat.html',
#                   {'mentoUser': mentoUser, 'isParents': isParents, 'myPropose': myPropose,
#                    'receivePropose': receivePropose, 'bothPropose': bothPropose})
#
#     # return render(request, 'mypage/mypage.html')
#     # return redirect('mypage')


# def chat_accept(request, id):
#     print('수락')
#     chat_id = get_object_or_404(Chat_Propose, id=id)
#     chat_id.Mentor_number = 1
#     chat_id.save()
#     mentoUser = User.objects.filter(role='Mentor')
#     session_user = request.session['user']
#     login_user = User.objects.get(email=session_user)
#     if login_user.role == 'Parents':
#         isParents = True
#         bothPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=1)
#     else:
#         isParents = False
#         bothPropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=1)
#
#     myPropose = Chat_Propose.objects.filter(my_email=session_user, Mentor_number=0)
#     receivePropose = Chat_Propose.objects.filter(email_id=session_user, Mentor_number=0, Parents_number=1)
#     return render(request, 'mypage/reservationChat.html',
#                   {'mentoUser': mentoUser, 'isParents': isParents, 'myPropose': myPropose,
#                    'receivePropose': receivePropose, 'bothPropose': bothPropose})
