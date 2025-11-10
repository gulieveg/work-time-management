#!/bin/bash

black . -l 120

isort . -l 120 --profile=black

find . -type d -name "__pycache__" -exec rm -r {} +

git add .; git commit -m ":tada: Next commit"; git push
