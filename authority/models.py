from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible

        
@python_2_unicode_compatible   
class Permission(models.Model):
    """ Resources that are allowed to be accessed. """
    name = models.CharField(max_length=30, unique=True, verbose_name="Identifie name")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Parent identifie")
    is_menu = models.BooleanField(default=False, verbose_name="Is menu")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="Icon")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Code")
    url = models.CharField(max_length=128, unique=True, null=True, blank=True)
    
    def __str__ (self):
        return self.name
    
    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = verbose_name
        
    @classmethod
    def get_menu_by_request_url(cls, url):
        try:
            return Permission.objects.get(url=url)
        except Permission.DoesNotExist:
            return None
        

python_2_unicode_compatible
class Role(models.Model):
    """Site Role"""
    name = models.CharField(max_length=32, unique=True, verbose_name="Role")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="Permissions".decode('utf-8'))
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = verbose_name
        
        
class User(AbstractUser):
    """Extending the existing User model"""
    roles = models.ManyToManyField("Role", blank=True, verbose_name="Roles".decode('utf-8') )
    
    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = verbose_name
        db_table = 'auth_user'
        
    def get_user_permissions(self):
        permissions = {}
        permission_url_list = []
        permission_menu_dict = {}
        
        user_roles = Role.objects.all() if self.is_superuser else self.roles.all()
        for r in user_roles:  # remove duplication
            for perm in r.permissions.values():  
                if permissions.has_key(perm['id']):
                    continue
                permissions[ perm['id'] ] = perm
        
        for item in permissions.values():
            if item['url']:
                permission_url_list.append(item['url'])
            if not item['is_menu']:
                continue
            item['status'] = False
            permission_menu_dict[ item['id'] ] = item
        
        pop_menu_list = []
        for id, menu in permission_menu_dict.items():
            if menu['parent_id']:
                parent_menu = permission_menu_dict[ menu['parent_id'] ]
                if not parent_menu.has_key('child'):
                    parent_menu['child'] = [ menu ]
                else:
                    parent_menu['child'].append( menu )
                pop_menu_list.append( menu['id'] )
        
        for id in pop_menu_list:
            permission_menu_dict.pop(id)
        return permission_menu_dict, permission_url_list
            
    
    