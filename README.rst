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
