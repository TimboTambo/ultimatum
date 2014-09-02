from django.conf.urls import patterns, include, url
import choices


urlpatterns = patterns('choices.views',
    url(r'^create_choice/', 'create_choice'),
    url(r'^submitted/', 'submitted'),
)