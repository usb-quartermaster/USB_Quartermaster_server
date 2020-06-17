#!/bin/bash
set -eux

if [ ! -d quartermaster_server ]; then
  ehco "This script should be run from the repository root"
  exit 1
fi

# Generate static files from Django
STATIC_FILES_DIR="$PWD/deploy/static"
rm -rf "$STATIC_FILES_DIR"
docker-compose build backend
docker-compose run -v "$STATIC_FILES_DIR":/deploy/static backend ./manage.py collectstatic --noinput

# Build everything else
docker-compose build

# Cleanup static files (Doing this in docker to get around any permissions issues)
docker-compose run -v $STATIC_FILES_DIR:$STATIC_FILES_DIR --workdir $STATIC_FILES_DIR backend rm -rf $STATIC_FILES_DIR/*
rm -rf "$STATIC_FILES_DIR"
