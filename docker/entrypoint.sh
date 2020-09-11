#!/bin/sh

if [ -z "$@" ]; then
    uwsgi --ini /app/docker/uwsgi.ini --die-on-term
else
    python3 /app/main.py --conllu-comments "$@"
fi
