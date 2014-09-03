from django.conf.urls import patterns, include, url
import users


urlpatterns = patterns('users.views',
    url(r'^add_friends/', 'add_friends'),
)