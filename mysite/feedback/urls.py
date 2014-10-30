from django.conf.urls import url

from feedback import views

urlpatterns = [
        url(r'^$', views.login, name='login'),
        url('invalid/$', views.login, name='invalid'),
        url('logout/$', views.logout, name='logout'),
        url('home/$', views.home, name='home'),

        # url(r'^(?P<task_id>\d+)/previous-feedback/$',views.usertask_detail),
        # url('new-feedback/$', views.new_feedback),
        # url('submitted/$', views.new_feedback),
]
