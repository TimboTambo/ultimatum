from django.db import models
from django.contrib.auth.models import User


class SiteUser(models.Model):
    user = models.OneToOneField(User)
    #https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
    friends = models.ManyToManyField("self")
    viewed_current = models.ManyToManyField('choices.Choice', blank=True, related_name='user_viewed_current')
    viewed_results = models.ManyToManyField('choices.Choice', blank=True, related_name='user_viewed_results')

    def __unicode__(self):
        return self.user.username