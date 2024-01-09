# Debian :: paperless-ngx LDAP
![size](https://img.shields.io/docker/image-size/11notes/paperless-ngx/2.3.2?color=0eb305) ![version](https://img.shields.io/docker/v/11notes/paperless-ngx?color=eb7a09) ![pulls](https://img.shields.io/docker/pulls/11notes/paperless-ngx?color=2b75d6) ![activity](https://img.shields.io/github/commit-activity/m/11notes/docker-paperless-ngx?color=c91cb8) ![commit-last](https://img.shields.io/github/last-commit/11notes/docker-paperless-ngx?color=c91cb8)

Run paperless-ngx based on Debian. Big, heavy, mostly secure and a bit slow 🍟

This image adds Active Directory authentication to paperless-ngx (UPN only!)

## Run
```shell
docker run --name paperless-ngx \
  -e DJANGO_SETTINGS_MODULE="paperless.settings_ldap" \
  -e PAPERLESS_AD_DOMAIN="ad.domain.com" \
  -e PAPERLESS_AD_UPN_DOMAIN="domain.com" \
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
| `PAPERLESS_AD_DOMAIN` | domain (FQDN) |  |
| `PAPERLESS_AD_UPN_DOMAIN` | the FQDN of the domain for UPN login if the user forgets it |  |
| `PAPERLESS_AD_AUTH_URL` | ldap://127.0.0.1:389 |  |
| `PAPERLESS_AD_AUTH_SEARCH_BASE` | DC=ad,DC=domain,DC=com |  |
| `PAPERLESS_AD_USER_GROUP_CN` | members of this group can login (CN=paperless,DC=ad,DC=domain,DC=com) |  |
| `PAPERLESS_AD_ADMIN_GROUP_CN` | members of this group are administrators (CN=paperless-admins,DC=ad,DC=domain,DC=com) |  |
| `PAPERLESS_AD_AUTH_USER` | user with AD read permissions |  |
| `PAPERLESS_AD_AUTH_PASSWORD` | password of user with AD read permissions |  |

## Parent Image
* [paperlessngx/paperless-ngx](https://hub.docker.com/r/paperlessngx/paperless-ngx)

## Built with and thanks to
* [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)
* [django-python3-ldap](https://github.com/etianen/django-python3-ldap)

## Tips
* Only use rootless container runtime (podman, rootless docker)
* Don't bind to ports < 1024 (requires root), use NAT/reverse proxy (haproxy, traefik, nginx)