from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^choices/', include('choices.urls')),
    (r'^users/', include('users.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ultimatum.views',
    # index.html is often used as default homepage address
    # and every sub address, e.g. events/index.html
    # TODO: need to update!
    url('^$', 'splash'),
    url(r'^welcome/$', 'welcome'),
    url(r'^home/$', 'home'),
    url(r'^accounts/login/$', 'login'),
    url(r'^accounts/auth/$', 'login'),
    url(r'^accounts/logout/$', 'logout'),
    url(r'^accounts/loggedin/$', 'home', {"message": "Welcome User, you are now logged in."}),
    url(r'^accounts/register/$', 'register_user'),
    url(r'^accounts/register_success/$', 'home', {"message": "Welcome User, your registration was successful."}),
)
