#!/bin/bash

# Script for code formatting and cleaning __pycache__

echo "Running black..."
black . -l 120

echo "Running isort..."
isort . -l 120 --profile=black

echo "Removing __pycache__..."
find . -type d -name "__pycache__" -exec rm -r {} +

echo "Done!"
