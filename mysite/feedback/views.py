from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from feedback import forms
from feedback.models import Task, Course, Student, Professor, CourseStudentProfessor
from django.contrib.auth.models import Group
from django.views.generic.base import TemplateView
import random

from graphos.renderers import highcharts
from graphos.sources.simple import SimpleDataSource
import json
import time
import urllib2
import datetime


#----------------------------------------------------------------
# User Authentication
#----------------------------------------------------------------

def login(request):
    """
    Authenticates user from the username and password from POST
    """
    if request.POST:
        form = forms.CaptchaTestForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                try:
                    student = request.user.student
                except Student.DoesNotExist:
                    student = None
                try:
                    professor = request.user.professor
                except Professor.DoesNotExist:
                    professor = None
                if professor is None and student is not None:
                    return HttpResponseRedirect('/feedback/student/home/')
                elif professor is not None and student is None:
                    return HttpResponseRedirect('/feedback/prof/home/')
                else:
                    response = str(student)
                    response+=str(professor)
                    return HttpResponse(response)

            else:
                # Return an 'invalid login' error message.
                form_errors = 'The username or password did not match with our records.'
                return render_to_response('feedback/login.html',
                                {'form_errors': form_errors,
                                'captchaform':form,},
                                context_instance = RequestContext(request))
        else:
                form_errors = 'You have entered an incorrect captcha.'
                return render_to_response('feedback/login.html',
                                {'form_errors': form_errors,
                                'captchaform':form,},
                                context_instance = RequestContext(request))
    form = forms.CaptchaTestForm()
    return render_to_response('feedback/login.html',
                            {'captchaform':form,},
                            context_instance = RequestContext(request))

@login_required(login_url="/feedback")
def logout(request):
    """
    logs out user, only if he is already logged in.
    """
    auth.logout(request)
    return HttpResponseRedirect('/feedback',
                                {'form_logout_message': 'You have successfulyy logged out.'})


#------------------------------------------------------------
# Student's dashboard
#------------------------------------------------------------

@login_required(login_url="/feedback/")
def student_home(request):
    """
    Displays the list of courses

    On clicking a course he will be redirected to a detailed
    view '/<course_id>/course' where he can see previous feedbacks
    on the course and 'add new feedback' button.
    """
    try:
        student = request.user.student
    except Student.DoesNotExist:
        raise Http404
    coursestudents = request.user.student.coursestudent_set.all()
    full_name = request.user.username
    return render_to_response('feedback/student/home.html',
                            {'full_name': full_name.capitalize(),
                            'username': request.user.username,
                            'coursestudents': coursestudents,},
                            context_instance = RequestContext(request))


@login_required(login_url="/feedback/")
def student_course_detail(request, course_id):
    """
    Displays information about a particular course.

    User can enter the feedback about the overall course or go to
    feedback forms of individual professors.
    """
    try:
        student = request.user.student
    except Student.DoesNotExist:
        raise Http404
    course = get_object_or_404(Course, id=course_id)
    coursestudent = get_object_or_404(course.coursestudent_set, student = student)

    if(coursestudent.feedback_status):
        return HttpResponseRedirect("/feedback/student/home/")

    coursestudentprofessors = coursestudent.coursestudentprofessor_set.all()

    return render_to_response('feedback/student/course_detail.html',
                            {'course':course,
                            'course_name': course.name.capitalize(),
                            'form': forms.TaskForm(),
                            'coursestudentprofessors': coursestudentprofessors},
                            context_instance=RequestContext(request))


@login_required(login_url="/feedback/")
def student_course_form_submitted(request, course_id):
    """
    Saves the feedback form on the overall course
    """
    try:
        student = request.user.student
    except Student.DoesNotExist:
        raise Http404
    course = get_object_or_404(Course, id=course_id)
    coursestudent = get_object_or_404(course.coursestudent_set, student = student)

    if(coursestudent.feedback_status):
        return HttpResponseRedirect("/feedback/student/home/")

    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.student = student
            task.course = course
            task.coursestudent = coursestudent
            task.save()
            coursestudent.feedback_status = False
            coursestudent.save()
        else:
            return HttpResponse('Not valid')
    return HttpResponseRedirect("/feedback/student/home/")


@login_required(login_url="/feedback/")
def taskprof_detail(request, coursestudentprofessor_id):
    """
    Takes feedback about a particular professor of a course from
    """
    try:
        student = request.user.student
    except Student.DoesNotExist:
        raise Http404
    coursestudentprofessor = get_object_or_404(CourseStudentProfessor, id=coursestudentprofessor_id)
    course = coursestudentprofessor.coursestudent.course
    professor_name = coursestudentprofessor.courseprofessor.professor.user.username

    if(coursestudentprofessor.feedback_status):
        response = "/feedback/"
        response+= str(course.id)
        response+= "/student/course/"
        return HttpResponseRedirect(response)

    return render_to_response('feedback/student/taskprof_detail.html',
                            {'course':course,
                            'professor_name': professor_name.capitalize(),
                            'coursestudentprofessor_id':coursestudentprofessor.id,
                            'form': forms.TaskProfessorForm(),},
                            context_instance=RequestContext(request))

@login_required(login_url="/feedback/")
def taskprof_submitted(request, coursestudentprofessor_id):
    """
    Saves the feedback form on the overall course
    """
    try:
        student = request.user.student
    except Student.DoesNotExist:
        raise Http404
    coursestudentprofessor = get_object_or_404(CourseStudentProfessor, id=coursestudentprofessor_id)
    course = coursestudentprofessor.coursestudent.course

    if(coursestudentprofessor.feedback_status):
        response = "/feedback/"
        response+= course.id
        response+= "/student/course/"
        return HttpResponseRedirect(response)

    if request.method == 'POST':
        form = forms.TaskProfessorForm(request.POST)
        if form.is_valid():
            taskprof = form.save(commit=False)
            taskprof.courseprofessor = coursestudentprofessor.courseprofessor
            taskprof.coursestudent = coursestudentprofessor.coursestudent
            taskprof.coursestudentprofessor = coursestudentprofessor
            taskprof.save()
            coursestudentprofessor.feedback_status = False
            coursestudentprofessor.save()
        else:
            return HttpResponse('Not valid')
            
    response = "/feedback/"
    response+= str(course.id)
    response+= "/student/course/"
    return HttpResponseRedirect(response)


#------------------------------------------------------------
# Professor's dashboard
#------------------------------------------------------------

@login_required(login_url="/feedback/")
def prof_home(request):
    """
    Displays the list of courses the professor is enrolled in

    On clicking a course he will be redirected to a detailed
    view '/<course_id>/course' where he can see previous feedbacks
    on the course and 'add new feedback' button.
    """
    try:
        professor = request.user.professor
    except Professor.DoesNotExist:
        raise Http404
    courses = professor.course_set.all()
    full_name = request.user.username
    return render_to_response('feedback/prof/home.html',
                            {'full_name': full_name.capitalize(),
                            'username': request.user.username,
                            'courses': courses,},
                            context_instance = RequestContext(request))

@login_required(login_url="/feedback/")
def prof_course_detail(request, course_id):
    """
    Displays information about a particular course.

    User can enter the feedback about the overall course or go to
    feedback forms of individual professors.
    """
    try:
        professor = request.user.professor
    except Professor.DoesNotExist:
        raise Http404
    course = get_object_or_404(professor.course_set, id=course_id)
    coursestudents = course.coursestudent_set.all()

    renderer = highcharts
    data =  [
            ['', 'Rating on Overall Course', 'Content of the Course', 'Text materials appropriate'],
            ['Course', 3.9, 4.5, 2.8],
            ['Professor', 2.9, 3.1, 4.5],
        ]

    Chart = renderer.BarChart(SimpleDataSource(data=data), options={'title': "Feedback Statistics"}, html_id="bar_chart")

    tasks = []
    for coursestudent in coursestudents:
        if coursestudent.task_set.first() is not None:
            tasks.append(coursestudent.task_set.first())
    return render_to_response('feedback/prof/course_detail.html',
                            {'tasks':tasks,
                            'chart':Chart,
                            'course_name':course.name.capitalize(),},
                            context_instance=RequestContext(request))

@login_required(login_url="/feedback/")
def prof_task_detail(request, task_id):
    """
    Displays a particular feedback(task) to the professor
    """
    try:
        professor = request.user.professor
    except Professor.DoesNotExist:
        raise Http404
    task = get_object_or_404(Task, id=task_id)
    return render_to_response('feedback/prof/task_detail.html',
                            {'task':task,
                            'course_name':task.course.name.capitalize(),},
                            context_instance=RequestContext(request))


def highcharts_demo(request):
    renderer = highcharts
    data =  [
            ['', 'Rating on Overall Course', 'Content of the Course', 'Text materials appropriate'],
            ['Course', 3.9, 4.5, 2.8],
            ['Professor', 2.9, 3.1, 4.5],
        ]
    Chart = renderer.BarChart(SimpleDataSource(data=data), options={'title': "Feedback Statistics"}, html_id="bar_chart")
    return render_to_response('feedback/prof/highcharts.html',
                            {'chart': Chart,},
                            context_instance=RequestContext(request))

# class HighChartsDemo(Demo):
#     template_name = "feedback/prof/highcharts.html"

# highcharts_demo = HighChartsDemo.as_view(renderer=highcharts)