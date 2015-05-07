from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Student, Subject, Question, Course, Professor, Result, Done
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import string
import random
from django.conf import settings
from django.core.mail import send_mail


def home(request):
    return render(request, 'feedback/getmail.html')


@login_required(login_url='/login/?next=/feedback/')
def index(request):
    if request.user.is_authenticated():
        student = Student.objects.filter(email=request.user.username)
        done_list = student[0].done_set.all()
        return render(request, 'feedback/course2.html', {'student': student[0], 'done_list': done_list})
    else:
        return HttpResponseRedirect(reverse('login'))

def index2(request,key):
    user = get_object_or_404(User,first_name=key)
    student = Student.objects.get(email=user.username)
    done_list = student.done_set.all()
    return render(request, 'feedback/course2.html', {'student': student, 'done_list': done_list})


def Login(request):
    if request.user.is_authenticated():
        return render(request, 'feedback/session.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.username
                if user.is_staff:
                    return redirect('feedback:analyse')
                else:
                    pass
                return HttpResponseRedirect(reverse('feedback:index'))
            else:
                return HttpResponse("User Inactive")

        else:
            return render(request, 'feedback/login.html')


def Logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    logout(request)
    return render(request, 'feedback/logout.html')


def register(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                new_user.save()
                return render(request, 'feedback/success.html')
            else:
                return render(request, 'feedback/unsuccess.html')
        else:
            form = UserCreationForm()
            return render(request, 'feedback/registration.html', {'form': form}, )
    else:
        return render(request, 'feedback/logoutfirst.html')


def success(request):
    return render(request, 'feedback/success.html')


def unsuccess(request):
    return render(request, 'feedback/unsuccess.html')

'''
@login_required(login_url='/login/')
def polls(request, prof_pk, stud_roll, sub_pk):
    student = Student.objects.get(roll_no=stud_roll)
    if request.user.username == student.email:
        professor = Professor.objects.get(pk=prof_pk)
        subject = Subject.objects.get(pk=sub_pk)
        course = Course.objects.filter(subject=subject, professor=professor)
        course = course[0]
        d = student.done_set.all()
        result_list = course.result_set.all()

        for done in d:
            if done.course == course:
                if done.student == student:
                    key = done.done
        if not key:
            if request.method == "POST":
                for result in result_list:
                    choice = request.POST.get(result.question.question_text)
                    if choice == 'excellent':
                        result.excellent_votes += 1
                        result.save()
                    elif choice == 'verygood':
                        result.verygood_votes += 1
                        result.save()
                    elif choice == 'good':
                        result.good_votes += 1
                        result.save()
                    elif choice == 'fair':
                        result.fair_votes += 1
                        result.save()
                    elif choice == 'poor':
                        result.poor_votes += 1
                        result.save()

                    result.total_votes = (
                        result.excellent_votes + result.verygood_votes + result.good_votes + result.fair_votes + result.poor_votes)
                    result.save()

                comment_text1 = request.POST.get("comment_1")
                comment_text2 = request.POST.get("comment_2")
                comment_text3 = request.POST.get("comment_3")
                comment_text4 = request.POST.get("comment_4")
                course.comment_set.create(comment_1=comment_text1,
                                          comment_2=comment_text2,
                                          comment_3=comment_text3,
                                          comment_4=comment_text4, )

                for done in d:
                    if done.course == course:
                        if done.student == student:
                            done.done = 1
                            done.save()
                return HttpResponseRedirect(reverse('feedback:index'))
            else:
                return render(request, 'feedback/questions2.html', {'result_list1': result_list[:5],
                                                                    'result_list2': result_list[5:10],
                                                                    'result_list3': result_list[10:14],
                                                                    'result_list4': result_list[14:19],
                                                                    'result_list5': result_list[19:21],
                                                                    'course': course,
                                                                    'professor': professor,
                                                                    'subject': subject, })


        else:
            return render(request, 'feedback/submitted.html')


    else:
        return render(request, 'feedback/logoutfirst.html')'''


def polls2(request, prof_pk, stud_roll, sub_pk):
    student = Student.objects.get(roll_no=stud_roll)
    professor = Professor.objects.get(pk=prof_pk)
    subject = Subject.objects.get(pk=sub_pk)
    course = Course.objects.filter(subject=subject, professor=professor)
    course = course[0]
    d = student.done_set.all()
    result_list = course.result_set.all()

    for done in d:
        if done.course == course:
            if done.student == student:
                key = done.done
    if not key:
        if request.method == "POST":
            for result in result_list:
                choice = request.POST.get(result.question.question_text)
                if choice == 'excellent':
                    result.excellent_votes += 1
                    result.save()
                elif choice == 'verygood':
                    result.verygood_votes += 1
                    result.save()
                elif choice == 'good':
                    result.good_votes += 1
                    result.save()
                elif choice == 'fair':
                    result.fair_votes += 1
                    result.save()
                elif choice == 'poor':
                    result.poor_votes += 1
                    result.save()

                result.total_votes = (
                        result.excellent_votes + result.verygood_votes + result.good_votes + result.fair_votes + result.poor_votes)
                result.save()

                comment_text1 = request.POST.get("comment_1")
                comment_text2 = request.POST.get("comment_2")
                comment_text3 = request.POST.get("comment_3")
                comment_text4 = request.POST.get("comment_4")
                course.comment_set.create(comment_1=comment_text1,
                                          comment_2=comment_text2,
                                          comment_3=comment_text3,
                                          comment_4=comment_text4, )

                for done in d:
                    if done.course == course:
                        if done.student == student:
                            done.done = 1
                            done.save()
            return HttpResponseRedirect(reverse('feedback:index'))
        else:
            return render(request, 'feedback/questions2.html', {'result_list1': result_list[:5],
                                                                    'result_list2': result_list[5:10],
                                                                    'result_list3': result_list[10:14],
                                                                    'result_list4': result_list[14:19],
                                                                    'result_list5': result_list[19:21],
                                                                    'course': course,
                                                                    'professor': professor,
                                                                    'subject': subject, })


    else:
        return render(request, 'feedback/submitted.html')



@login_required(login_url='/login/')
def analyse(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            professor_list = Professor.objects.all()
            return render(request, 'feedback/analyse.html', {'professor_list': professor_list})
        else:
            return HttpResponse("Not a valid memeber")
    else:
        return HttpResponse("Please Login First")


@login_required(login_url='/login/')
def courseanalyse(request, prof_pk):
    if request.user.is_authenticated():
        if request.user.is_staff:
            professor = Professor.objects.get(pk=prof_pk)
            course_list = professor.course_set.all()

            return render(request, 'feedback/courseanalyse.html', {'course_list': course_list, 'professor': professor})
        else:
            return HttpResponse("Not a valid memeber")
    else:
        return HttpResponse("Please Login First")


def getmail(request):
    email = request.POST.get('email')
    user = User.objects.get(username=email)
    key=user.first_name
    text = "Submit the coursefeedback form by clicking this link: http://10.1.1.239/feedback/"+key+"/"
    send_mail('Course Change Portal', text, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    return HttpResponse("<b>An email has been sent to your email address.Please Follow the link in the email</b>")

def getmail2(request):
    email = request.POST.get("email")
    user = get_object_or_404(User, username=email)
    return HttpResponse(user.username)