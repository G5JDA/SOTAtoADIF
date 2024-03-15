#!/bin/bash
# Check if venv is missing
if [ ! -d ".venv" ]; then
  echo "SOTAtoADIF Python venv does not exist, creating..."
  # create python venv
  python3 -m venv --prompt="SOTAtoADIF" .venv
  # activate the venv
  source .venv/bin/activate
  # install pip requirements
  pip install -r requirements.txt
fi

# activate the venv
source .venv/bin/activate
