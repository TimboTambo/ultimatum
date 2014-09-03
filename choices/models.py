from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import timezone

from users.models import SiteUser
# Create your models here.


class Choice(models.Model):
    question = models.CharField(max_length=300, blank=False)
    option1 = models.ImageField(blank=False, upload_to="images/uploaded_images/")
    option2 = models.ImageField(blank=False, upload_to="images/uploaded_images/")
    time_created = models.DateTimeField(default=timezone.now())

    TIME_LIMIT_CHOICES = (
        (10, '10 minutes'),
        (30, '30 minutes'),
        (60, '1 hour'),
        (3600, '6 hours'),
        )

    time_limit = models.IntegerField(choices=TIME_LIMIT_CHOICES, default=60)

    SHARE_WITH_CHOICES = (
        ('some', 'Select few'),
        ('all', 'All friends'),
        ) 

    share_with = models.CharField(max_length=200, choices=SHARE_WITH_CHOICES, default='all')
    # info on related_name: http://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    share_list = models.ManyToManyField(SiteUser, related_name="choice_shared_list")
    voted_1 = models.ManyToManyField(SiteUser, related_name="choice_voted_1")
    voted_2 = models.ManyToManyField(SiteUser, related_name="choice_voted_2")

    @property
    def time_remaining(self):
        time_delta_since_created = timezone.now() - self.time_created
        time_delta_in_mins = time_delta_since_created.seconds/60
        return self.time_limit - time_delta_in_mins

    @property
    def expired(self):
        if self.time_remaining < 0:
            return True
        return False

    created_by = models.ForeignKey(SiteUser, related_name="creator")

    class Meta:
        ordering = ('time_created',)

    def __unicode__(self):
        return self.question

