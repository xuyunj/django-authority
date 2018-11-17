Configuration
-------------

We need to hook ``django-authority`` into our project.

1. Put ``authority`` into your ``INSTALLED_APPS`` at settings module::

      INSTALLED_APPS = (
         ...
         'authority',
      )

2. Add extra authorization backend to your `settings.py`::

      AUTHENTICATION_BACKENDS = (
          'django.contrib.auth.backends.ModelBackend', # default
          'authority.backends.LdapBackend',
      )

3. Configure ``authority`` user model in your `settings.py`::

     AUTH_USER_MODEL = 'authority.User'
     
4. Add MENU_SESSION_KEY and PERMISSION_SESSION_KEY to your `settings.py`::

    MENU_SESSION_KEY = '_menu'
    PERMISSION_SESSION_KEY ='_permission'

5. Create ``authority`` database tables by running::

     python manage.py migrate

Usage
-----

After installation we can use object permissions
with Django_.

Lets start really quickly::

1. Add the following lines to your login function::
    
    auth.login(request, user)
    authority.shortcuts.set_user_permissions(request)
    
2. If you need check login and permission you can use the `login_perm_required`::

    from authority.shortcuts import login_perm_required
    @login_perm_required(perm_check=True)
    def index(request):
        pass
