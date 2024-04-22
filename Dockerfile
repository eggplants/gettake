FROM python:3-slim

# docker build -t eggplants/gettake .
# docker run --rm eggplants/gettake --help

ARG VERSION
ENV VERSION ${VERSION:-master}

RUN <<-EOF
    set -x
    apt-get update
    apt-get install -y --no-install-recommends git=1:*
    apt-get autoremove -qq -y --purge
    apt-get clean
    rm -rf /var/lib/apt/lists/*
    pip install --no-cache-dir git+https://github.com/eggplants/gettake@${VERSION}
    apt-get purge -y --auto-remove git
EOF

ENTRYPOINT ["gettake"]
