#!/bin/bash

coverage run -m pytest
coverage html
open ./htmlcov/index.html