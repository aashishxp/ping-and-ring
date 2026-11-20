<<<<<<< Updated upstream
=======
FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm
ENV PYTHONUNBUFFERED=1
RUN curl --fail --location --silent --show-error https://astral.sh/uv/install.sh --output /tmp/uv-install.sh \
    && UV_INSTALL_DIR=/usr/local/bin sh /tmp/uv-install.sh \
    && rm /tmp/uv-install.sh
>>>>>>> Stashed changes
