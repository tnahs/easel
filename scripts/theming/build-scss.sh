#!/bin/zsh

node-sass \
    "../../src/easel/themes/$1/static/scss" \
    --output "../../src/easel/themes/$1/static/css"
