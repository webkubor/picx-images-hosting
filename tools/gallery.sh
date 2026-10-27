#!/bin/sh
# Portable entry point; Python generates and checks both documentation galleries.
exec python3 "$(dirname "$0")/gallery.py" "$@"
