#!/bin/bash

python -m src.easel \
    --debug \
    --loglevel="DEBUG" \
    --site-root="./examples/$1" \
    rebuild-site-cache