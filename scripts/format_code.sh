# !/bin/sh

set -e

isort --profile black .
black .
