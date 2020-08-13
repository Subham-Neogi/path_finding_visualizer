FROM gitpod/workspace-full

USER root
RUN apt-get update && apt-get install -y \
        tk-dev \
        python3-tk \
        python-tk \
    && pyenv install 3.7.6 \
    && pyenv local 3.7.6 \
    && apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
