from django.conf.urls import url

from feedback import views

urlpatterns = [
        url(r'^$', views.login, name='login'),
        url('invalid/$', views.login, name='invalid'),
        url('logout/$', views.logout, name='logout'),
        url('home/$', views.home, name='home'),

        url(r'^(?P<course_id>\d+)/course/$',views.course_detail),
        url(r'^(?P<course_id>\d+)/submitted/$',views.course_form_submitted),
]
