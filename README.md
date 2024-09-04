![Banner](https://github.com/11notes/defaults/blob/main/static/img/banner.png?raw=true)

# paperless-ngx
![size](https://img.shields.io/docker/image-size/11notes/paperless-ngx/2.11?color=0eb305) ![version](https://img.shields.io/docker/v/11notes/paperless-ngx/2.11?color=eb7a09) ![pulls](https://img.shields.io/docker/pulls/11notes/paperless-ngx?color=2b75d6) ![stars](https://img.shields.io/docker/stars/11notes/paperless-ngx?color=e6a50e) [<img src="https://img.shields.io/badge/github-11notes-blue?logo=github">](https://github.com/11notes)

**Store all your paper documents protected by Active Directory as IdP**

# SYNOPSIS
What can I do with this? This image adds Active Directory authentication to paperless-ngx (UPN only!).

# COMPOSE
```yaml
name: "paperless-ngx"
services:
  redis:
    image: "11notes/redis:7.4.0"
    environment:
      REDIS_PASSWORD: "*****************"
      TZ: Europe/Zurich
    volumes:
      - "redis-etc:/redis/etc"
      - "redis-var:/redis/var"
    networks:
      - backend
    restart: always
  postgres:
    image: "11notes/postgres:16"
    environment:
      POSTGRES_PASSWORD: "*****************"
      TZ: Europe/Zurich
    volumes:
      - "postgres-var:/postgres/var"
    networks:
      - backend
    restart: always
  app:
    image: "11notes/paperless-ngx:2.11"
    environment:
      TZ: "Europe/Zurich"
      PAPERLESS_REDIS: "redis://:*****************@redis:6379"
      PAPERLESS_DBHOST: "postgres"
      PAPERLESS_DBNAME: "postgres"
      PAPERLESS_DBUSER: "postgres"
      PAPERLESS_DBPASS: "*****************"
      USERMAP_UID: "1000"
      USERMAP_GID: "1000"
      PAPERLESS_CONSUMER_POLLING: "60"
      PAPERLESS_CONSUMER_POLLING_DELAY: "30"
      PAPERLESS_CONSUMER_POLLING_RETRY_COUNT: "3"
      PAPERLESS_OCR_SKIP_ARCHIVE_FILE: "never"
      PAPERLESS_CONSUMER_RECURSIVE: "false"
      DJANGO_SETTINGS_MODULE: "paperless.settings_ldap"
      PAPERLESS_AD_AUTH_URL: "ldaps://ad.domain.com:636"
      PAPERLESS_AD_DOMAIN: "ad.domain.com"
      PAPERLESS_AD_UPN_DOMAIN: "domain.com"
      PAPERLESS_AD_AUTH_SEARCH_BASE: "DC=ad,DC=domain,DC=com"
      PAPERLESS_AD_AUTH_USER: "ldap.paperless"
      PAPERLESS_AD_AUTH_PASSWORD: "******************"
      PAPERLESS_AD_USER_GROUP_CN: "CN=Users,OU=paperless-ngx,OU=Services,OU=Groups,OU=Domain,DC=ad,DC=domain,DC=com"
      PAPERLESS_AD_ADMIN_GROUP_CN: "CN=Administrators,OU=paperless-ngx,OU=Services,OU=Groups,OU=Domain,DC=ad,DC=domain,DC=com"
      PAPERLESS_OCR_LANGUAGES: "eng deu"
      PAPERLESS_OCR_LANGUAGE: "deu"
      PAPERLESS_SECRET_KEY: "****************************************"
      PAPERLESS_TIME_ZONE: "Europe/Zurich"
      PAPERLESS_URL: "https://paperless.domain.com"
    depends_on:
      redis:
        condition: service_healthy
        restart: true
      postgres:
        condition: service_healthy
        restart: true
    volumes:
      - "consume:/usr/src/paperless/consume"
      - "originals:/usr/src/paperless/media/documents/originals"
      - "archive:/usr/src/paperless/media/documents/archive"
      - "paperless-data:/usr/src/paperless/data"
      - "paperless-export:/usr/src/paperless/export"
      - "paperless-thumbnails:/usr/src/paperless/media/documents/thumbnails"
    ports:
      - 8000:8000/tcp
    networks:
      - backend
      - frontend
    restart: always
volumes:
  redis-etc:
  redis-var:
  postgres-var:
  paperless-data:
  paperless-export:
  paperless-thumbnails:
  consume:
    driver_opts:
      type: cifs
      o: username=service.paperless,password=*****************,domain=DOMAIN,uid=1000,gid=1000,dir_mode=0700,file_mode=0700
      device: //dfs/domain.com/paperless-ngx/scanner
  originals:
    driver_opts:
      type: cifs
      o: username=service.paperless,password=*****************,domain=DOMAIN,uid=1000,gid=1000,dir_mode=0700,file_mode=0700
      device: //dfs/domain.com/paperless-ngx/originals
  archive:
    driver_opts:
      type: cifs
      o: username=service.paperless,password=*****************,domain=DOMAIN,uid=1000,gid=1000,dir_mode=0700,file_mode=0700
      device: //dfs/domain.com/paperless-ngx
networks:
  backend:
    internal: true
  frontend:
```

# DEFAULT SETTINGS
| Parameter | Value | Description |
| --- | --- | --- |
| `user` | docker | user docker |
| `uid` | 1000 | user id 1000 |
| `gid` | 1000 | group id 1000 |
| `home` | /usr/src/paperless | home directory of user docker |

# ENVIRONMENT
| Parameter | Value | Default |
| --- | --- | --- |
| `TZ` | [Time Zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) | |
| `DEBUG` | Show debug information | |
| `DJANGO_SETTINGS_MODULE` | paperless.settings_ldap |  |
| `PAPERLESS_AD_DOMAIN` | domain (FQDN) |  |
| `PAPERLESS_AD_UPN_DOMAIN` | the FQDN of the domain for UPN login if the user forgets it |  |
| `PAPERLESS_AD_AUTH_URL` | ldaps://127.0.0.1:636 |  |
| `PAPERLESS_AD_AUTH_SEARCH_BASE` | DC=ad,DC=domain,DC=com |  |
| `PAPERLESS_AD_USER_GROUP_CN` | members of this group can login (CN=paperless,DC=ad,DC=domain,DC=com) |  |
| `PAPERLESS_AD_ADMIN_GROUP_CN` | members of this group are administrators (CN=paperless-admins,DC=ad,DC=domain,DC=com) |  |
| `PAPERLESS_AD_AUTH_USER` | user with AD read permissions |  |
| `PAPERLESS_AD_AUTH_PASSWORD` | password of user with AD read permissions |  |

# SOURCE
* [11notes/paperless-ngx](https://github.com/11notes/docker-paperless-ngx)

# PARENT IMAGE
* [paperlessngx/paperless-ngx:2.11](https://hub.docker.com/r/paperlessngx/paperless-ngx)

# BUILT WITH
* [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)
* [django-python3-ldap](https://github.com/etianen/django-python3-ldap)

# TIPS
* Use a reverse proxy like Traefik, Nginx to terminate TLS with a valid certificate
* Use Let’s Encrypt certificates to protect your SSL endpoints

# ElevenNotes<sup>™️</sup>
This image is provided to you at your own risk. Always make backups before updating an image to a new version. Check the changelog for breaking changes. You can find all my repositories on [github](https://github.com/11notes).
    