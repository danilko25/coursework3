from django.contrib import admin
from .models import Subscription, Visit
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "password",
        "is_staff"
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(Subscription)
admin.site.register(Visit)

