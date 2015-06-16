
from earthquakes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),


)
