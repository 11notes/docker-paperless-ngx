# :: Header
FROM paperlessngx/paperless-ngx:1.16.5

# :: copy root filesystem changes and add execution rights to init scripts
  COPY ./rootfs /

RUN set -eux \
  pip install django-python3-ldap;