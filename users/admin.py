from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users.models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    def designation(obj):
        return obj.get_profile().designation

    inlines = [ UserProfileInline, ]
    list_display = (designation, 'username', 'first_name', 'last_name',
                    'email', 'is_staff',)
    list_display_links = ('username',)

admin.site.register(User, UserProfileAdmin)
