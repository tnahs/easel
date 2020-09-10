# !/bin/zsh

python -m src.easel serve \
    --debug \
    --loglevel="DEBUG" \
    --site-root="./examples/$1" \
    --host="0.0.0.0" \
    --port="5000" \