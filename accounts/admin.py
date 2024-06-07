from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("id","full_name", "email","created_at")
    def get_search_fields(self, request):
        return "full_name", "id","email"
admin.site.register(User, UserAdmin)



class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id","from_user", "to_user","status","created_at")

admin.site.register(FriendRequest, FriendRequestAdmin)
