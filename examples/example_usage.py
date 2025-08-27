#!/usr/bin/env python3
"""
Example usage of the Content Analysis Agent with different types of content.
This demonstrates the agent's capabilities across various domains.
"""

import asyncio
import requests
import json
from typing import Dict, Any


class ContentAnalysisExamples:
    """Examples of using the Content Analysis Agent with different content types."""
    
    def __init__(self, base_url: str = "http://localhost:8005"):
        self.base_url = base_url
        self.analyze_url = f"{base_url}/analyze"
    
    def submit_analysis(self, content: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Submit content for analysis."""
        payload = {
            "content": content,
            "analysis_type": analysis_type
        }
        
        try:
            response = requests.post(
                self.analyze_url,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}
    
    def wait_for_completion(self, analysis_id: str, max_wait: int = 300) -> Dict[str, Any]:
        """Wait for analysis completion."""
        url = f"{self.base_url}/analysis/{analysis_id}"
        
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < max_wait:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    status = response.json()
                    if status.get("status") == "completed":
                        return status
                    elif status.get("status") == "failed":
                        return status
                
                print(f"Status: {status.get('status', 'unknown')} - waiting 5 seconds...")
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"Error checking status: {e}")
                await asyncio.sleep(5)
        
        return {"status": "timeout", "error": "Analysis did not complete within timeout period"}
    
    async def run_examples(self):
        """Run various examples demonstrating the agent's capabilities."""
        
        print("="*70)
        print("CONTENT ANALYSIS AGENT EXAMPLES")
        print("="*70)
        
        # Example 1: Business/Technology Content
        print("\n1. BUSINESS/TECHNOLOGY CONTENT ANALYSIS")
        print("-" * 50)
        
        business_content = """
        The rise of artificial intelligence and machine learning is fundamentally 
        transforming business operations across industries. Companies implementing 
        AI solutions report 20-30% improvements in operational efficiency and 
        significant cost reductions. However, successful AI adoption requires 
        careful change management, employee training, and ethical considerations.
        
        Organizations must balance innovation with responsibility, ensuring that 
        AI systems are transparent, fair, and aligned with business values. 
        The future belongs to companies that can harness AI's power while 
        maintaining human oversight and ethical standards.
        """
        
        print("Submitting business content for comprehensive analysis...")
        result = self.submit_analysis(business_content, "comprehensive")
        
        if result:
            print(f"Analysis submitted with ID: {result['analysis_id']}")
            print("Waiting for completion...")
            
            final_result = await self.wait_for_completion(result['analysis_id'])
            if final_result.get("status") == "completed":
                print("✓ Business content analysis completed!")
        
        # Example 2: Creative Writing Analysis
        print("\n2. CREATIVE WRITING SENTIMENT ANALYSIS")
        print("-" * 50)
        
        creative_content = """
        The old oak tree stood majestically in the center of the meadow, its 
        branches reaching toward the heavens like ancient arms. Golden sunlight 
        filtered through the leaves, creating a magical dance of light and shadow 
        on the grass below. Birds sang sweet melodies from hidden perches, and 
        a gentle breeze carried the scent of wildflowers.
        
        It was a place of peace and wonder, where time seemed to stand still 
        and the worries of the world melted away like morning mist.
        """
        
        print("Submitting creative content for sentiment analysis...")
        result = self.submit_analysis(creative_content, "sentiment")
        
        if result:
            print(f"Analysis submitted with ID: {result['analysis_id']}")
            print("Waiting for completion...")
            
            final_result = await self.wait_for_completion(result['analysis_id'])
            if final_result.get("status") == "completed":
                print("✓ Creative content sentiment analysis completed!")
        
        # Example 3: News Article Thematic Analysis
        print("\n3. NEWS ARTICLE THEMATIC ANALYSIS")
        print("-" * 50)
        
        news_content = """
        Climate change continues to accelerate at an alarming rate, with global 
        temperatures rising faster than predicted by early models. Scientists 
        warn that we have a narrow window of opportunity to implement effective 
        solutions before reaching irreversible tipping points.
        
        Renewable energy adoption is increasing globally, with solar and wind 
        power becoming cost-competitive with fossil fuels. However, challenges 
        remain in energy storage, grid infrastructure, and policy coordination 
        between nations.
        
        The economic impact of climate change is already significant, with 
        extreme weather events causing billions in damages annually. Insurance 
        companies are adjusting their risk models, and investors are increasingly 
        considering climate factors in their decision-making.
        """
        
        print("Submitting news content for thematic analysis...")
        result = self.submit_analysis(news_content, "thematic")
        
        if result:
            print(f"Analysis submitted with ID: {result['analysis_id']}")
            print("Waiting for completion...")
            
            final_result = await self.wait_for_completion(result['analysis_id'])
            if final_result.get("status") == "completed":
                print("✓ News content thematic analysis completed!")
        
        # Example 4: Technical Documentation Summary
        print("\n4. TECHNICAL DOCUMENTATION SUMMARY")
        print("-" * 50)
        
        technical_content = """
        The Dapr Agents framework provides a powerful abstraction layer for 
        building intelligent, distributed applications. It integrates seamlessly 
        with Dapr's building blocks for state management, pub/sub messaging, 
        and workflow orchestration.
        
        Key features include:
        - LLM integration with multiple providers (OpenAI, Hugging Face, etc.)
        - Tool-based agent architecture with custom function calling
        - Built-in observability and tracing capabilities
        - Support for both stateless and durable agents
        - Workflow orchestration with LLM-based decision making
        
        The framework is designed for cloud-native applications and can be 
        deployed on Kubernetes or run locally with Docker. It supports 
        multiple programming languages and provides a consistent API across 
        different deployment environments.
        """
        
        print("Submitting technical content for summary analysis...")
        result = self.submit_analysis(technical_content, "summary")
        
        if result:
            print(f"Analysis submitted with ID: {result['analysis_id']}")
            print("Waiting for completion...")
            
            final_result = await self.wait_for_completion(result['analysis_id'])
            if final_result.get("status") == "completed":
                print("✓ Technical content summary analysis completed!")
        
        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED!")
        print("="*70)
        
        # List all jobs
        print("\nListing all analysis jobs...")
        try:
            response = requests.get(f"{self.base_url}/jobs", timeout=5)
            if response.status_code == 200:
                jobs = response.json()
                print(f"Total jobs: {jobs.get('total_jobs', 0)}")
                for job in jobs.get('jobs', []):
                    print(f"  - {job['analysis_id']}: {job['status']} ({job['analysis_type']})")
        except Exception as e:
            print(f"Error listing jobs: {e}")


async def main():
    """Main function to run the examples."""
    examples = ContentAnalysisExamples()
    await examples.run_examples()


if __name__ == "__main__":
    asyncio.run(main())
