# Content Analysis Agent

This quickstart demonstrates a powerful Content Analysis Agent that showcases the strength of Dapr Agents with LLM capabilities. The agent can analyze text content, extract insights, identify key themes, and provide actionable recommendations.

## Features

- **Content Analysis**: Deep analysis of text content using LLM capabilities
- **Theme Extraction**: Identifies key themes and topics
- **Sentiment Analysis**: Analyzes emotional tone and sentiment
- **Recommendation Engine**: Provides actionable insights and suggestions
- **HTTP Trigger**: Waits for HTTP messages to trigger analysis jobs
- **Observability**: Built-in tracing and monitoring capabilities
- **Scalable**: Built on Dapr's distributed architecture

## Prerequisites

- Python 3.10 (recommended)
- pip package manager
- OpenAI API key
- Dapr CLI and Docker installed

## Environment Setup

```bash
# Create a virtual environment
python3.10 -m venv .venv

# Activate the virtual environment 
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file for your API keys:

```env
OPENAI_API_KEY=your_api_key_here
```

2. Make sure Dapr is initialized on your system:

```bash
dapr init
```

## Project Structure

```
components/                    # Dapr configuration files
├── pubsub.yaml               # Pub/Sub configuration
├── statestore.yaml           # State store configuration
└── workflowstate.yaml        # Workflow state configuration
services/                     # Directory for agent services
├── content-analyzer/         # Main content analysis agent
│   └── app.py               # FastAPI app for content analyzer
└── client/                   # HTTP client for triggering jobs
    └── http_client.py        # Client to trigger analysis jobs
dapr.yaml                     # Multi-App Run Template
```

## Usage

### 1. Start the Content Analysis Agent

```bash
# Start the agent service
dapr run --app-id content-analyzer --app-port 8005 --dapr-http-port 3505 -- python services/content-analyzer/app.py
```

### 2. Trigger Analysis Jobs

Use the HTTP client to trigger content analysis:

```bash
python services/client/http_client.py
```

Or send HTTP requests directly:

```bash
# Health check
curl http://localhost:8005/status

# Start analysis job
curl -X POST http://localhost:8005/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your text content here for analysis",
    "analysis_type": "comprehensive"
  }'
```

## Analysis Types

The agent supports different types of analysis:

- **comprehensive**: Full analysis with themes, sentiment, and recommendations
- **thematic**: Focus on key themes and topics
- **sentiment**: Emotional tone and sentiment analysis
- **summary**: Concise summary of content

## Example Output

```json
{
  "analysis_id": "uuid-here",
  "status": "completed",
  "results": {
    "themes": ["technology", "innovation", "future"],
    "sentiment": "positive",
    "confidence": 0.92,
    "summary": "The content discusses technological innovation...",
    "recommendations": [
      "Consider exploring emerging technologies",
      "Focus on sustainable innovation practices"
    ]
  }
}
```

## Architecture

The Content Analysis Agent demonstrates:

- **LLM Integration**: Uses OpenAI's GPT models for intelligent analysis
- **Tool-based Processing**: Custom tools for different analysis types
- **State Management**: Persistent state storage for job tracking
- **Event-driven**: HTTP-triggered job processing
- **Scalable**: Can handle multiple concurrent analysis requests
- **Observable**: Built-in tracing and monitoring

## Next Steps

- Add more analysis tools and capabilities
- Implement batch processing for multiple documents
- Add support for different content types (PDF, images, etc.)
- Integrate with external data sources for enhanced analysis
