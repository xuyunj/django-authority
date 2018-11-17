import logging
from django.contrib.auth.models import User
from django.conf import settings
import ldap


class LdapBackend(object):
    """
    Base class for implementing an authentication backend which authenticates
    against LDAP and sets Django group membership based on LDAP Organizational
    Unit (OU) membership.
    """
    def authenticate(self, username=None, password=None):
        """
        Attempts to bind the provided username and password to LDAP.

        A successful LDAP bind authenticates the user.
        """
        raise NotImplementedError

    def bind_ldap(self, username, password):
        """
        Implements the specific logic necessary to bind a given username and
        password to the particular LDAP server.

        Override this method for each new variety of LDAP backend.
        """
        raise NotImplementedError

    def get_or_create_user(self, username, password):
        """
        Attempts to get the user from the Django db; failing this, creates a
        django.contrib.auth.models.User from details pulled from the specific
        LDAP backend.

        Override this method for each new variety of LDAP backend.
        """
        raise NotImplementedError

    def get_user(self, user_id):
        """
        Implements the logic to retrieve a specific user from the Django db.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None




