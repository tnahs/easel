#!/bin/bash

# scripts/run-rebuild-site-cache.sh sorolla-demo
# scripts/run-rebuild-site-cache.sh testing-demo

python -m src.easel \
    --debug \
    --loglevel="DEBUG" \
    --site-root="./examples/$1" \
    rebuild-site-cache