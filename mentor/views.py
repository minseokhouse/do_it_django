import MySQLdb
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mentor.models import Mentor
from mypage.models import Chat_Propose
from user.models import User


def mentor(request):
    mentorList = Mentor.objects.all().order_by('mentor_id')
    page = request.GET.get('page', '1')
    paginator = Paginator(mentorList, 16)
    page_obj = paginator.get_page(page)
    userList = User.objects.all()
    session_email = request.session['user']
    context = {'mentorList': page_obj, "userList": userList, "myEmail": session_email}
    return render(request, 'mentor/mentor.html', context)


def mentor_up(request):
    if request.method == 'POST':
        Mentor(
            mentor=request.POST['mentor'],
            mentor_img=request.FILES['mentor_img'],
            mento_title=request.POST['mento_title'],
            mento_content=request.POST['mento_content'],
            mento_type=request.POST['mento_type'],
            email=User.objects.get(email=request.POST['email'])
        ).save()
        return redirect('mentor')

    user_object = User.objects.all().order_by('email')
    user_context = {'userList': user_object}
    return render(request, 'mentor/mentor_upload.html', user_context)


def mentor_content(request):
    return render(request, 'mentor/mentor_content.html')


def mentor_profile(request, email):
    mento = Mentor.objects.get(email=email)
    context = {'mento': mento}
    return render(request, 'mentor/mentor_profile.html', context)


def mentor_chatrooms(request: HttpRequest, myEmail: str, id: str) -> HttpResponse:
    print('id:' + id)
    login_user = User.objects.get(email=myEmail)
    my_role = login_user.role
    conn = MySQLdb.connect(host='localhost', user='root', passwd='Fleur0320!@#', db='django_insta')
    cur = conn.cursor()
    cur.nextset()
    myEmail2 = "'" + myEmail + "'"
    print(myEmail2)
    if my_role == 'Parents':
        print('parents')
        query = "select user_user.name, room_join.email, date_add(message.updated_at, interval 9 hour), message.message, message.room_id from user_user as user_user inner join roomjoin as room_join on user_user.email = room_join.email inner join message as message on room_join.room_id = message.room_id where message.id in ( select max(id) from message group by room_id) and user_user.role != 'Parents' and room_join.room_id in (select room_id from roomjoin where email =" + myEmail2 + ")"
        # query = "select user_user.name, room_join.email, message.updated_at, message.message, message.room_id from user_user as user_user inner join roomjoin as room_join on user_user.email = room_join.email inner join message as message on room_join.room_id = message.room_id where message.id in ( select max(id) from message group by room_id) and user_user.role = 'Parents' and room_join.room_id in (select room_id from roomjoin where email =" + myEmail2 + ")"

    else:
        print('not parents')
        query = "select user_user.name, room_join.email, date_add(message.updated_at, interval 9 hour), message.message, message.room_id from user_user as user_user inner join roomjoin as room_join on user_user.email = room_join.email inner join message as message on room_join.room_id = message.room_id where message.id in (select max(id) from message group by room_id) and user_user.role = 'Parents' and room_join.room_id in (select room_id from roomjoin where email =" + myEmail2 + ")"

    result_query = cur.execute(query)
    result_query = cur.fetchall()

    result_out = []
    for data in result_query:
        row = {'name': data[0],
               'email': data[1],
               'updated_at': data[2],
               'message': data[3],
               'room_id': data[4]}

        result_out.append(row)

    print(result_query)
    return render(request, 'mentor/mentor_chatrooms.html',
                  {'result_query': result_out})



    # Chat_Propose.objects.select_related('mentor').filter(my_email=myEmail, Mentor_number=1)
    # bothPropose = Chat_Propose.objects.filter(my_email=myEmail, Mentor_number=1)

    # return render(request, 'mentor/mentor_chatrooms.html',
    #               {'bothPropose': bothPropose})





def chat_propose(request, email):
    print('입장')
    session_email = request.session['user']
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
    # conn = MySQLdb.connect(host='localhost', user='root', passwd='Fleur0320!@#', db='django_insta')
    # cur = conn.cursor()
    # cur.nextset()
    # cur.execute('call propose_chat(%s, %s)', {session_email, email})
    if Chat_Propose.objects.filter(my_email=session_email, email=email).exists():
        return render(request, 'mypage/mypage.html',
                      {'mentoUser': mentoUser, 'isParents': isParents, 'myPropose': myPropose,
                       'receivePropose': receivePropose, 'bothPropose': bothPropose})
    else:
        login_user = User.objects.get(email=session_email)
        Chat_Propose(
            email_id=email,
            name=login_user.name,
            nickname=login_user.nickname,
            my_email=session_email,
            Parents_number=1,
            Mentor_number=0
        ).save()

        return render(request, 'mypage/mypage.html')
        # return redirect('mypage')
        # return redirect('reservationChat')


def search(request):
    context = dict()
    mentorList = Mentor.objects.filter(mentor__icontains="")
