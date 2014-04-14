from django.conf.urls import patterns, include, url
from queueuebble.views import hello
from queue import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'queueuebble.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^hello/$', hello),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/(?P<username>[\w\.@+-]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w\.@+-]+)/(?P<uid>\d+)$', views.profile_id, name='profile_id')
)

urlpatterns += staticfiles_urlpatterns()
