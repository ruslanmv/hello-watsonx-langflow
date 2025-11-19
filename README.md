# LangFlow + IBM watsonx.ai Integration Demo

This demo shows how to integrate **IBM watsonx.ai** with **LangFlow** for visual AI workflow building.

## 🎯 What is LangFlow?

LangFlow is a visual UI tool for building LangChain flows through drag-and-drop components. It provides:

- 🎨 **Visual Flow Builder** - Drag-and-drop interface
- 🔧 **Component Library** - Pre-built LangChain components
- 🔗 **Easy Integration** - Connect various AI services
- 🚀 **Rapid Prototyping** - Build AI workflows quickly
- 📊 **Real-time Testing** - Test flows interactively

## 📋 Prerequisites

- Python 3.10+
- IBM Cloud account with watsonx.ai access
- watsonx.ai API key and Project ID
- Basic understanding of LLMs and chat interfaces

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install langflow langchain-ibm python-dotenv
```

Or use the provided script:

```bash
./run.sh install
```

### 2. Configure Credentials

Create a `.env` file with your watsonx.ai credentials:

```bash
# .env file
WATSONX_APIKEY=your_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here
```

**Get your credentials:**
- API Key: [IBM Cloud IAM](https://cloud.ibm.com/iam/apikeys)
- Project ID: From your watsonx.ai project settings
- URL: Based on your region (see below)

### 3. Run the Demo

```bash
./run.sh demo
```

Or run the Python script directly:

```bash
python agent_langflow.py
```

### 4. Launch LangFlow UI

```bash
./run.sh ui
```

Or manually:

```bash
langflow run
```

This will start the LangFlow UI at `http://localhost:7860`

## 🌐 Regional Endpoints

Choose the appropriate URL for your region:

| Region | URL |
|--------|-----|
| Dallas (US South) | `https://us-south.ml.cloud.ibm.com` |
| Frankfurt (EU) | `https://eu-de.ml.cloud.ibm.com` |
| London (UK) | `https://eu-gb.ml.cloud.ibm.com` |
| Tokyo (Japan) | `https://jp-tok.ml.cloud.ibm.com` |
| Sydney (Australia) | `https://au-syd.ml.cloud.ibm.com` |

## 📁 Project Structure

```
agent_langflow/
├── README.md              # This file
├── agent_langflow.py      # Main demo application
├── run.sh                 # Convenience script
├── .env.example           # Example environment file
└── flows/                 # LangFlow flow definitions (optional)
```

## 🔧 Using LangFlow with watsonx.ai

### Method 1: Visual Builder (LangFlow UI)

1. **Start LangFlow UI:**
   ```bash
   langflow run
   ```

2. **Create a New Flow:**
   - Click "New Flow"
   - Search for "ChatWatsonx" component
   - Drag it to the canvas

3. **Configure watsonx.ai:**
   - Set Model ID: `ibm/granite-3-8b-instruct`
   - Set API Key: Your watsonx.ai API key
   - Set URL: Your regional endpoint
   - Set Project ID: Your project ID

4. **Build Your Flow:**
   - Add prompt templates
   - Add output parsers
   - Connect components
   - Test in the UI

### Method 2: Python API (Programmatic)

See `agent_langflow.py` for a complete example of using LangFlow programmatically.

## 💡 Demo Application Features

The `agent_langflow.py` demo includes:

- ✅ Environment variable configuration
- ✅ watsonx.ai LLM setup
- ✅ Simple chat interface
- ✅ Conversation history
- ✅ Error handling
- ✅ Interactive CLI

## 🎓 Example Use Cases

### 1. Simple Chatbot

```python
from langchain_ibm import ChatWatsonx
from langchain.schema import HumanMessage

chat = ChatWatsonx(
    model_id="ibm/granite-3-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="your_project_id",
)

response = chat.invoke([HumanMessage(content="Hello!")])
print(response.content)
```

### 2. Chain with Prompt Template

```python
from langchain_ibm import ChatWatsonx
from langchain.prompts import ChatPromptTemplate

chat = ChatWatsonx(...)
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. {input}"
)
chain = prompt | chat
result = chain.invoke({"input": "Explain AI"})
```

### 3. RAG Pipeline (Visual in LangFlow)

Build in LangFlow UI:
```
[Document Loader] → [Text Splitter] → [Embeddings] → [Vector Store]
                                                           ↓
[User Question] → [Prompt Template] → [ChatWatsonx] → [Output Parser]
                         ↑
                   [Retrieved Context]
```

## 🛠️ Available Scripts

### Installation
```bash
./run.sh install       # Install dependencies
```

### Running
```bash
./run.sh demo          # Run Python demo
./run.sh ui            # Start LangFlow UI
./run.sh help          # Show help message
```

### Manual Commands
```bash
# Run demo with custom model
python agent_langflow.py --model ibm/granite-13b-instruct-v2

# Start LangFlow with custom port
langflow run --port 8080

# Export a flow
langflow export MyFlow --output my_flow.json
```

## 📊 Available watsonx.ai Models

| Model | Model ID | Best For |
|-------|----------|----------|
| Granite 3 8B | `ibm/granite-3-8b-instruct` | Balanced performance |
| Granite 3 2B | `ibm/granite-3-2b-instruct` | Fast, efficient |
| Granite 13B | `ibm/granite-13b-instruct-v2` | Complex tasks |
| Llama 3 70B | `meta-llama/llama-3-70b-instruct` | High capability |
| Llama 3 8B | `meta-llama/llama-3-8b-instruct` | Efficient |
| Mixtral 8x7B | `mistralai/mixtral-8x7b-instruct-v01` | Mixture of experts |

## 🔒 Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Rotate API keys** regularly
4. **Use .gitignore** for `.env` files
5. **Limit API key permissions** in IBM Cloud

## 🐛 Troubleshooting

### LangFlow won't start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall LangFlow
pip uninstall langflow
pip install langflow --upgrade
```

### watsonx.ai connection errors

```bash
# Verify credentials
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', 'SET' if os.getenv('WATSONX_APIKEY') else 'MISSING')"

# Test connection
python agent_langflow.py
```

### Port already in use

```bash
# Use different port
langflow run --port 8080

# Or kill existing process
lsof -ti:7860 | xargs kill -9
```

## 📚 Additional Resources

### Official Documentation
- [LangFlow Documentation](https://docs.langflow.org/)
- [LangChain IBM Integration](https://python.langchain.com/docs/integrations/llms/ibm_watsonx)
- [IBM watsonx.ai Docs](https://www.ibm.com/docs/en/watsonx-as-a-service)

### Tutorials
- [LangFlow Quickstart](https://docs.langflow.org/getting-started/quickstart)
- [watsonx.ai Getting Started](https://www.ibm.com/docs/en/watsonx/saas?topic=started-getting)

### Community
- [LangFlow GitHub](https://github.com/logspace-ai/langflow)
- [LangChain Community](https://github.com/langchain-ai/langchain)

## 🚀 Next Steps

1. **Explore LangFlow UI** - Build visual flows
2. **Try Different Models** - Experiment with Granite, Llama, Mixtral
3. **Build RAG Pipeline** - Add document retrieval
4. **Create Custom Components** - Extend LangFlow
5. **Deploy to Production** - Use LangFlow's export features

## 📝 Example .env File

Create a `.env` file in this directory:

```bash
# IBM watsonx.ai Configuration
WATSONX_APIKEY=your_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here

# Optional: Model Configuration
DEFAULT_MODEL=ibm/granite-3-8b-instruct
TEMPERATURE=0.7
MAX_TOKENS=1000

# Optional: LangFlow Configuration
LANGFLOW_PORT=7860
LANGFLOW_HOST=0.0.0.0
```

## 🤝 Contributing

Feel free to enhance this demo:
- Add new flow examples
- Improve error handling
- Add more use cases
- Update documentation

## 📄 License

This demo is provided as-is for educational purposes.

## 🙏 Acknowledgments

- **IBM watsonx.ai** - Enterprise AI platform
- **LangFlow** - Visual flow builder for LangChain
- **LangChain** - Framework for LLM applications

---

**Happy Building with LangFlow + watsonx.ai!** 🚀

For questions or issues, refer to the official documentation or open an issue in your project repository.
