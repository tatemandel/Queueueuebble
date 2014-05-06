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
        url(r'^profile/(?P<username>[\w\.@+-]+)/(?P<uid>\d+)/$', views.profile_id, name='profile_id'),
        url(r'^search/$', views.search, name='search'),
        url(r'^user/password/reset/$',
            'django.contrib.auth.views.password_reset',
            #views.password_reset,
            {'template_name': 'reg/password_reset_form.html',
                'post_reset_redirect': '/user/password/reset/done/',
                'email_template_name': 'reg/password_email.html'},
            name='user_password_reset'),
        #
        url(r'^user/password/reset/done/',
            'django.contrib.auth.views.password_reset_done',
            {'template_name': 'reg/password_reset_done.html'},
            name='password_reset_done'),
        #'template_name': 'password_reset_done.html'),
        url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            'django.contrib.auth.views.password_reset_confirm',
            #views.password_reset_confirm,
            {'template_name': 'reg/password_reset_confirm.html',
                'post_reset_redirect': 'user/password/done/'},
            name='password_reset_confirm'),
        url(r'^user/password/done/',
            'django.contrib.auth.views.password_reset_complete',
            {'template_name': 'reg/password_reset_complete.html'},
            name='password_done'),
        url(r'^pebble_login/$', views.pebble_login, name='pebble_login'),
        url(r'^pebble_validate/$', views.pebble_validate, name='pebble_validate'),
        url(r'^pebble_get_admin/$', views.pebble_get_admin, name='pebble_admin'),
        url(r'^pebble_get_member/$', views.pebble_get_member, name='pebble_member'),
        url(r'^pebble_get_queue/$', views.pebble_get_queue, name='pebble_queue'),
        )

urlpatterns += staticfiles_urlpatterns()
