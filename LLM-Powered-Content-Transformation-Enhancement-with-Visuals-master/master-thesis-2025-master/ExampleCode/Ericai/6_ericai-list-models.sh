#!/bin/bash

API_VERSION="2024-02-15-preview"
export OPENAI_API_VERSION=${API_VERSION}

FILE="Ericai-Model-list.json"
ericai api models.list | jq > $FILE
echo
echo "# Ericai list all models..."
cat $FILE | jq '.id, .deployment_status'

echo
echo "# The full list can be found in the file: $FILE"
