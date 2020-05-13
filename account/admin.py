from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'is_staff')


admin.site.register(User, UserAdmin)
