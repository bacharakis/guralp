from django.conf.urls import patterns, url

from earthquakes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^guralp$', views.api_calls, name='guralp')


)
