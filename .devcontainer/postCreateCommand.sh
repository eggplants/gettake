#!/usr/bin/env sh

set -eux

# create poetry venvdir under projectdir
poetry config virtualenvs.in-project true
poetry install
git config --global --add safe.directory /workspaces/*
poetry run pre-commit

# Install typos cli
if
    ! command -v typos >/dev/null 2>&1
then
    curl -sLO https://raw.githubusercontent.com/crate-ci/gh-install/master/v1/install.sh
    sh install.sh -s -- --git crate-ci/typos --to ~/.local/bin --target x86_64-unknown-linux-musl
    rm install.sh
fi
