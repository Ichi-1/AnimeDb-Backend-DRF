from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = CustomUser

    list_filter = ('nickname', 'auth_provider', 'is_active', 'is_staff')
    list_display = (
        'id', 'nickname', 'email',
        'auth_provider', 'is_active', 'is_staff'
    )
    search_fields = ('nickname',)
    ordering = ('-created_at',)

    #   ? fileds displaying on admin single entity detail page
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'auth_provider', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('avatar', 'about')}),
    )

    #   ? fileds displaying on admin creating entity form page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'nickname', 'email', 'password1', 'password2',
                'is_active', 'is_staff'
            )}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
