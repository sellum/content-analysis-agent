#!/usr/bin/env python3
"""
Simple test script to send requests to the Content Analysis Agent.
Run this after starting the agent service.
"""

import requests
import json
import time
from typing import Dict, Any


def test_health_check(base_url: str = "http://localhost:8005") -> bool:
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False


def test_content_analysis(base_url: str = "http://localhost:8005") -> Dict[str, Any]:
    """Test content analysis with sample text."""
    print("\n📝 Testing content analysis...")
    
    sample_content = """
    Artificial Intelligence is revolutionizing the way we work and live. 
    From virtual assistants to autonomous vehicles, AI technologies are 
    becoming increasingly integrated into our daily lives.
    
    However, this rapid advancement also raises important questions about 
    privacy, ethics, and the future of employment. We must carefully 
    consider how to harness AI's benefits while addressing its challenges.
    """
    
    payload = {
        "content": sample_content,
        "analysis_type": "comprehensive"
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis request submitted successfully!")
            print(f"   Analysis ID: {result['analysis_id']}")
            print(f"   Status: {result['status']}")
            return result
        else:
            print(f"❌ Analysis request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return {}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Analysis request error: {e}")
        return {}


def wait_for_analysis(base_url: str, analysis_id: str, max_wait: int = 60) -> Dict[str, Any]:
    """Wait for analysis to complete and return results."""
    print(f"\n⏳ Waiting for analysis {analysis_id} to complete...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{base_url}/analysis/{analysis_id}", timeout=5)
            if response.status_code == 200:
                status = response.json()
                current_status = status.get("status", "unknown")
                
                print(f"   Current status: {current_status}")
                
                if current_status == "completed":
                    print("✅ Analysis completed successfully!")
                    return status
                elif current_status == "failed":
                    print("❌ Analysis failed!")
                    return status
                
                # Wait before checking again
                time.sleep(3)
            else:
                print(f"   Error checking status: {response.status_code}")
                time.sleep(3)
                
        except requests.exceptions.RequestException as e:
            print(f"   Error checking status: {e}")
            time.sleep(3)
    
    print("⏰ Timeout waiting for analysis completion")
    return {"status": "timeout", "error": "Analysis did not complete within timeout period"}


def test_different_analysis_types(base_url: str = "http://localhost:8005"):
    """Test different types of analysis."""
    print("\n🎯 Testing different analysis types...")
    
    # Test content
    test_content = "The weather is beautiful today and I feel great about the future!"
    
    analysis_types = ["thematic", "sentiment", "summary"]
    
    for analysis_type in analysis_types:
        print(f"\n--- Testing {analysis_type} analysis ---")
        
        payload = {
            "content": test_content,
            "analysis_type": analysis_type
        }
        
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {analysis_type} analysis submitted: {result['analysis_id']}")
                
                # Wait for completion
                final_result = wait_for_analysis(base_url, result['analysis_id'], max_wait=30)
                if final_result.get("status") == "completed":
                    print(f"✅ {analysis_type} analysis completed!")
                else:
                    print(f"❌ {analysis_type} analysis failed or timed out")
            else:
                print(f"❌ {analysis_type} analysis request failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {analysis_type} analysis error: {e}")


def test_jobs_endpoint(base_url: str = "http://localhost:8005"):
    """Test the jobs listing endpoint."""
    print("\n📋 Testing jobs endpoint...")
    
    try:
        response = requests.get(f"{base_url}/jobs", timeout=5)
        if response.status_code == 200:
            jobs = response.json()
            print("✅ Jobs endpoint working!")
            print(f"   Total jobs: {jobs.get('total_jobs', 0)}")
            
            for job in jobs.get('jobs', []):
                print(f"   - {job['analysis_id']}: {job['status']} ({job['analysis_type']})")
        else:
            print(f"❌ Jobs endpoint failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Jobs endpoint error: {e}")


def main():
    """Main test function."""
    base_url = "http://localhost:8005"
    
    print("🚀 Content Analysis Agent Test Suite")
    print("=" * 50)
    print(f"Testing agent at: {base_url}")
    print("Make sure the agent service is running before executing this script!")
    print()
    
    # Test 1: Health check
    if not test_health_check(base_url):
        print("\n❌ Agent service is not responding. Please start the service first.")
        return
    
    # Test 2: Basic content analysis
    analysis_result = test_content_analysis(base_url)
    if analysis_result:
        # Wait for completion
        final_result = wait_for_analysis(base_url, analysis_result['analysis_id'])
        if final_result.get("status") == "completed":
            print("\n📊 Analysis Results:")
            print(json.dumps(final_result.get("results", {}), indent=2))
    
    # Test 3: Different analysis types
    test_different_analysis_types(base_url)
    
    # Test 4: Jobs endpoint
    test_jobs_endpoint(base_url)
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
