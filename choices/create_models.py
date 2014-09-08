import random

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core import mail
from django.forms.fields import Field
from django.utils import timezone

from choices.models import Choice
from users.models import SiteUser

# Populates the test database with users and choices

get_user_model().objects.create_superuser(username="tim", email="timothyaaronlee@gmail.com", password="poo")
get_user_model().objects.create_user(username="john", email="john@johns.co.uk", password="john")
get_user_model().objects.create_user(username="percy", email="percy@percy.co.uk", password="percy")
get_user_model().objects.create_user(username="jane", email="jane@jane.co.uk", password="jane")
get_user_model().objects.create_user(username="mike", email="mike@mike.co.uk", password="mike")
get_user_model().objects.create_user(username="emily", email="emily@emily.co.uk", password="emily")
get_user_model().objects.create_user(username="lucy", email="lucy@lucy.co.uk", password="lucy")

USERS = list(get_user_model().objects.all())
for user in USERS:
    SiteUser.objects.create(user=user)
    SiteUser.friends = SiteUser.objects.all().exclude(pk=user.siteuser.pk)

SITE_USERS = list(SiteUser.objects.all())

QUESTIONS =['Which one should I choose?', 
            'Should I go out tonight or not?',
            'Blonde or Brunette?', 
            'Cats or dogs?',
            'Pulp Fiction or Reservoir Dogs',
            '10am or 7pm?']

IMAGE_URL = ['rabbit',
             'jessica',
             'angelina',
             'car',
             'beer',
             'cake',
             'waffles',
             'miles',
             'surfing',
             'storyteller']

TIME_LIMIT = [x[0] for x in Choice.TIME_LIMIT_CHOICES]
SHARE_WITH = [x[0] for x in Choice.SHARE_WITH_CHOICES]

for question in QUESTIONS:
    user = random.choice(SITE_USERS)
    Choice.objects.create(question=question,
                          image1='images/uploaded_images/{}.jpg'.format(random.choice(IMAGE_URL)),
                          image2='images/uploaded_images/{}.jpg'.format(random.choice(IMAGE_URL)),
                          time_limit=random.choice(TIME_LIMIT),
                          share_with=random.choice(SHARE_WITH),
                          created_by=user
                          )
    Choice.objects.get(question=question).share_list = user.friends