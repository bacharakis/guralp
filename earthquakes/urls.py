from django.conf.urls import patterns, url

from earthquakes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^stations$', views.stations_api, name='stations_api')
    url(r'^events$', views.events_api, name='events_api')


)
