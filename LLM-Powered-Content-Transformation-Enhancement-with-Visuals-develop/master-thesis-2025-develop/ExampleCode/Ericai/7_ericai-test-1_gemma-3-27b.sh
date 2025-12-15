#!/bin/bash

echo
echo "# Get ericai access token"
export ERICAI_ACCESS_TOKEN=$(ericai --ericsson-access-token)

SCRIPT="test-ericai-gemma-3-27b-it.py"
echo
echo "# Run python script: $SCRIPT"
python $SCRIPT
