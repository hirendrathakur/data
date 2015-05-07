__author__ = 'HIRENDRA'

from django.conf.urls import patterns, url

from feedback import views

urlpatterns = patterns('',
                       url(r'^$',views.index, name='index'),
                       url(r'^(.*)/$',views.index2, name='index2'),
                       url(r'^getmail/$',views.getmail, name='getmail'),
                       url(r'^(?P<prof_pk>\d+)/(?P<stud_roll>\w+)/(?P<sub_pk>\d+)/$',views.polls2, name='polls2'),
                       url(r'^analyse/$',views.analyse, name='analyse'),
                       url(r'^analyse/(?P<prof_pk>\d+)/$',views.courseanalyse, name='courseanalyse'),
                        )