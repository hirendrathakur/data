from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'feedback.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^feedback/', include('feedback.urls', namespace="feedback")),
    #url(r'^(?P<key>\w+)/$','feedback.views.index2', name='index2'),
    #url(r'^my/', 'feedback.views.my_view', name='my'),
    url(r'^login/', 'feedback.views.Login', name='login'),
    url(r'^getmail/', 'feedback.views.getmail', name='getmail'),
    url(r'^logout/', 'feedback.views.Logout', name='logout'),
    url(r'^register/', 'feedback.views.register', name='register'),
    url(r'^success/', 'feedback.views.success', name='success'),
    url(r'^unsuccess/', 'feedback.views.unsuccess', name='unsuccess'),
    #url(r'^analyse/', 'feedback.views.analyse', name='analyse'),
    url(r'^admin/', include(admin.site.urls)),
)
