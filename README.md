# Debian :: paperless-ngx+
Run paperless-ngx based on Debian. Big, heavy, mostly secure and a bit slow 🍟

This image adds Active Directory authentication to paperless-ngx.

## Run
```shell
docker run --name paperless-ngx \
  -e DJANGO_SETTINGS_MODULE="paperless.settings_ldap" \
  -e PAPERLESS_AD_DOMAIN="domain" \
  -e PAPERLESS_AD_AUTH_URL="ldap://127.0.0.1:389" \
  -e PAPERLESS_AD_AUTH_SEARCH_BASE="DC=ad,DC=domain,DC=com" \
  -e PAPERLESS_AD_USER_GROUP_CN="CN=paperless,DC=ad,DC=domain,DC=com" \
  -e PAPERLESS_AD_ADMIN_GROUP_CN="CN=paperless-admins,DC=ad,DC=domain,DC=com" \
  -e PAPERLESS_AD_AUTH_USER="paperless-ldap" \
  -e PAPERLESS_AD_AUTH_PASSWORD="************" \
  -d 11notes/paperless-ngx:[tag]
```

## Environment
| Parameter | Value | Default |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | paperless.settings_ldap |  |
| `PAPERLESS_AD_DOMAIN` | domain (short name, not FQDN!) |  |
| `PAPERLESS_AD_AUTH_URL` | ldap://127.0.0.1:389 |  |
| `PAPERLESS_AD_AUTH_SEARCH_BASE` | DC=ad,DC=domain,DC=com |  |
| `PAPERLESS_AD_USER_GROUP_CN` | members of this group can login (CN=paperless,DC=ad,DC=domain,DC=com) |  |
| `PAPERLESS_AD_ADMIN_GROUP_CN` | members of this group are administrators (CN=paperless-admins,DC=ad,DC=domain,DC=com) |  |
| `PAPERLESS_AD_AUTH_USER` | user with AD read permissions |  |
| `PAPERLESS_AD_AUTH_PASSWORD` | password of user with AD read permissions |  |

## Parent
* [paperlessngx/paperless-ngx](https://hub.docker.com/r/paperlessngx/paperless-ngx)

## Built with
* [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)
* [django-python3-ldap](https://github.com/etianen/django-python3-ldap)

## Tips
* Don't bind to ports < 1024 (requires root), use NAT/reverse proxy
* [Permanent Stroage](https://github.com/11notes/alpine-docker-netshare) - Module to store permanent container data via NFS/CIFS and more