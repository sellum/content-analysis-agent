#!/bin/bash

# Simple curl tests for Content Analysis Agent
# Run this after starting the agent service

BASE_URL="http://localhost:8005"

echo "🧪 Simple curl tests for Content Analysis Agent"
echo "==============================================="
echo ""

# Test 1: Health check
echo "1. Health check:"
curl -s "$BASE_URL/status" | jq '.' 2>/dev/null || curl -s "$BASE_URL/status"
echo ""
echo ""

# Test 2: Submit analysis
echo "2. Submit content analysis:"
ANALYSIS_RESPONSE=$(curl -s -X POST "$BASE_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI is transforming industries and creating new opportunities for innovation and growth.",
    "analysis_type": "comprehensive"
  }')

echo "$ANALYSIS_RESPONSE" | jq '.' 2>/dev/null || echo "$ANALYSIS_RESPONSE"
echo ""

# Extract analysis ID if successful
if echo "$ANALYSIS_RESPONSE" | grep -q "analysis_id"; then
    ANALYSIS_ID=$(echo "$ANALYSIS_RESPONSE" | grep -o '"analysis_id":"[^"]*"' | cut -d'"' -f4)
    echo "Analysis ID: $ANALYSIS_ID"
    echo ""
    
    # Test 3: Check analysis status
    echo "3. Check analysis status:"
    sleep 3  # Wait a bit for processing
    curl -s "$BASE_URL/analysis/$ANALYSIS_ID" | jq '.' 2>/dev/null || curl -s "$BASE_URL/analysis/$ANALYSIS_ID"
    echo ""
fi

# Test 4: List all jobs
echo "4. List all jobs:"
curl -s "$BASE_URL/jobs" | jq '.' 2>/dev/null || curl -s "$BASE_URL/jobs"
echo ""

echo "🎉 Curl tests completed!"
