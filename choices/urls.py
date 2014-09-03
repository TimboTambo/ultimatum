from django.conf.urls import patterns, include, url
import choices


urlpatterns = patterns('choices.views',
    url(r'^create_choice/', 'create_choice'),
    url(r'^submitted/', 'submitted'),
    url(r'^view_ultimatums/', 'view_ultimatums'),
    url(r'^view_ultimatum/(?P<id>[0-9]+)', 'view_ultimatum'),
)