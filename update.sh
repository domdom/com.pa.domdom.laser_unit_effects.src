#!/usr/bin/env bash

set -ex

git submodule update --recursive

pa_version=$(python3 -c "from src.pa_tools.pa.paths import PA_VERSION; print(PA_VERSION)")

cd src

python3 gen.py

cd ..

do_git_update() {
    local dir="$1"
    git -C "$dir" checkout -B master
    git -C "$dir" add --all .
    git -C "$dir" commit -m "Automated update: build $pa_version" || true
    git -C "$dir" push
}

do_git_update classic
do_git_update titans
do_git_update .

