# :: Header
FROM paperlessngx/paperless-ngx:1.16.5

# :: copy root filesystem changes and add execution rights to init scripts
  COPY ./rootfs /

WORKDIR /usr/src/paperless/src/paperless
RUN set -ex \
  pip install --upgrade pip \
  pip install django-python3-ldap;