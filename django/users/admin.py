from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group


class UserAdmin(BaseUserAdmin):
    print(BaseUserAdmin.fieldsets)
    # 'fieldsets' list is based on BaseUserAdmin.fieldsets, but
    # with irrelevant fields removed for simplicity
    # Fields removed: password, first and last name, email, groups,
    # and user permissions
    fieldsets = (
        (None, {'fields': ('username', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )}))

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
