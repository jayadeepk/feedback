from django.conf.urls import url

from feedback import views

urlpatterns = [
        url(r'^$', views.login, name='login'),
        url('logout/$', views.logout, name='logout'),
        
        url('student/home/$', views.student_home, name='student_home'),
        url(r'^(?P<course_id>\d+)/student/course/$',views.student_course_detail),
        url(r'^(?P<course_id>\d+)/student/submitted/$',views.student_course_form_submitted),

        url('prof/home/$', views.prof_home, name='prof_home'),
        url(r'^(?P<course_id>\d+)/prof/course/$',views.prof_course_detail),
        url(r'^(?P<task_id>\d+)/prof/feedback/$',views.prof_task_detail),
]
