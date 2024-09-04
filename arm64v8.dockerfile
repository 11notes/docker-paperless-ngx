# :: Header
FROM --platform=linux/arm64 paperlessngx/paperless-ngx:2.11

# :: Run
  USER root

  # :: update image
    RUN set -ex; \
      apt update -y; \
      apt upgrade -y; \
      pip install --upgrade pip;

  # :: copy root filesystem changes
    COPY ./rootfs /

  # :: install ldap
    RUN set -ex; \
      cd /usr/src/paperless/src; \
      pip install django_python3_ldap;