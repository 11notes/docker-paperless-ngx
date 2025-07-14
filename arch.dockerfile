# ╔═════════════════════════════════════════════════════╗
# ║                       SETUP                         ║
# ╚═════════════════════════════════════════════════════╝
  # GLOBAL
  ARG APP_UID=1000 \
      APP_GID=1000 \
      APP_VERSION=2.17.0

  # :: FOREIGN IMAGES
  FROM 11notes/util AS util
  

# ╔═════════════════════════════════════════════════════╗
# ║                       IMAGE                         ║
# ╚═════════════════════════════════════════════════════╝
  # :: HEADER
  FROM paperlessngx/paperless-ngx:${APP_VERSION}

  # :: default arguments
    ARG TARGETPLATFORM \
        TARGETOS \
        TARGETARCH \
        TARGETVARIANT \
        APP_IMAGE \
        APP_NAME \
        APP_VERSION \
        APP_ROOT \
        APP_UID \
        APP_GID \
        APP_NO_CACHE

  # :: default environment
    ENV APP_IMAGE=${APP_IMAGE} \
        APP_NAME=${APP_NAME} \
        APP_VERSION=${APP_VERSION} \
        APP_ROOT=${APP_ROOT}

  # :: application specific environment
    ENV USERMAP_UID=${APP_UID} \
        USERMAP_GID=${APP_GID} \
        PAPERLESS_DBHOST="postgres" \
        PAPERLESS_DBNAME="postgres" \
        PAPERLESS_DBUSER="postgres"

  # :: multi-stage
    COPY --from=util / /
    COPY ./rootfs /

# :: INSTALL
  USER root 

  RUN set -ex; \
    apt update -y; \
    pip install --upgrade pip;

  RUN set -ex; \
    cd /usr/src/paperless/src; \
    pip install django_python3_ldap;

  RUN set -ex; \
    find / -not -path "/proc/*" -user root -perm -4000 -exec chown -R ${APP_UID}:${APP_GID} {} \;

  RUN set -ex; \
    chown -R ${APP_UID}:${APP_GID} \
      /run;

# :: MONITORING
  HEALTHCHECK --interval=5s --timeout=2s --start-period=5s \
    CMD ["curl", "-kILs", "--fail", "-o", "/dev/null", "http://localhost:8000"]

# :: EXECUTE
  USER ${APP_UID}:${APP_GID}