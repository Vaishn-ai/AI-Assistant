#!/usr/bin/env bash
set -e
gunicorn assistant.wsgi:application --bind 0.0.0.0:${PORT:-8000}
