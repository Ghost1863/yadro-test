# syntax=docker/dockerfile:1.7
ARG UBUNTU_DIGEST=sha256:962f6cadeae0ea6284001009daa4cc9a8c37e75d1f5191cf0eb83fe565b63dd7

FROM ubuntu:22.04@${UBUNTU_DIGEST} AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VENV_PATH=/opt/venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv "${VENV_PATH}"

WORKDIR /opt/build
COPY section1/requirements.txt ./requirements.txt
RUN "${VENV_PATH}/bin/pip" install --no-cache-dir -r requirements.txt


FROM ubuntu:22.04@${UBUNTU_DIGEST} AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH=/opt/venv/bin:${PATH}

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        python3 \
        ca-certificates \
        tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 app \
    && useradd  --system --uid 10001 --gid app --home-dir /nonexistent --shell /usr/sbin/nologin app

COPY --from=builder --chown=app:app /opt/venv /opt/venv

WORKDIR /opt/app
COPY --chown=app:app section1/http_checker ./http_checker

USER 10001:10001

LABEL org.opencontainers.image.title="http-checker" \
      org.opencontainers.image.description="HTTP status probe for httpstat.us" \
      org.opencontainers.image.source="https://github.com/" \
      org.opencontainers.image.licenses="MIT"

ENTRYPOINT ["/usr/bin/tini", "--", "python3", "-m", "http_checker"]
CMD ["100", "200", "301", "404", "500"]
