import os
import django_python3_ldap

LDAP_AUTH_URL = [os.getenv('PAPERLESS_AD_AUTH_URL')]
LDAP_AUTH_SEARCH_BASE = os.getenv('PAPERLESS_AD_AUTH_SEARCH_BASE')
LDAP_AUTH_CONNECTION_USERNAME = os.getenv('PAPERLESS_AD_AUTH_USER')
LDAP_AUTH_CONNECTION_PASSWORD = os.getenv('PAPERLESS_AD_AUTH_PASSWORD')
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = os.getenv('PAPERLESS_AD_DOMAIN')
LDAP_AUTH_USER_FIELDS = {
    "username": "userPrincipalName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
LDAP_AUTH_OBJECT_CLASS = "user"
PAPERLESS_AD_USER_GROUP = os.getenv('PAPERLESS_AD_USER_GROUP_CN')
PAPERLESS_AD_ADMIN_GROUP = os.getenv('PAPERLESS_AD_ADMIN_GROUP_CN')

from .settings import *
INSTALLED_APPS.append("django_python3_ldap")
AUTHENTICATION_BACKENDS.insert(2, "django_python3_ldap.auth.LDAPBackend")

def _format_username(username: str):
    if ("@" not in username):
        username = "{username}@{domain}".format(
            username=username,
            domain=os.getenv('PAPERLESS_AD_UPN_DOMAIN')
        )

    return username

LDAP_AUTH_FORMAT_USERNAME = "paperless.settings_ldap.custom_format_username_active_directory"
def custom_format_username_active_directory(model_fields):
    username = model_fields["username"]  
    return _format_username(username)

LDAP_AUTH_FORMAT_SEARCH_FILTERS = "paperless.settings_ldap.custom_format_search_filters"
def custom_format_search_filters(ldap_fields):
    if PAPERLESS_AD_USER_GROUP:
        ldap_fields["memberOf"] = PAPERLESS_AD_USER_GROUP

    if 'userPrincipalName' in ldap_fields.keys():
        ldap_fields['userPrincipalName'] = _format_username(username=ldap_fields['userPrincipalName'])
        

    from django_python3_ldap.utils import format_search_filters
    search_filters = format_search_filters(ldap_fields)

    return search_filters

LDAP_AUTH_SYNC_USER_RELATIONS = "paperless.settings_ldap.custom_sync_user_relations"
def custom_sync_user_relations(user, ldap_attributes, *, connection=None, dn=None):
    is_admin = False

    if 'memberOf' in ldap_attributes and len(ldap_attributes['memberOf']) > 0:
        if PAPERLESS_AD_ADMIN_GROUP and PAPERLESS_AD_ADMIN_GROUP in ldap_attributes['memberOf']:
            is_admin = True

    if user.is_staff != is_admin or user.is_superuser != is_admin:
        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.save()