# :: Header
FROM paperlessngx/paperless-ngx:1.16.5

# :: Run
  USER root

  # :: copy root filesystem changes and add execution rights to init scripts
    COPY ./rootfs /

# :: Start
  USER docker