from django.conf.urls import patterns, include, url
import users


urlpatterns = patterns('users.views',
    url(r'^update_friends/', 'update_friends'),
)