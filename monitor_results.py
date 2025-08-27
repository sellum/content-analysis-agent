#!/usr/bin/env python3
"""
Real-time monitoring script for Content Analysis Agent results.
This script continuously monitors analysis jobs and displays results as they complete.
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, Any


class ResultsMonitor:
    """Monitor analysis jobs and display results in real-time."""
    
    def __init__(self, base_url: str = "http://localhost:8005"):
        self.base_url = base_url
        self.known_jobs = set()
        self.completed_jobs = set()
    
    def get_all_jobs(self) -> Dict[str, Any]:
        """Get all analysis jobs."""
        try:
            response = requests.get(f"{self.base_url}/jobs", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting jobs: {response.status_code}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {}
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a specific job."""
        try:
            response = requests.get(f"{self.base_url}/analysis/{job_id}", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "error": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}
    
    def display_job_results(self, job_data: Dict[str, Any]):
        """Display formatted job results."""
        job_id = job_data.get("analysis_id", "unknown")
        status = job_data.get("status", "unknown")
        timestamp = job_data.get("timestamp", "unknown")
        
        print(f"\n{'='*60}")
        print(f"📊 ANALYSIS RESULTS - {job_id}")
        print(f"{'='*60}")
        print(f"Status: {status}")
        print(f"Submitted: {timestamp}")
        
        if job_data.get("completed_at"):
            print(f"Completed: {job_data['completed_at']}")
        
        if status == "completed" and job_data.get("results"):
            results = job_data["results"]
            
            # Display themes
            if results.get("themes"):
                print(f"\n🎯 Key Themes:")
                for theme in results["themes"]:
                    print(f"   • {theme}")
            
            # Display sentiment
            if results.get("sentiment"):
                print(f"\n😊 Sentiment: {results['sentiment']}")
            
            # Display confidence
            if results.get("confidence"):
                print(f"\n📈 Confidence: {results['confidence']}")
            
            # Display summary
            if results.get("summary"):
                print(f"\n📝 Summary:")
                print(f"   {results['summary']}")
            
            # Display recommendations
            if results.get("recommendations"):
                print(f"\n💡 Recommendations:")
                for rec in results["recommendations"]:
                    print(f"   • {rec}")
            
            # Display raw response if available
            if results.get("raw_response"):
                print(f"\n🔍 Raw Analysis:")
                print(f"   {results['raw_response']}")
                
        elif status == "failed":
            error = job_data.get("error", "Unknown error")
            print(f"\n❌ Analysis Failed:")
            print(f"   {error}")
        
        elif status == "processing":
            print(f"\n⏳ Analysis still in progress...")
        
        print(f"{'='*60}")
    
    def monitor_continuously(self, check_interval: int = 5):
        """Continuously monitor for new jobs and results."""
        print("🔍 Starting real-time monitoring of Content Analysis Agent...")
        print(f"Monitoring URL: {self.base_url}")
        print(f"Check interval: {check_interval} seconds")
        print("Press Ctrl+C to stop monitoring")
        print("-" * 60)
        
        try:
            while True:
                # Get all jobs
                jobs_data = self.get_all_jobs()
                current_jobs = set()
                
                if jobs_data.get("jobs"):
                    for job in jobs_data["jobs"]:
                        job_id = job["analysis_id"]
                        current_jobs.add(job_id)
                        
                        # Check if this is a new job
                        if job_id not in self.known_jobs:
                            self.known_jobs.add(job_id)
                            print(f"\n🆕 New job detected: {job_id}")
                            print(f"   Type: {job.get('analysis_type', 'unknown')}")
                            print(f"   Status: {job.get('status', 'unknown')}")
                        
                        # Check if job completed and we haven't seen results yet
                        if (job["status"] == "completed" and 
                            job_id not in self.completed_jobs):
                            
                            # Get detailed results
                            detailed_job = self.get_job_status(job_id)
                            self.display_job_results(detailed_job)
                            self.completed_jobs.add(job_id)
                
                # Show summary
                total_jobs = jobs_data.get("total_jobs", 0)
                if total_jobs > 0:
                    print(f"\r📊 Monitoring {total_jobs} jobs... (Press Ctrl+C to stop)", end="", flush=True)
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            print(f"Total jobs monitored: {len(self.known_jobs)}")
            print(f"Completed jobs: {len(self.completed_jobs)}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor Content Analysis Agent results")
    parser.add_argument("--url", default="http://localhost:8005", 
                       help="Base URL of the agent service")
    parser.add_argument("--interval", type=int, default=5,
                       help="Check interval in seconds (default: 5)")
    
    args = parser.parse_args()
    
    monitor = ResultsMonitor(args.url)
    monitor.monitor_continuously(args.interval)


if __name__ == "__main__":
    main()
