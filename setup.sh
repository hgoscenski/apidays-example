#!/bin/bash

if ! command -v pyenv &> /dev/null
then
    echo "pyenv missing, exiting"
    exit 1
fi

if ! command -v make &> /dev/null
then
    echo "make missing, exiting"
    exit 1
fi

# uses pyenv to set the correct python version
pyenv install 3.11
pyenv local 3.11

# setup huggingface login
pip install huggingface_hub
echo ''
echo 'Installing huggingface cli, enter HF credential when prompted'
echo ''
huggingface-cli login

# install dependencies
poetry install --extras "ui llms-llama-cpp embeddings-huggingface vector-stores-qdrant"
# downloads model and setups scripts
poetry run python scripts/setup

# run privateGPT with configured local models
PGPT_PROFILES=local make run