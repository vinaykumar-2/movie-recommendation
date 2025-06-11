#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create .streamlit folder and write config.toml
mkdir -p ~/.streamlit/

cat << EOF > ~/.streamlit/config.toml
[server]
headless = true
enableCORS = false
port = $PORT
EOF