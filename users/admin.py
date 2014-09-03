from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import SiteUser


# Define an inline admin descriptor for SiteUser model
# which acts a bit like a singleton
class SiteUserInline(admin.StackedInline):
    model = SiteUser
    can_delete = False
    verbose_name_plural = 'site_user'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (SiteUserInline, )


class SiteUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SiteUser)