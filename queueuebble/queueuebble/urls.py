from django.conf.urls import patterns, include, url
from queueuebble.views import hello
from queue import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'queueuebble.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^hello/$', hello),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', views.register, name='register')
)
