#!/bin/bash
pushd ..
gunicorn --bind 0.0.0.0:80 wsgi:app --chdir /app --timeout 600
popd