from django.core.paginator import Paginator
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
    context = {'mentorList': page_obj, "userList": userList}
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

def mentor_chatrooms(request):
    return render(request, 'mentor/mentor_chatrooms.html')

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