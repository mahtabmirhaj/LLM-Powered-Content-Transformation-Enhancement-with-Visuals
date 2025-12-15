#!/bin/bash

echo
echo "# Run first:"
echo "source .venv/bin/activate"
echo
echo "# Get ericai access token"
export ERICAI_ACCESS_TOKEN=$(ericai --ericsson-access-token)
# echo $ERICAI_ACCESS_TOKEN

API_VERSION="2024-02-15-preview"
export OPENAI_API_VERSION=${API_VERSION}

SCRIPT="test-ericai-qwen2.5-vl-32b-it.py"
echo
echo "# Run script: $SCRIPT"
python $SCRIPT
