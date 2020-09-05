#!/bin/zsh

node-sass --watch \
    "../../src/easel/themes/$1/static/scss" \
    --output "../../src/easel/themes/$1/static/css"
