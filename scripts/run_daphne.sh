#!/bin/sh

set -e

daphne -b 0.0.0.0 -p 8001 taskmaster.asgi:application