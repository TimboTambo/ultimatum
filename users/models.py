from django.db import models
from django.contrib.auth.models import User


class SiteUser(models.Model):
    user = models.OneToOneField(User)
    #https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
    friends = models.ManyToManyField("self")

    def __unicode__(self):
        return self.user.username