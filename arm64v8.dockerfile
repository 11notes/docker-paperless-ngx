# :: QEMU
  FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu

# :: Header
  FROM --platform=linux/arm64 paperlessngx/paperless-ngx:2.11
  COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin

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