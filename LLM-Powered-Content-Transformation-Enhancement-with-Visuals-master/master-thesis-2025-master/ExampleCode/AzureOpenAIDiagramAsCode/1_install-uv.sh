#!/bin/bash

echo
echo "# Installing uv - An extremely fast Python package and project manager ..."

curl -LsSf https://astral.sh/uv/install.sh | sh

echo
which uv

echo
uv self update
