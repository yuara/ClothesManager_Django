FROM jess/chrome

# Check chromedriver version http://chromedriver.chromium.org/downloads
ARG CHROMEDRIVER_VERSION=86.0.4240.22

USER root
# Install chromedriver
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    unzip \
    libgconf-2-4 \
    --no-install-recommends \
    && curl -sSL -O https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && chmod +x chromedriver \
    && mv -f chromedriver /usr/local/share/chromedriver \
    && ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
    && rm -f chromedriver_linux64.zip \
    && apt-get purge --auto-remove -y curl unzip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /src/*.deb

USER chrome
ENTRYPOINT []
