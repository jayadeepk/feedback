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
    form_errors = None
    if request.POST:
        form = forms.CaptchaTestForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            if user is not None:
                # Check whether user is student or professor
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
                    auth.logout(request)
                    form_errors = 'You are not registered as student or professor'

            else:
                # Return an 'invalid login' error message.
                form_errors = 'The username or password did not match with our records.'
        else:
                form_errors = 'You have entered an incorrect captcha.'
                return render_to_response('feedback/login.html',
                                {'form_errors': form_errors,
                                'captchaform':form,},
                                context_instance = RequestContext(request))
    form = forms.CaptchaTestForm()
    return render_to_response('feedback/login.html',
                            {'form_errors': form_errors,
                            'captchaform':form,},
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
    courseprofessor = course.courseprofessor_set.filter(professor=professor)


    course_rating1_average = 0.0
    course_rating2_average = 0.0
    course_rating3_average = 0.0
    professor_rating1_average = 0.0
    professor_rating2_average = 0.0
    professor_rating3_average = 0.0

    # Calculate average of all the ratings on the course
    tasks = []
    for coursestudent in coursestudents:
        if coursestudent.task_set.first() is not None:
            course_rating1_average += coursestudent.task_set.first().rating1
            course_rating2_average += coursestudent.task_set.first().rating2
            course_rating3_average += coursestudent.task_set.first().rating3
            tasks.append(coursestudent.task_set.first())
    number_of_tasks = len(tasks)
    if len(tasks) is not 0:
        course_rating1_average /= len(tasks)
        course_rating1_average += 1
        course_rating2_average /= len(tasks)
        course_rating2_average += 1
        course_rating3_average /= len(tasks)
        course_rating3_average += 1

    # Calculate average of all the ratings on the professor
    taskprofessors = []
    for coursestudent in coursestudents:
        taskprofessor = coursestudent.coursestudentprofessor_set.get(courseprofessor=courseprofessor).taskprofessor_set.first()
        if taskprofessor is not None:
            professor_rating1_average += taskprofessor.rating1
            professor_rating2_average += taskprofessor.rating2
            professor_rating3_average += taskprofessor.rating3
            taskprofessors.append(taskprofessor)
    number_of_taskprofessors = len(tasks)
    if len(taskprofessors) is not 0:
        professor_rating1_average /= len(taskprofessors)
        professor_rating1_average += 1
        professor_rating2_average /= len(taskprofessors)
        professor_rating2_average += 1
        professor_rating3_average /= len(taskprofessors)
        professor_rating3_average += 1

    renderer = highcharts
    data =  [
            ['', 'Overall Course', 'Content of the Course', 'Text materials appropriate'],
            ['Course Rating', course_rating1_average, course_rating2_average, course_rating3_average],
            ['Professor Rating', professor_rating1_average, professor_rating2_average, professor_rating3_average],
        ]

    Chart = renderer.BarChart(SimpleDataSource(data=data), options={'title': "Feedback Statistics"}, html_id="bar_chart")

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