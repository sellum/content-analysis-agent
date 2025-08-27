#!/usr/bin/env python3
import requests
import time
import sys
import json
from typing import Dict, Any


class ContentAnalysisClient:
    """Client for interacting with the Content Analysis Agent."""
    
    def __init__(self, base_url: str = "http://localhost:8005"):
        self.base_url = base_url
        self.status_url = f"{base_url}/status"
        self.analyze_url = f"{base_url}/analyze"
        self.jobs_url = f"{base_url}/jobs"
    
    def health_check(self, max_attempts: int = 10) -> bool:
        """Check if the service is healthy."""
        print("Checking service health...")
        
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Attempt {attempt}...")
                response = requests.get(self.status_url, timeout=5)
                
                if response.status_code == 200:
                    print("Content Analysis Agent is healthy!")
                    return True
                else:
                    print(f"Received status code {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            
            if attempt < max_attempts:
                print("Waiting 5 seconds before next health check attempt...")
                time.sleep(5)
        
        print("Service is not healthy after maximum attempts!")
        return False
    
    def analyze_content(self, content: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Submit a content analysis job."""
        payload = {
            "content": content,
            "analysis_type": analysis_type
        }
        
        print(f"Submitting {analysis_type} analysis job...")
        
        for attempt in range(1, 11):
            try:
                print(f"Attempt {attempt}...")
                response = requests.post(
                    self.analyze_url, 
                    json=payload, 
                    timeout=10,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("Analysis job submitted successfully!")
                    print(f"Job ID: {result['analysis_id']}")
                    return result
                else:
                    print(f"Received status code {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            
            if attempt < 10:
                print("Waiting 1 second before next attempt...")
                time.sleep(1)
        
        raise Exception("Failed to submit analysis job after maximum attempts")
    
    def get_analysis_status(self, analysis_id: str) -> Dict[str, Any]:
        """Get the status of an analysis job."""
        url = f"{self.base_url}/analysis/{analysis_id}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting status: {response.status_code} - {response.text}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}
    
    def wait_for_completion(self, analysis_id: str, max_wait: int = 300) -> Dict[str, Any]:
        """Wait for an analysis job to complete."""
        print(f"Waiting for analysis {analysis_id} to complete...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            status = self.get_analysis_status(analysis_id)
            
            if status.get("status") == "completed":
                print("Analysis completed successfully!")
                return status
            elif status.get("status") == "failed":
                print("Analysis failed!")
                return status
            
            print(f"Status: {status.get('status', 'unknown')} - waiting 5 seconds...")
            time.sleep(5)
        
        print("Timeout waiting for analysis completion")
        return {"status": "timeout", "error": "Analysis did not complete within timeout period"}
    
    def list_jobs(self) -> Dict[str, Any]:
        """List all analysis jobs."""
        try:
            response = requests.get(self.jobs_url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error listing jobs: {response.status_code} - {response.text}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}


def main():
    """Main function to demonstrate the client usage."""
    client = ContentAnalysisClient()
    
    # Check service health
    if not client.health_check():
        print("Service is not healthy. Exiting.")
        sys.exit(1)
    
    # Example content for analysis
    sample_content = """
    Artificial Intelligence (AI) is transforming industries across the globe. 
    From healthcare to finance, manufacturing to retail, AI technologies are 
    enabling unprecedented levels of automation, efficiency, and innovation. 
    
    Machine learning algorithms can now process vast amounts of data to identify 
    patterns and make predictions with remarkable accuracy. Deep learning models 
    are revolutionizing computer vision, natural language processing, and 
    autonomous systems.
    
    However, the rapid advancement of AI also raises important questions about 
    ethics, privacy, and the future of work. Organizations must carefully 
    consider how to implement AI responsibly while maximizing its benefits.
    
    The key to successful AI adoption lies in understanding both the technical 
    capabilities and the human factors involved. Companies that can balance 
    innovation with responsibility will be best positioned to thrive in the 
    AI-powered future.
    """
    
    try:
        # Submit comprehensive analysis
        print("\n" + "="*50)
        print("SUBMITTING COMPREHENSIVE ANALYSIS")
        print("="*50)
        
        result = client.analyze_content(sample_content, "comprehensive")
        analysis_id = result["analysis_id"]
        
        # Wait for completion
        print("\n" + "="*50)
        print("WAITING FOR ANALYSIS COMPLETION")
        print("="*50)
        
        final_result = client.wait_for_completion(analysis_id)
        
        if final_result.get("status") == "completed":
            print("\n" + "="*50)
            print("ANALYSIS RESULTS")
            print("="*50)
            print(json.dumps(final_result.get("results", {}), indent=2))
        
        # Submit thematic analysis
        print("\n" + "="*50)
        print("SUBMITTING THEMATIC ANALYSIS")
        print("="*50)
        
        thematic_result = client.analyze_content(sample_content, "thematic")
        thematic_id = thematic_result["analysis_id"]
        
        # Wait for thematic analysis completion
        thematic_final = client.wait_for_completion(thematic_id)
        
        if thematic_final.get("status") == "completed":
            print("\n" + "="*50)
            print("THEMATIC ANALYSIS RESULTS")
            print("="*50)
            print(json.dumps(thematic_final.get("results", {}), indent=2))
        
        # List all jobs
        print("\n" + "="*50)
        print("ALL ANALYSIS JOBS")
        print("="*50)
        
        jobs = client.list_jobs()
        print(json.dumps(jobs, indent=2))
        
        print("\n" + "="*50)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*50)
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
