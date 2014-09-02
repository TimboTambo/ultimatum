from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import timezone
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

    SHARE_WITH_CHOICE = (
        ('some', 'Select few'),
        ('all', 'All friends'),
        ) 

    share_with = models.CharField(max_length=200, choices=SHARE_WITH_CHOICE, default='all')

    @property
    def time_remaining(self):
        time_since_created = timezone.now() - self.time_created
        return self.time_limit - time_since_created

    @property
    def expired(self):
        if time_remaining < 0:
            return True
        return False

    created_by = models.ForeignKey(User)

    class Meta:
        ordering = ('time_created',)


    def __unicode__(self):
        return self.created_by.username

