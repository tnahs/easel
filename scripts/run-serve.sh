#!/bin/bash

# scripts/run-serve.sh sorolla-demo
# scripts/run-serve.sh testing-demo

python -m src.easel \
    --debug \
    --loglevel="DEBUG" \
    --site-root="./examples/$1" \
    serve \
    --watch \
    --host="0.0.0.0" \
    --port="5000" \