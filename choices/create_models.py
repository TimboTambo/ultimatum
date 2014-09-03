import datetime
import random
from choices.models import Choice
from users.models import SiteUser
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core import mail
from django.forms.fields import Field
from django.utils import timezone
from django.conf import settings


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
SITE_USERS = list(SiteUser.objects.all())
QUESTIONS =['Test1?', 'Test2?', 'Test3?', 'Test4?', 'Test5?', 'Test6?']
IMAGE_URL = '/images/uploaded_images/storyteller.jpg'
TIME_LIMIT = [x[0] for x in Choice.TIME_LIMIT_CHOICES]
SHARE_WITH = [x[0] for x in Choice.SHARE_WITH_CHOICES]


for question in QUESTIONS:
    Choice.objects.create(question=question,
                          option1=IMAGE_URL,
                          option2=IMAGE_URL,
                          time_limit=random.choice(TIME_LIMIT),
                          share_with=random.choice(SHARE_WITH),
                          created_by=random.choice(SITE_USERS),
                          )
