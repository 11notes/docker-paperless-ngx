import logging
import os
import subprocess
import sys


logger = logging.getLogger(__name__)

__DJANGO_PYTHON3_LDAP = "django_python3_ldap"
__HAS_DJANGO_PYTHON3_LDAP = False


#
# Install LDAP support in the Paperless docker environment
#

try:
    import django_python3_ldap

except ModuleNotFoundError:
    # LDAP module not yet installed
    logger.debug("LDAP module not installed.")

    if os.getenv('PAPERLESS_LDAP_PIP_INSTALL', '').lower() == "true":
        try:
            logger.warning("Attempting automatic installation of LDAP module...")
            subprocess.run([sys.executable, "-m", "pip", "install", __DJANGO_PYTHON3_LDAP], check=True)

        except subprocess.CalledProcessError:
            # Failed to install module
            logger.exception("LDAP module installation failed!")

        else:
            logger.critical("LDAP module was just installed - it will be available from the next Python execution.")
            # sys.exit(1)

    else:
        logger.info("Not attempting to install the LDAP module (env variable not set)")

else:
    logger.debug("LDAP module already installed")
    __HAS_DJANGO_PYTHON3_LDAP = True


#
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

PAPERLESS_LDAP_UID_FORMAT = os.getenv('PAPERLESS_LDAP_UID_FORMAT')
PAPERLESS_LDAP_USER_GROUP = os.getenv('PAPERLESS_LDAP_USER_GROUP_CN')
PAPERLESS_LDAP_ADMIN_GROUP = os.getenv('PAPERLESS_LDAP_ADMIN_GROUP_CN')
PAPERLESS_LDAP_LLDAP_FIX = False



#
# Load the default Paperless settings
#

from .settings import *


if __HAS_DJANGO_PYTHON3_LDAP:
    INSTALLED_APPS.append(__DJANGO_PYTHON3_LDAP)
    AUTHENTICATION_BACKENDS.insert(2, "django_python3_ldap.auth.LDAPBackend")


LDAP_AUTH_SYNC_USER_RELATIONS = "paperless.settings_ldap.custom_sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "paperless.settings_ldap.custom_format_search_filters"
LDAP_AUTH_FORMAT_USERNAME = "paperless.settings_ldap.auth_user"


if __HAS_DJANGO_PYTHON3_LDAP and PAPERLESS_LDAP_LLDAP_FIX:
    # Patch the module search to work with LLDAP
    import ldap3
    from django_python3_ldap.utils import format_search_filter

    def hacked_has_user(self, **kwargs):
        self._connection.search(
            search_base=LDAP_AUTH_SEARCH_BASE,
            search_filter=format_search_filter(kwargs),
            search_scope=ldap3.SUBTREE,
            attributes=['memberOf', ldap3.ALL_ATTRIBUTES],
            get_operational_attributes=True,
            size_limit=1,
        )
        return bool(len(self._connection.response) > 0 and self._connection.response[0].get("attributes"))

    import django_python3_ldap.ldap
    django_python3_ldap.ldap.Connection.has_user = hacked_has_user


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
    return PAPERLESS_LDAP_UID_FORMAT.format(model_fields['username'])