#!/bin/bash

# Quick script to get results for a specific analysis ID
# Usage: ./get_results.sh <analysis_id>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <analysis_id>"
    echo "Example: $0 123e4567-e89b-12d3-a456-426614174000"
    exit 1
fi

ANALYSIS_ID="$1"
BASE_URL="http://localhost:8005"

echo "🔍 Getting results for analysis: $ANALYSIS_ID"
echo "=============================================="

# Get the analysis results
RESPONSE=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID")

if [ $? -eq 0 ]; then
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
else
    echo "❌ Error getting results for analysis $ANALYSIS_ID"
    echo "Make sure the agent service is running and the ID is correct."
fi
