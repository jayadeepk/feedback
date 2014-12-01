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
from feedback.models import Task, Course
from django.contrib.auth.models import Group


#----------------------------------------------------------------
# User Authentication
#----------------------------------------------------------------

def login(request):
    """
    Authenticates user from the username and password from POST
    """
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Since the user is authenticated, Log the user in.
            auth.login(request, user)
            if user.groups.filter(name='Professors'):
                return HttpResponseRedirect('/feedback/prof/home/')
            elif user.groups.filter(name='Students'):
                return HttpResponseRedirect('/feedback/student/home/')
            else:
                return HttpResponse('You are not registered as a student or a Professor.',
                                    'Please contact netadmin.')

        else:
            # Return an 'invalid login' error message.
            form_errors = True
            return render_to_response('feedback/login.html', {'form_errors': form_errors},
                            context_instance = RequestContext(request))
    
    return render_to_response('feedback/login.html',
                            context_instance = RequestContext(request))

@login_required(login_url="/feedback")
def logout(request):
    """
    logs out user, only if he is already logged in.
    """
    auth.logout(request)
    return HttpResponseRedirect('/feedback')


#------------------------------------------------------------
# Student's dashboard
#------------------------------------------------------------

@login_required(login_url="/feedback/")
@user_passes_test(lambda u: u.has_perm('feedback.can_access_student_views'))
def student_home(request):
    """
    Displays the list of courses

    On clicking a course he will be redirected to a detailed
    view '/<course_id>/course' where he can see previous feedbacks
    on the course and 'add new feedback' button.
    """
    user = request.user
    courseuser_list = user.courseuser_set.all()
    full_name = request.user.username
    return render_to_response('feedback/student/home.html',
                            {'full_name': full_name.capitalize(),
                            'username': request.user.username,
                            'courseusers': courseuser_list,},
                            context_instance = RequestContext(request))


@login_required(login_url="/feedback/")
@user_passes_test(lambda u: u.has_perm('feedback.can_access_student_views'))
def student_course_detail(request, course_id):
    """
    Displays information about a particular course.

    User can enter the feedback about the overall course or go to
    feedback forms of individual professors.
    """
    course = get_object_or_404(Course, id=course_id)
    courseuser = get_object_or_404(course.courseuser_set, user = request.user)

    if(courseuser.feedback_status):
        return HttpResponseRedirect("/feedback/student/home/")

    return render_to_response('feedback/student/course_detail.html',
                            {'course':course,
                            'course_name':course.name.capitalize(),
                            'course_form':forms.CourseTaskForm()},
                            context_instance=RequestContext(request))


@login_required(login_url="/feedback/")
@user_passes_test(lambda u: u.has_perm('feedback.can_access_student_views'))
def student_course_form_submitted(request, course_id):
    """
    Saves the feedback form on the overall course
    """
    course = get_object_or_404(Course, id=course_id)
    courseuser = get_object_or_404(course.courseuser_set, user = request.user)

    if(courseuser.feedback_status):
        return HttpResponseRedirect("/feedback/student/home/")

    if request.method == 'POST':
        form = forms.CourseTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.student = request.user
            task.course = course
            task.courseuser = courseuser
            task.save()
            courseuser.feedback_status = True
            courseuser.save()

    return HttpResponseRedirect("/feedback/student/home/")


#------------------------------------------------------------
# Professor's dashboard
#------------------------------------------------------------

@login_required(login_url="/feedback/")
@user_passes_test(lambda u: u.has_perm('feedback.can_access_professor_views'))
def prof_home(request):
    """
    Displays the list of courses the professor is enrolled in

    On clicking a course he will be redirected to a detailed
    view '/<course_id>/course' where he can see previous feedbacks
    on the course and 'add new feedback' button.
    """
    user = request.user
    courseuser_list = user.courseuser_set.all()
    full_name = request.user.username
    return render_to_response('feedback/prof/home.html',
                            {'full_name': full_name.capitalize(),
                            'username': request.user.username,
                            'courseusers': courseuser_list,},
                            context_instance = RequestContext(request))

@login_required(login_url="/feedback/")
@user_passes_test(lambda u: u.has_perm('feedback.can_access_professor_views'))
def prof_course_detail(request, course_id):
    """
    Displays information about a particular course.

    User can enter the feedback about the overall course or go to
    feedback forms of individual professors.
    """
    course = get_object_or_404(Course, id=course_id)
    courseusers = course.courseuser_set.all()
    tasks = []
    for courseuser in courseusers:
        if courseuser.task_set.first() is not None:
            tasks.append(courseuser.task_set.first())
    return render_to_response('feedback/prof/course_detail.html',
                            {'tasks':tasks,
                            'course_name':course.name.capitalize(),},
                            context_instance=RequestContext(request))


@login_required(login_url="/feedback/")
@user_passes_test(lambda u: u.has_perm('feedback.can_access_professor_views'))
def prof_task_detail(request, task_id):
    """
    Displays a particular feedback(task) to the professor
    """
    task = get_object_or_404(Task, id=task_id)
    return render_to_response('feedback/prof/task_detail.html',
                            {'task':task,
                            'course_name':task.course.name.capitalize(),},
                            context_instance=RequestContext(request))