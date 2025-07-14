![banner](https://github.com/11notes/defaults/blob/main/static/img/banner.png?raw=true)

# PAPERLESS-NGX
![size](https://img.shields.io/docker/image-size/11notes/paperless-ngx/2.17.1?color=0eb305)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)![version](https://img.shields.io/docker/v/11notes/paperless-ngx/2.17.1?color=eb7a09)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)![pulls](https://img.shields.io/docker/pulls/11notes/paperless-ngx?color=2b75d6)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)[<img src="https://img.shields.io/github/issues/11notes/docker-PAPERLESS-NGX?color=7842f5">](https://github.com/11notes/docker-PAPERLESS-NGX/issues)![5px](https://github.com/11notes/defaults/blob/main/static/img/transparent5x2px.png?raw=true)![swiss_made](https://img.shields.io/badge/Swiss_Made-FFFFFF?labelColor=FF0000&logo=data:image/svg%2bxml;base64,PHN2ZyB2ZXJzaW9uPSIxIiB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDMyIDMyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxyZWN0IHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0idHJhbnNwYXJlbnQiLz4KICA8cGF0aCBkPSJtMTMgNmg2djdoN3Y2aC03djdoLTZ2LTdoLTd2LTZoN3oiIGZpbGw9IiNmZmYiLz4KPC9zdmc+)

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
    image: "11notes/paperless-ngx:2.17.1"
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

* [2.17.1](https://hub.docker.com/r/11notes/paperless-ngx/tags?name=2.17.1)

### There is no latest tag, what am I supposed to do about updates?
It is of my opinion that the ```:latest``` tag is dangerous. Many times, I’ve introduced **breaking** changes to my images. This would have messed up everything for some people. If you don’t want to change the tag to the latest [semver](https://semver.org/), simply use the short versions of [semver](https://semver.org/). Instead of using ```:2.17.1``` you can use ```:2``` or ```:2.17```. Since on each new version these tags are updated to the latest version of the software, using them is identical to using ```:latest``` but at least fixed to a major or minor version.

If you still insist on having the bleeding edge release of this app, simply use the ```:rolling``` tag, but be warned! You will get the latest version of the app instantly, regardless of breaking changes or security issues or what so ever. You do this at your own risk!

# REGISTRIES ☁️
```
docker pull 11notes/paperless-ngx:2.17.1
docker pull ghcr.io/11notes/paperless-ngx:2.17.1
docker pull quay.io/11notes/paperless-ngx:2.17.1
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

# SECURITY VULNERABILITIES REPORT ⚡
| ID | Severity | Risk | Vector | Source |
| --- | --- | --- | --- | --- |
| CVE-2017-17479 | critical | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-17479) |
| CVE-2017-9117 | critical | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-9117) |
| CVE-2019-1010022 | critical | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2019-1010022) |
| CVE-2023-24531 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-24531) |
| CVE-2023-24540 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-24540) |
| CVE-2023-29402 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-29402) |
| CVE-2023-29404 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-29404) |
| CVE-2023-29405 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-29405) |
| CVE-2023-34152 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-34152) |
| CVE-2023-45853 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-45853) |
| CVE-2023-6879 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-6879) |
| CVE-2024-24790 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-24790) |
| CVE-2024-35368 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-35368) |
| CVE-2024-56431 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-56431) |
| CVE-2025-25467 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-25467) |
| CVE-2025-5914 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-5914) |
| CVE-2025-4517 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-4517) |
| CVE-2023-0645 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-0645) |
| CVE-2024-35367 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-35367) |
| CVE-2025-22871 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-22871) |
| CVE-2025-43859 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-43859) |
| CVE-2025-49794 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-49794) |
| CVE-2025-49796 | critical | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-49796) |
| CVE-2014-8166 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2014-8166) |
| CVE-2016-9580 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2016-9580) |
| CVE-2016-9581 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2016-9581) |
| CVE-2017-17973 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-17973) |
| CVE-2017-2814 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-2814) |
| CVE-2017-2818 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-2818) |
| CVE-2017-2820 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-2820) |
| CVE-2017-5563 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-5563) |
| CVE-2018-16375 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2018-16375) |
| CVE-2018-16376 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2018-16376) |
| CVE-2019-1010023 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2019-1010023) |
| CVE-2019-9543 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2019-9543) |
| CVE-2019-9545 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2019-9545) |
| CVE-2021-40633 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2021-40633) |
| CVE-2023-49463 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-49463) |
| CVE-2023-49502 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-49502) |
| CVE-2025-1594 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-1594) |
| CVE-2024-28960 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-28960) |
| CVE-2025-6297 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-6297) |
| CVE-2022-49043 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2022-49043) |
| CVE-2023-31484 | high | low | [CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-31484) |
| CVE-2023-31486 | high | low | [CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-31486) |
| CVE-2023-39323 | high | low | [CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-39323) |
| CVE-2023-49528 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-49528) |
| CVE-2017-11695 | high | low | [CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-11695) |
| CVE-2017-11696 | high | low | [CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-11696) |
| CVE-2017-11697 | high | low | [CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-11697) |
| CVE-2017-11698 | high | low | [CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-11698) |
| CVE-2022-24106 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2022-24106) |
| CVE-2023-29403 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-29403) |
| CVE-2023-50008 | high | low | [CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-50008) |
| CVE-2024-31582 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-31582) |
| CVE-2024-56171 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-56171) |
| CVE-2025-24928 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-24928) |
| CVE-2025-4802 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-4802) |
| CVE-2025-52496 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-52496) |
| CVE-2025-6020 | high | low | [CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-6020) |
| CVE-2025-7424 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-7424) |
| CVE-2025-7425 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-7425) |
| CVE-2011-4116 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2011-4116) |
| CVE-2012-0039 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2012-0039) |
| CVE-2015-3276 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2015-3276) |
| CVE-2016-9113 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2016-9113) |
| CVE-2016-9114 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2016-9114) |
| CVE-2017-16232 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-16232) |
| CVE-2017-17740 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2017-17740) |
| CVE-2018-1000520 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2018-1000520) |
| CVE-2018-20796 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2018-20796) |
| CVE-2018-5709 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2018-5709) |
| CVE-2018-6829 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2018-6829) |
| CVE-2019-9192 | high | low | [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2019-9192) |
| CVE-2021-20311 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2021-20311) |
| CVE-2021-36691 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2021-36691) |
| CVE-2023-25193 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-25193) |
| CVE-2023-2953 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-2953) |
| CVE-2023-35790 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-35790) |
| CVE-2023-39616 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-39616) |
| CVE-2023-43615 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-43615) |
| CVE-2023-44487 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-44487) |
| CVE-2023-45285 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-45285) |
| CVE-2023-45287 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-45287) |
| CVE-2023-45288 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-45288) |
| CVE-2023-52355 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-52355) |
| CVE-2023-52425 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-52425) |
| CVE-2023-6603 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-6603) |
| CVE-2024-23775 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-23775) |
| CVE-2024-24784 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-24784) |
| CVE-2024-24791 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-24791) |
| CVE-2024-25062 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-25062) |
| CVE-2024-25269 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-25269) |
| CVE-2024-26461 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-26461) |
| CVE-2024-28757 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-28757) |
| CVE-2024-29511 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-29511) |
| CVE-2024-31578 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-31578) |
| CVE-2024-34156 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-34156) |
| CVE-2024-34158 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-34158) |
| CVE-2024-34459 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-34459) |
| CVE-2024-6239 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-6239) |
| CVE-2024-8176 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2024-8176) |
| CVE-2025-27113 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-27113) |
| CVE-2025-29070 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-29070) |
| CVE-2025-32414 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-32414) |
| CVE-2025-32415 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-32415) |
| CVE-2025-32873 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-32873) |
| CVE-2025-4138 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-4138) |
| CVE-2025-4330 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-4330) |
| CVE-2025-4435 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-4435) |
| CVE-2025-47287 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-47287) |
| CVE-2025-6021 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-6021) |
| CVE-2025-7345 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-7345) |
| CVE-2023-24539 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-24539) |
| CVE-2023-29400 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-29400) |
| CVE-2025-0725 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-0725) |
| CVE-2025-2176 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-2176) |
| CVE-2025-2177 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-2177) |
| CVE-2025-31344 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-31344) |
| CVE-2023-6605 | high | low | [CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-6605) |
| CVE-2020-23922 | high | low | [CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2020-23922) |
| CVE-2023-48161 | high | low | [CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2023-48161) |
| CVE-2025-5222 | high | low | [CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H) | [nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2025-5222) |

# ElevenNotes™️
This image is provided to you at your own risk. Always make backups before updating an image to a different version. Check the [releases](https://github.com/11notes/docker-paperless-ngx/releases) for breaking changes. If you have any problems with using this image simply raise an [issue](https://github.com/11notes/docker-paperless-ngx/issues), thanks. If you have a question or inputs please create a new [discussion](https://github.com/11notes/docker-paperless-ngx/discussions) instead of an issue. You can find all my other repositories on [github](https://github.com/11notes?tab=repositories).

*created 14.07.2025, 15:32:01 (CET)*