#!/bin/bash

# Content Analysis Agent Test Script
# This script provides various testing options for the agent

echo "🧪 Content Analysis Agent Test Suite"
echo "====================================="
echo ""

# Check if the agent service is running
check_service() {
    echo "🔍 Checking if agent service is running..."
    if curl -s http://localhost:8005/status > /dev/null 2>&1; then
        echo "✅ Agent service is running on port 8005"
        return 0
    else
        echo "❌ Agent service is not running on port 8005"
        echo "   Please start the service first with: ./start_service.sh"
        return 1
    fi
}

# Quick health check
health_check() {
    echo ""
    echo "🏥 Running health check..."
    curl -s http://localhost:8005/status | jq '.' 2>/dev/null || curl -s http://localhost:8005/status
}

# Test content analysis
test_analysis() {
    echo ""
    echo "📝 Testing content analysis..."
    
    # Sample content for analysis
    sample_content="Artificial Intelligence is transforming how we work and live. The rapid advancement of AI technologies brings both opportunities and challenges that we must carefully consider."
    
    echo "   Submitting content for comprehensive analysis..."
    
    response=$(curl -s -X POST http://localhost:8005/analyze \
        -H "Content-Type: application/json" \
        -d "{\"content\": \"$sample_content\", \"analysis_type\": \"comprehensive\"}")
    
    if echo "$response" | grep -q "analysis_id"; then
        analysis_id=$(echo "$response" | grep -o '"analysis_id":"[^"]*"' | cut -d'"' -f4)
        echo "   ✅ Analysis submitted successfully!"
        echo "   Analysis ID: $analysis_id"
        
        # Wait a bit and check status
        echo "   ⏳ Waiting for analysis to complete..."
        sleep 5
        
        status_response=$(curl -s "http://localhost:8005/analysis/$analysis_id")
        echo "   Status response:"
        echo "$status_response" | jq '.' 2>/dev/null || echo "$status_response"
        
    else
        echo "   ❌ Analysis submission failed:"
        echo "$response"
    fi
}

# Test different analysis types
test_analysis_types() {
    echo ""
    echo "🎯 Testing different analysis types..."
    
    test_content="The weather is beautiful today and I feel optimistic about the future!"
    
    for analysis_type in "thematic" "sentiment" "summary"; do
        echo "   Testing $analysis_type analysis..."
        
        response=$(curl -s -X POST http://localhost:8005/analyze \
            -H "Content-Type: application/json" \
            -d "{\"content\": \"$test_content\", \"analysis_type\": \"$analysis_type\"}")
        
        if echo "$response" | grep -q "analysis_id"; then
            echo "   ✅ $analysis_type analysis submitted"
        else
            echo "   ❌ $analysis_type analysis failed"
        fi
    done
}

# List all jobs
list_jobs() {
    echo ""
    echo "📋 Listing all analysis jobs..."
    jobs_response=$(curl -s http://localhost:8005/jobs)
    echo "$jobs_response" | jq '.' 2>/dev/null || echo "$jobs_response"
}

# Run Python test scripts
run_python_tests() {
    echo ""
    echo "🐍 Running Python test scripts..."
    
    if command -v python3 &> /dev/null; then
        echo "   Running quick test..."
        python3 quick_test.py
        
        echo ""
        echo "   Running comprehensive test..."
        python3 test_agent.py
    else
        echo "   Python3 not found, skipping Python tests"
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "Choose a test option:"
    echo "1) Health check only"
    echo "2) Test content analysis"
    echo "3) Test different analysis types"
    echo "4) List all jobs"
    echo "5) Run Python test scripts"
    echo "6) Run all tests"
    echo "7) Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            health_check
            ;;
        2)
            health_check
            test_analysis
            ;;
        3)
            health_check
            test_analysis_types
            ;;
        4)
            health_check
            list_jobs
            ;;
        5)
            run_python_tests
            ;;
        6)
            health_check
            test_analysis
            test_analysis_types
            list_jobs
            run_python_tests
            ;;
        7)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Check if jq is available for JSON formatting
if ! command -v jq &> /dev/null; then
    echo "⚠️  Note: 'jq' not found. JSON responses will not be formatted."
    echo "   Install jq for better output formatting: brew install jq (macOS) or apt-get install jq (Ubuntu)"
    echo ""
fi

# Main execution
if [ "$1" = "auto" ]; then
    # Auto-run all tests
    echo "🤖 Auto-running all tests..."
    check_service && {
        health_check
        test_analysis
        test_analysis_types
        list_jobs
        run_python_tests
    }
else
    # Interactive mode
    check_service && show_menu
fi

echo ""
echo "🎉 Testing completed!"
