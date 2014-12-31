from django.conf.urls import patterns, url

from guralp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<guralpre>\w+)/$', views.detail, name='detail'),

)
