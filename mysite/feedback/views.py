from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from feedback import forms
from feedback.models import Task, Course
from django.contrib.auth.models import Group

#------------------------------------------------------------
#       User Authentication
#------------------------------------------------------------

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
            return HttpResponseRedirect('/feedback/home')

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
#       Student's dashboard
#------------------------------------------------------------


@login_required(login_url="/feedback/")
def home(request):
    """
    Displays the list of courses

    On clicking a course he will be redirected to a detailed
    view '/<course_id>/course' where he can see previous feedbacks
    on the course and 'add new feedback' button.
    """

    course_list=Course.objects.all()
    full_name = request.user.username
    return render_to_response('feedback/home.html',
                            {'full_name': full_name.capitalize(),
                            'username': request.user.username,
                            'courses': course_list,},
                            context_instance = RequestContext(request))