from django.db import models
from django.utils import timezone

from users.models import SiteUser
# Create your models here.


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(expired=False)

class ExpiredManager(models.Manager):
    def get_query_set(self):
        return super(ExpiredManager, self).get_query_set().filter(expired=True)

class Choice(models.Model):
    
    TIME_LIMIT_CHOICES = (
    (10, '10 minutes'),
    (30, '30 minutes'),
    (60, '1 hour'),
    (360, '6 hours'))

    SHARE_WITH_CHOICES = (
    ('some', 'Select few'),
    ('all', 'All friends'),
    ('public', 'Public')) 

    question = models.CharField(max_length=300, blank=False)
    image1 = models.ImageField(blank=True, upload_to="images/uploaded_images/")
    image2 = models.ImageField(blank=True, upload_to="images/uploaded_images/")
    text1 = models.TextField(max_length=200, blank=True)
    text2 = models.TextField(max_length=200, blank=True)
    url1 = models.URLField(max_length=200, blank=True)
    url2 = models.URLField(max_length=200, blank=True)
    time_created = models.DateTimeField(default=timezone.now())
    time_limit = models.IntegerField(choices=TIME_LIMIT_CHOICES, default=60)
    share_with = models.CharField(max_length=200, choices=SHARE_WITH_CHOICES, default='all')
    # info on related_name: http://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    share_list = models.ManyToManyField(SiteUser, related_name="choice_shared_list", blank=True)
    voted_1 = models.ManyToManyField(SiteUser, related_name="choice_voted_1")
    voted_2 = models.ManyToManyField(SiteUser, related_name="choice_voted_2")
    created_by = models.ForeignKey(SiteUser, related_name="creator")

    objects = models.Manager() # default Manager
    active_set = ActiveManager()
    expired_set = ExpiredManager()

    @property
    def time_remaining(self):
        time_delta_since_created = timezone.now() - self.time_created
        time_delta_in_mins = time_delta_since_created.seconds/60
        return self.time_limit - time_delta_in_mins

    @property
    def time_remaining_str(self):
        time_delta_since_created = timezone.now() - self.time_created
        time_delta_in_mins = time_delta_since_created.seconds/60
        time_remaining = self.time_limit - time_delta_in_mins
        if time_remaining > 120:
            return "{} hours {} minutes".format(str(time_remaining // 60), str(time_remaining % 60))
        elif time_remaining > 60:
            return "{} hour {} minutes".format(str(time_remaining // 60), (time_remaining % 60))
        else:
            return "{} minutes".format(str(time_remaining))


    @property
    def expired(self):
        if self.time_remaining < 0:
            return True
        return False

    class Meta:
        ordering = ('time_created',)

    def __unicode__(self):
        return self.question
 

class Comment(models.Model):
    user = models.ForeignKey(SiteUser)
    choice = models.ForeignKey(Choice)
    content = models.TextField(max_length=200)
    time_created = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        if len(self.content) > 10:
            return self.content[:10]
        return  self.content