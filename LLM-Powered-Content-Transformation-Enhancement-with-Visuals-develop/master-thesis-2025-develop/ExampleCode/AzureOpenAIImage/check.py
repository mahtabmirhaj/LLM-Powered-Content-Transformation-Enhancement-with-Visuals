#!/bin/bash
 
export ENDPOINT_URL='https://ptco-ecn-azure-openai.openai.azure.com/'
export DEPLOYMENT_NAME='ptco-ecn-o1'
export AZURE_OPENAI_API_KEY='key'
 
if [ -z "${AZURE_OPENAI_API_KEY}" ]; then
    echo "Please set the following environment variables in your shell:"
    echo
    echo "export ENDPOINT_URL='https://<endpoint>.openai.azure.com/'"
    echo "export DEPLOYMENT_NAME='ptco-ecn-gpt-o1'"
    echo "export AZURE_OPENAI_API_KEY='key'"
    echo
    exit 1
fi
 
DOT_ENV_FILE=".env"
[ -e $DOT_ENV_FILE ] && sudo rm $DOT_ENV_FILE
echo "ENDPOINT_URL=${ENDPOINT_URL}" | sudo tee $DOT_ENV_FILE > /dev/null
echo "DEPLOYMENT_NAME=${DEPLOYMENT_NAME}" | sudo tee -a $DOT_ENV_FILE > /dev/null
echo "AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}" | sudo tee -a $DOT_ENV_FILE > /dev/null
