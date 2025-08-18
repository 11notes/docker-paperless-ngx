![banner](https://github.com/11notes/defaults/blob/main/static/img/banner.png?raw=true)

# PAPERLESS-NGX
![size](https://img.shields.io/docker/image-size/11notes/paperless-ngx/2.18.1?color=0eb305)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)![version](https://img.shields.io/docker/v/11notes/paperless-ngx/2.18.1?color=eb7a09)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)![pulls](https://img.shields.io/docker/pulls/11notes/paperless-ngx?color=2b75d6)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)[<img src="https://img.shields.io/github/issues/11notes/docker-PAPERLESS-NGX?color=7842f5">](https://github.com/11notes/docker-PAPERLESS-NGX/issues)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)![swiss_made](https://img.shields.io/badge/Swiss_Made-FFFFFF?labelColor=FF0000&logo=data:image/svg%2bxml;base64,PHN2ZyB2ZXJzaW9uPSIxIiB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDMyIDMyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxyZWN0IHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0idHJhbnNwYXJlbnQiLz4KICA8cGF0aCBkPSJtMTMgNmg2djdoN3Y2aC03djdoLTZ2LTdoLTd2LTZoN3oiIGZpbGw9IiNmZmYiLz4KPC9zdmc+)

Run paperless-ngx rootless by default (no SUID)!

# INTRODUCTION 📢

A community-supported supercharged document management system: scan, index and archive all your documents.

# SYNOPSIS 📖
**What can I do with this?** This image will run paperless-ngx with s6, but rootless.

# UNIQUE VALUE PROPOSITION 💶
**Why should I run this image and not the other image(s) that already exist?** Good question! Because ...

> [!IMPORTANT]
>* ... this image runs [rootless](https://github.com/11notes/RTFM/blob/main/linux/container/image/rootless.md) as 1000:1000
>* ... this image is auto updated to the latest version via CI/CD
>* ... this image has a health check
>* ... this image is automatically scanned for CVEs before and after publishing
>* ... this image is created via a secure and pinned CI/CD process

If you value security, simplicity and optimizations to the extreme, then this image might be for you.

# VOLUMES 📁
* **/usr/src/paperless/consume** - Directory of the documents you want to consume
* **/usr/src/paperless/media/documents/originals** - Directory of the original imported documents
* **/usr/src/paperless/media/documents/archive** - Directory of the processed documents
* **/usr/src/paperless/media/documents/thumbnails** - Directory of the thumbnails of each document
* **/usr/src/paperless/data** - Directory of internal app relevant files and configs
* **/usr/src/paperless/export** - Directory of document exports

# COMPOSE ✂️
```yaml
name: "dms"
services:
  postgres:
    image: "11notes/postgres:16"
    read_only: true
    environment:
      TZ: "Europe/Zurich"
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      # make a full and compressed database backup each day at 03:00
      POSTGRES_BACKUP_SCHEDULE: "0 3 * * *"
    volumes:
      - "postgres.etc:/postgres/etc"
      - "postgres.var:/postgres/var"
      - "postgres.backup:/postgres/backup"
    tmpfs:
      # needed for read-only
      - "/postgres/run:uid=1000,gid=1000"
      - "/postgres/log:uid=1000,gid=1000"
    networks:
      backend:
    restart: "always"

  redis:
    image: "11notes/redis:7.4.0"
    environment:
      REDIS_PASSWORD: ${REDIS_PASSWORD}
      TZ: Europe/Zurich
    volumes:
      - "redis.etc:/redis/etc"
      - "redis.var:/redis/var"
    networks:
      backend:
    restart: always

  paperless-ngx:
    depends_on:
      postgres:
        condition: "service_healthy"
        restart: true
      redis:
        condition: "service_healthy"
        restart: true
    image: "11notes/paperless-ngx:2.18.1"
    environment:
      TZ: "Europe/Zurich"
      PAPERLESS_REDIS: "redis://:${REDIS_PASSWORD}@redis:6379"
      PAPERLESS_DBPASS: ${POSTGRES_PASSWORD}
      PAPERLESS_CONSUMER_POLLING: "60"
      PAPERLESS_CONSUMER_POLLING_DELAY: "30"
      PAPERLESS_CONSUMER_POLLING_RETRY_COUNT: "3"
      PAPERLESS_OCR_SKIP_ARCHIVE_FILE: "never"
      PAPERLESS_CONSUMER_RECURSIVE: "false"
      PAPERLESS_OCR_LANGUAGES: "eng deu"
      PAPERLESS_OCR_LANGUAGE: "deu"
      PAPERLESS_SECRET_KEY: ${PAPERLESS_NGX_SECRET_KEY}
      PAPERLESS_TIME_ZONE: "Europe/Zurich"
      PAPERLESS_URL: "https://${PAPERLESS_NGX_FQDN}"
      # LDAP module for ADDS with UPN as login
      DJANGO_SETTINGS_MODULE: "paperless.settings_ldap"
      PAPERLESS_AD_AUTH_URL: "ldaps://${PAPERLESS_NGX_LDAP_FQDN}:636"
      PAPERLESS_AD_DOMAIN: ${PAPERLESS_NGX_LDAP_FQDN}
      PAPERLESS_AD_UPN_DOMAIN: ${PAPERLESS_NGX_LDAP_UPN}
      PAPERLESS_AD_AUTH_SEARCH_BASE: ${PAPERLESS_NGX_LDAP_SEARCH_CN}
      PAPERLESS_AD_AUTH_USER: ${PAPERLESS_NGX_LDAP_USER}
      PAPERLESS_AD_AUTH_PASSWORD: ${PAPERLESS_NGX_LDAP_PASSWORD}
      PAPERLESS_AD_USER_GROUP_CN: ${PAPERLESS_NGX_LDAP_USERS_CN}
      PAPERLESS_AD_ADMIN_GROUP_CN: ${PAPERLESS_NGX_LDAP_ADMINS_CN}
    volumes:
      - "paperless-ngx.consume:/usr/src/paperless/consume"
      - "paperless-ngx.originals:/usr/src/paperless/media/documents/originals"
      - "paperless-ngx.archive:/usr/src/paperless/media/documents/archive"
      - "paperless-ngx.data:/usr/src/paperless/data"
      - "paperless-ngx.export:/usr/src/paperless/export"
      - "paperless-ngx.thumbnails:/usr/src/paperless/media/documents/thumbnails"
    networks:
      frontend:
      backend:
    ports:
      - "3000:8000/tcp"
    restart: "always"

volumes:
  postgres.etc:
  postgres.var:
  postgres.backup:
  redis.etc:
  redis.var:
  paperless-ngx.consume:
  paperless-ngx.originals:
  paperless-ngx.archive:
  paperless-ngx.data:
  paperless-ngx.export:
  paperless-ngx.thumbnails:  

networks:
  frontend:
  backend:
    internal: true
```

# DEFAULT SETTINGS 🗃️
| Parameter | Value | Description |
| --- | --- | --- |
| `user` | docker | user name |
| `uid` | 1000 | [user identifier](https://en.wikipedia.org/wiki/User_identifier) |
| `gid` | 1000 | [group identifier](https://en.wikipedia.org/wiki/Group_identifier) |
| `home` | /paperless-ngx | home directory of user docker |

# ENVIRONMENT 📝
| Parameter | Value | Default |
| --- | --- | --- |
| `TZ` | [Time Zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) | |
| `DEBUG` | Will activate debug option for container image and app (if available) | |

# MAIN TAGS 🏷️
These are the main tags for the image. There is also a tag for each commit and its shorthand sha256 value.

* [2.18.1](https://hub.docker.com/r/11notes/paperless-ngx/tags?name=2.18.1)

### There is no latest tag, what am I supposed to do about updates?
It is of my opinion that the ```:latest``` tag is dangerous. Many times, I’ve introduced **breaking** changes to my images. This would have messed up everything for some people. If you don’t want to change the tag to the latest [semver](https://semver.org/), simply use the short versions of [semver](https://semver.org/). Instead of using ```:2.18.1``` you can use ```:2``` or ```:2.18```. Since on each new version these tags are updated to the latest version of the software, using them is identical to using ```:latest``` but at least fixed to a major or minor version.

If you still insist on having the bleeding edge release of this app, simply use the ```:rolling``` tag, but be warned! You will get the latest version of the app instantly, regardless of breaking changes or security issues or what so ever. You do this at your own risk!

# REGISTRIES ☁️
```
docker pull 11notes/paperless-ngx:2.18.1
docker pull ghcr.io/11notes/paperless-ngx:2.18.1
docker pull quay.io/11notes/paperless-ngx:2.18.1
```

# SOURCE 💾
* [11notes/paperless-ngx](https://github.com/11notes/docker-PAPERLESS-NGX)

# PARENT IMAGE 🏛️
* [${{ json_readme_parent_image }}](${{ json_readme_parent_url }})

# BUILT WITH 🧰
* [paperless-ngxio/paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)
* [11notes/util](https://github.com/11notes/docker-util)

# GENERAL TIPS 📌
> [!TIP]
>* Use a reverse proxy like Traefik, Nginx, HAproxy to terminate TLS and to protect your endpoints
>* Use Let’s Encrypt DNS-01 challenge to obtain valid SSL certificates for your services

# CAUTION ⚠️
> [!CAUTION]
>* Since this image is rootless, unlike the official one, it will only work with EN, DE, FR, IT and ES. If you need another language for OCR, please fork this image and install the ```tesseract-ocr-{LANGUAGE}``` package that you need. I can't add all the languages to this image by default

# ElevenNotes™️
This image is provided to you at your own risk. Always make backups before updating an image to a different version. Check the [releases](https://github.com/11notes/docker-paperless-ngx/releases) for breaking changes. If you have any problems with using this image simply raise an [issue](https://github.com/11notes/docker-paperless-ngx/issues), thanks. If you have a question or inputs please create a new [discussion](https://github.com/11notes/docker-paperless-ngx/discussions) instead of an issue. You can find all my other repositories on [github](https://github.com/11notes?tab=repositories).

*created 18.08.2025, 07:19:51 (CET)*