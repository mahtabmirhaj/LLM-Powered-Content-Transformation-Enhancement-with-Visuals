#!/bin/bash

echo
echo "# Using uv to create my Python virtual environment:"

PYTHON_VERSION="3.11"
VENV=".venv"

echo
if [ -d "$VENV" ]; then

    echo "Directory already exists: $VENV"

else

    echo "# Creating venv for Python $PYTHON_VERSION:"
    echo "uv venv $VENV --python $PYTHON_VERSION"
    uv venv $VENV --python $PYTHON_VERSION

fi

echo
echo "# To activate $VENV, run:"
echo "  $ source ${VENV}/bin/activate"
echo

