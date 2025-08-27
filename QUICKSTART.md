# Content Analysis Agent - Quick Start Guide

Get up and running with the Content Analysis Agent in minutes!

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Dapr CLI installed
- OpenAI API key

### 2. Setup
```bash
# Clone or navigate to the content-analysis-agent directory
cd content-analysis-agent

# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. Start the Service
```bash
# Make startup script executable (if needed)
chmod +x start_service.sh

# Start the service
./start_service.sh
```

The service will start on port 8005 with Dapr integration.

### 4. Test the Agent

#### Option A: Direct Demo (No HTTP)
```bash
python demo_agent.py
```

#### Option B: HTTP Client Demo
```bash
python services/client/http_client.py
```

#### Option C: Comprehensive Examples
```bash
python examples/example_usage.py
```

## 🔧 API Endpoints

Once running, the service provides these endpoints:

- `GET /status` - Health check
- `POST /analyze` - Submit content for analysis
- `GET /analysis/{id}` - Get analysis results
- `GET /jobs` - List all analysis jobs

## 📝 Example Usage

### Submit Content for Analysis
```bash
curl -X POST http://localhost:8005/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your text content here",
    "analysis_type": "comprehensive"
  }'
```

### Check Analysis Status
```bash
curl http://localhost:8005/analysis/{analysis_id}
```

## 🎯 Analysis Types

- **comprehensive** - Full analysis with themes, sentiment, summary, and recommendations
- **thematic** - Focus on key themes and topics
- **sentiment** - Emotional tone and sentiment analysis
- **summary** - Concise content summary

## 🏗️ Architecture

The agent demonstrates:
- **LLM Integration** with OpenAI GPT models
- **Custom Tools** for different analysis types
- **Durable Agent** with state persistence
- **HTTP API** for easy integration
- **Dapr Integration** for distributed systems

## 🐛 Troubleshooting

### Common Issues

1. **Service won't start**
   - Check if Dapr is installed: `dapr --version`
   - Ensure Redis is running: `redis-cli ping`

2. **Analysis fails**
   - Verify OpenAI API key in `.env`
   - Check service logs for errors

3. **Port conflicts**
   - Change port in `start_service.sh` and `app.py`
   - Update client URLs accordingly

### Logs
Check the service output for detailed logs and error messages.

## 🔍 What's Next?

- Try different content types and analysis modes
- Integrate with your own applications
- Extend the agent with custom tools
- Deploy to Kubernetes with the provided manifests

## 📚 Learn More

- [Dapr Agents Documentation](https://docs.dapr.io/concepts/dapr-agents/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Dapr Building Blocks](https://docs.dapr.io/concepts/building-blocks-concept/)

---

**Happy Analyzing! 🎉**
