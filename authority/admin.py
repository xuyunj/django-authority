from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import User,Role,Permission


class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)
    
    
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_menu', 'icon', 'code', 'url' ]
    

class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        
        self.fieldsets = (
            (None, {'fields': ('username', 'password')}),
            (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions', 'roles')}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    
        self.list_display = ('username', 'is_superuser', 'email', 'is_staff', 'show_roles', )
        self.filter_horizontal = ('groups', 'user_permissions', 'roles', )
        
        
    def show_roles(self, obj):
        role_list = []
        for role in obj.roles.all():
            role_list.append(role.name)
        return ','.join(role_list)
    show_roles.short_description = 'roles'
        
admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
