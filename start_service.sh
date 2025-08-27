#!/bin/bash

# Content Analysis Agent Startup Script
# This script starts the Content Analysis Agent service with Dapr

echo "Starting Content Analysis Agent Service..."

# Check if Dapr is installed
if ! command -v dapr &> /dev/null; then
    echo "Error: Dapr CLI is not installed. Please install Dapr first."
    echo "Visit: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Please create one with your OpenAI API key:"
    echo "OPENAI_API_KEY=your_api_key_here"
    echo ""
fi

# Start the service with Dapr
echo "Starting service on port 8005 with Dapr..."
dapr run \
    --app-id content-analyzer \
    --app-port 8005 \
    --dapr-http-port 3505 \
    --resources-path ./components \
    -- python services/content-analyzer/app.py

echo "Service stopped."
