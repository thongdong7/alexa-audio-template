#!/usr/bin/env bash

set -ex

git add -A

git commit -m "$@"

git push