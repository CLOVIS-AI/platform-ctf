ARG DOCKER_PROXY
FROM $DOCKER_PROXY/oznu/s6-node:16.13.2-amd64

RUN apk add --no-cache git python2 python3 make g++ avahi-compat-libdns_sd avahi-dev dbus \
    iputils sudo nano \
  && chmod 4755 /bin/ping \
  && mkdir /homebridge \
  && npm set global-style=true \
  && npm set audit=false \
  && npm set fund=false

RUN case "$(uname -m)" in \
    x86_64) FFMPEG_ARCH='x86_64';; \
    armv6l) FFMPEG_ARCH='armv6l';; \
    armv7l) FFMPEG_ARCH='armv6l';; \
    aarch64) FFMPEG_ARCH='aarch64';; \
    *) echo "unsupported architecture"; exit 1 ;; \
    esac \
    && set -x \
    && curl -Lfs https://github.com/oznu/ffmpeg-for-homebridge/releases/download/v0.0.9/ffmpeg-alpine-${FFMPEG_ARCH}.tar.gz | tar xzf - -C / --no-same-owner

ENV PATH="${PATH}:/homebridge/node_modules/.bin"

ENV HOMEBRIDGE_VERSION=1.4.0
RUN npm install -g --unsafe-perm homebridge@${HOMEBRIDGE_VERSION}

ENV CONFIG_UI_VERSION=4.42.0 HOMEBRIDGE_CONFIG_UI=1 HOMEBRIDGE_CONFIG_UI_PORT=8581
RUN npm install -g --unsafe-perm homebridge-config-ui-x@${CONFIG_UI_VERSION} && npm install -g homebridge-http-iot@latest

WORKDIR /homebridge
VOLUME /homebridge

COPY root /
COPY myfiles/config.json .
COPY myfiles/auth.json .

ARG AVAHI
ENV ENABLE_AVAHI="${AVAHI:-0}"
