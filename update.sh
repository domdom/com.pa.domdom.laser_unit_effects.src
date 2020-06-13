#!/usr/bin/env bash

git submodule update --recursive

pa_version=$(python3 -c "from src.pa_tools.pa.paths import PA_VERSION; print(PA_VERSION)")

cd src

python3 gen.py

do_git_update() {
    git checkout -B automated-update
    git add --all .
    git commit -m "Automated update: build $pa_version"
    git push
}

cd ../classic
do_git_update

cd ../titans
do_git_update

cd ..
do_git_update

