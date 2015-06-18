from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guralps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^guralp/', include('guralp.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^earthquakes/', include('earthquakes.urls'))
)

urlpatterns += staticfiles_urlpatterns()
