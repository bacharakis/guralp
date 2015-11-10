from django.conf.urls import patterns, url

from earthquakes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^stations$', views.stations_api, name='stations_api'),
    url(r'^events$', views.events_api, name='events_api'),
    url(r'^plot$', views.plotting_files, name='plotting_files'),
    url(r'^plot_station$', views.plotting_station_files, name='plotting_station_files'),
    #url(r'^get_files$', views.get_files_json, name='get_files_json'),
    url(r'^download$', views.download_files),
    url(r'^chart.html', views.chart),


)
