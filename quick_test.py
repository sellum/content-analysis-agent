#!/usr/bin/env python3
"""
Quick test script for the Content Analysis Agent.
Simple and fast testing of basic functionality.
"""

import requests
import json


def quick_test():
    """Run a quick test of the agent."""
    base_url = "http://localhost:8005"
    
    print("🚀 Quick Test - Content Analysis Agent")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            print("   ✅ Service is healthy")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Cannot connect to service: {e}")
        return
    
    # Test 2: Submit analysis
    print("\n2. Submitting content for analysis...")
    
    test_content = "AI is transforming industries and creating new opportunities for innovation and growth."
    
    payload = {
        "content": test_content,
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
            analysis_id = result['analysis_id']
            print(f"   ✅ Analysis submitted: {analysis_id}")
            
            # Test 3: Check status
            print(f"\n3. Checking analysis status...")
            status_response = requests.get(f"{base_url}/analysis/{analysis_id}", timeout=5)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   Status: {status_data.get('status')}")
                
                if status_data.get('results'):
                    print("   Results available!")
                else:
                    print("   Results not yet available")
            else:
                print(f"   ❌ Status check failed: {status_response.status_code}")
                
        else:
            print(f"   ❌ Analysis submission failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
    
    # Test 4: List jobs
    print("\n4. Listing all jobs...")
    try:
        jobs_response = requests.get(f"{base_url}/jobs", timeout=5)
        if jobs_response.status_code == 200:
            jobs = jobs_response.json()
            print(f"   Total jobs: {jobs.get('total_jobs', 0)}")
        else:
            print(f"   ❌ Jobs listing failed: {jobs_response.status_code}")
    except Exception as e:
        print(f"   ❌ Jobs error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Quick test completed!")


if __name__ == "__main__":
    quick_test()
