from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'last_name', 'invite_code', 'activated_invite_code')
    list_filter = ('id', 'phone', 'activated_invite_code')
    search_fields = ('id', 'phone', 'name', 'last_name', 'activated_invite_code')
