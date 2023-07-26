import logging
import os
import subprocess
import sys


logger = logging.getLogger(__name__)


# Edit these settings to match your configuration
#

# The URL of the LDAP server(s).  List multiple servers for high availability ServerPool connection.
LDAP_AUTH_URL = [os.getenv('PAPERLESS_LDAP_AUTH_URL')]

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = os.getenv('PAPERLESS_LDAP_AUTH_SEARCH_BASE')

# The LDAP username and password of a user for querying the LDAP database for user
# details. If None, then the authenticated user will be used for querying, and
# the `ldap_sync_users`, `ldap_clean_users` commands will perform an anonymous query.
LDAP_AUTH_CONNECTION_USERNAME = os.getenv('PAPERLESS_LDAP_AUTH_USER')
LDAP_AUTH_CONNECTION_PASSWORD = os.getenv('PAPERLESS_LDAP_AUTH_PASSWORD')

logger.info("try bind with %s // %s", LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD)

LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = os.getenv('PAPERLESS_LDAP_DOMAIN')
LDAP_AUTH_USER_FIELDS = {
    "username": "userPrincipalName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

LDAP_AUTH_OBJECT_CLASS = "user"

PAPERLESS_LDAP_UID_FORMAT = os.getenv('PAPERLESS_LDAP_UID_FORMAT')
PAPERLESS_LDAP_USER_GROUP = os.getenv('PAPERLESS_LDAP_USER_GROUP_CN')
PAPERLESS_LDAP_ADMIN_GROUP = os.getenv('PAPERLESS_LDAP_ADMIN_GROUP_CN')

#
# Load the default Paperless settings
#

from .settings import *


INSTALLED_APPS.append("django_python3_ldap")
AUTHENTICATION_BACKENDS.insert(2, "django_python3_ldap.auth.LDAPBackend")


def custom_sync_user_relations(user, ldap_attributes, *, connection=None, dn=None):
    is_admin = False

    if 'memberOf' in ldap_attributes and len(ldap_attributes['memberOf']) > 0:
        if PAPERLESS_LDAP_ADMIN_GROUP and PAPERLESS_LDAP_ADMIN_GROUP in ldap_attributes['memberOf']:
            is_admin = True

    if user.is_staff != is_admin or user.is_superuser != is_admin:
        logger.warning("LDAP admin level mismatch for %s! Setting admin = %s", ldap_attributes['uid'][0], is_admin)
        user.is_staff = is_admin
        user.is_superuser = is_admin

        user.save()


def custom_format_search_filters(ldap_fields):
    # Ensure the user is a member of the Paperless LDAP group, if specified
    if PAPERLESS_LDAP_USER_GROUP:
        ldap_fields["memberOf"] = PAPERLESS_LDAP_USER_GROUP

    # Call the base format callable.
    from django_python3_ldap.utils import format_search_filters
    search_filters = format_search_filters(ldap_fields)

    return search_filters


def auth_user(model_fields):
    logger.info("LDAP searching for user %s", model_fields['username'])
    return PAPERLESS_LDAP_UID_FORMAT.format(model_fields['username'])