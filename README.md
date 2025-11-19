# Hello watsonx + LangFlow 🚀

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IBM watsonx](https://img.shields.io/badge/IBM-watsonx.ai-blue)](https://www.ibm.com/watsonx)
[![LangFlow](https://img.shields.io/badge/LangFlow-Latest-green)](https://github.com/logspace-ai/langflow)

A production-ready starter template for building multi-agent AI workflows with **IBM watsonx.ai** and **LangFlow**. Features comprehensive documentation, cross-platform support, and modern Python tooling with UV package manager.

## 🎯 What is This?

This project demonstrates how to integrate **IBM watsonx.ai Granite models** with **LangFlow** for visual AI workflow building. It includes:

- 🎨 **Visual Flow Builder** - Build AI workflows with drag-and-drop
- 🤖 **Multi-Agent Support** - CrewAI integration examples  
- 🔧 **Production Ready** - Complete with Makefile, UV support, testing
- 📚 **Comprehensive Docs** - 2,000+ lines of documentation
- 🪟 **Cross-Platform** - Works on Linux, macOS, and Windows
- ⚡ **Modern Tooling** - UV package manager for 10-100x faster installs

## ✨ Features

-  **Native watsonx.ai Integration** - Direct connection to IBM Granite models
-  **Interactive Chat Demo** - Command-line interface with conversation history
-  **LangFlow Visual Builder** - Drag-and-drop workflow creation
-  **Environment Management** - Automated setup with Make or scripts
-  **Code Quality Tools** - Black, Ruff, mypy configured
-  **Windows Native** - First-class Windows support with run.bat
-  **UV Compatible** - Fast package installation and dependency management
-  **Complete Examples** - RAG, chatbots, multi-agent systems

## 📋 Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **IBM watsonx.ai account** ([Sign up](https://www.ibm.com/watsonx))
- **API Key** ([Get one](https://cloud.ibm.com/iam/apikeys))
- **Project ID** (From your watsonx.ai project settings)

### Optional (Recommended)
- **UV package manager** for faster installs ([Install UV](https://github.com/astral-sh/uv))
- **Make** for build automation (comes with most Unix systems)

## 🚀 Quick Start

### Method 1: Clone and Make (Unix/macOS/Linux)
```bash
# Clone the repository
git clone https://github.com/ruslanmv/hello-watsonx-langflow.git
cd hello-watsonx-langflow

# One-command setup
make install && make setup && make demo
```

### Method 2: Clone and Make (Windows with Git Bash)
```bash
# Clone the repository
git clone https://github.com/ruslanmv/hello-watsonx-langflow.git
cd hello-watsonx-langflow

# Same as Unix
make install && make setup && make demo
```

### Method 3: Windows Native (run.bat)
```cmd
REM Clone the repository
git clone https://github.com/ruslanmv/hello-watsonx-langflow.git
cd hello-watsonx-langflow

REM Setup and run
run.bat install
run.bat setup
run.bat demo
```

### Method 4: With UV (Fastest!)
```bash
# Clone the repository
git clone https://github.com/ruslanmv/hello-watsonx-langflow.git
cd hello-watsonx-langflow

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Super fast setup with UV
make install  # Automatically uses UV if available
make setup
make demo
```

## 🌐 Regional Endpoints

Choose the appropriate URL for your region:

| Region | URL |
|--------|-----|
| 🇺🇸 Dallas (US South) | `https://us-south.ml.cloud.ibm.com` |
| 🇩🇪 Frankfurt (EU) | `https://eu-de.ml.cloud.ibm.com` |
| 🇬🇧 London (UK) | `https://eu-gb.ml.cloud.ibm.com` |
| 🇯🇵 Tokyo (Japan) | `https://jp-tok.ml.cloud.ibm.com` |
| 🇦🇺 Sydney (Australia) | `https://au-syd.ml.cloud.ibm.com` |

## 📁 Project Structure
```
hello-watsonx-langflow/
├── 📄 Documentation (7 files)
│   ├── README.md                    # This file
│   ├── QUICKSTART.md                # 5-minute getting started
│   ├── WINDOWS_SETUP.md             # Complete Windows guide
│   ├── ENVIRONMENT_SETUP.md         # Environment configuration
│   ├── PROJECT_SUMMARY.md           # Project overview
│   └── UPDATE_SUMMARY.md            # Latest updates
│
├── 💻 Code (1 file)
│   └── agent_langflow.py            # Main demo application
│
├── 🔧 Scripts (2 files)
│   ├── run.sh                       # Unix/Linux/macOS script
│   └── run.bat                      # Windows batch script
│
├── ⚙️ Configuration (6 files)
│   ├── Makefile                     # Build automation (30+ commands)
│   ├── pyproject.toml               # Modern Python config
│   ├── setup.cfg                    # Additional config
│   ├── requirements.txt             # Dependencies
│   ├── .env.example                 # Environment template
│   └── .gitignore                   # Git ignore rules
```

## 🛠️ Available Commands

### Using Makefile (Unix/macOS/Linux/Windows with Git Bash)
```bash
# Installation & Setup
make install          # Install dependencies (auto-detects UV)
make install-dev      # Install with dev dependencies
make setup            # Interactive credential setup

# Running
make demo             # Run interactive chat demo
make simple           # Run simple demo
make ui               # Start LangFlow UI (http://localhost:7860)

# Development
make format           # Format code with Black
make lint             # Run linting (Ruff/flake8)
make type-check       # Type checking with mypy
make test             # Run tests
make check            # Run all quality checks

# Utilities
make clean            # Clean temporary files
make update           # Update dependencies
make show-env         # Show environment info
make help             # Show all commands
```

### Using run.sh (Unix/macOS/Linux)
```bash
./run.sh install      # Install dependencies
./run.sh setup        # Setup credentials
./run.sh demo         # Run demo
./run.sh ui           # Start LangFlow UI
./run.sh test         # Test connection
./run.sh help         # Show help
```

### Using run.bat (Windows)
```cmd
run.bat install       # Install dependencies
run.bat setup         # Setup credentials
run.bat demo          # Run demo
run.bat ui            # Start LangFlow UI
run.bat test          # Test connection
run.bat help          # Show help
```

## 💡 Usage Examples

### 1. Interactive Chat Demo

Start a conversation with watsonx.ai:
```bash
make demo
# or
python agent_langflow.py
```

**Available commands in chat:**
- `/help` - Show help
- `/clear` - Clear conversation history
- `/history` - Show conversation
- `/model` - Show model info
- `/exit` - Quit

### 2. Simple Stateless Demo

Run without conversation history:
```bash
make simple
# or
python agent_langflow.py --simple
```

### 3. LangFlow Visual Builder

Launch the visual workflow builder:
```bash
make ui
# or
langflow run
```

Then open http://localhost:7860 in your browser.

### 4. Custom Model

Use a different watsonx.ai model:
```bash
python agent_langflow.py --model ibm/granite-13b-instruct-v2
```

## 📊 Available watsonx.ai Models

| Model | Model ID | Size | Best For |
|-------|----------|------|----------|
| **Granite 3 8B** | `ibm/granite-3-8b-instruct` | 8B | ⭐ Balanced (Recommended) |
| Granite 3 2B | `ibm/granite-3-2b-instruct` | 2B | Fast, efficient |
| Granite 13B | `ibm/granite-13b-instruct-v2` | 13B | Complex tasks |
| Llama 3 70B | `meta-llama/llama-3-70b-instruct` | 70B | High capability |
| Llama 3 8B | `meta-llama/llama-3-8b-instruct` | 8B | Efficient |
| Mixtral 8x7B | `mistralai/mixtral-8x7b-instruct-v01` | 8x7B | Mixture of experts |

## 🎓 Learning Path

### For Beginners

1. **Start Here**: [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
2. **Environment Setup**: [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
3. **Windows Users**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
4. **Run Demo**: `make demo`

### For Intermediate Users

1. Read this README completely
2. Explore `make help` for all commands
3. Review `agent_langflow.py` source code
4. Try custom models and parameters
5. Build visual flows in LangFlow UI

### For Advanced Users

1. Study the [Makefile](Makefile) for build automation
2. Review [pyproject.toml](pyproject.toml) for tooling config
3. Extend with custom agents
4. Integrate with CrewAI
5. Build production deployments

## 🔧 LangFlow Integration Methods

### Method 1: Visual Builder (LangFlow UI)

1. **Start LangFlow UI:**
```bash
   make ui
```

2. **Create a New Flow:**
   - Click "New Flow"
   - Search for "ChatWatsonx" component
   - Drag it to the canvas

3. **Configure watsonx.ai:**
   - Model ID: `ibm/granite-3-8b-instruct`
   - API Key: Your watsonx.ai API key
   - URL: Your regional endpoint
   - Project ID: Your project ID

4. **Build and Test:**
   - Add components (prompts, parsers, etc.)
   - Connect them visually
   - Test in real-time

### Method 2: Python API (Programmatic)
```python
from langchain_ibm import ChatWatsonx
from langchain.schema import HumanMessage

# Initialize watsonx.ai
chat = ChatWatsonx(
    model_id="ibm/granite-3-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="your_project_id",
)

# Simple chat
response = chat.invoke([HumanMessage(content="Hello!")])
print(response.content)
```

See [agent_langflow.py](agent_langflow.py) for complete examples.

## 🔒 Security Best Practices

1. ✅ **Never commit credentials** to version control
2. ✅ **Use environment variables** (.env file)
3. ✅ **Rotate API keys** regularly
4. ✅ **Add .env to .gitignore** (already configured)
5. ✅ **Limit API key permissions** in IBM Cloud IAM
6. ✅ **Use separate keys** for dev/staging/production

### Setting Up Credentials

**Create .env file:**
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your favorite editor
```

**Required variables:**
```bash
WATSONX_API_KEY=your_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here
```

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>Python 3.11 not found</b></summary>

**Solution:**
```bash
# Check available Python versions
python --version
python3 --version
python3.11 --version

# Install Python 3.11
# Ubuntu/Debian:
sudo apt install python3.11

# macOS:
brew install python@3.11

# Windows:
# Download from https://www.python.org/downloads/
```
</details>

<details>
<summary><b>LangFlow won't start</b></summary>

**Solution:**
```bash
# Reinstall LangFlow
pip uninstall langflow
pip install langflow --upgrade

# Or with UV
uv pip install langflow --upgrade
```
</details>

<details>
<summary><b>watsonx.ai connection errors</b></summary>

**Solution:**
```bash
# Verify credentials
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key:', 'SET' if os.getenv('WATSONX_API_KEY') else 'MISSING')"

# Test connection
make test-connection
```
</details>

<details>
<summary><b>Port 7860 already in use</b></summary>

**Solution:**
```bash
# Use different port
langflow run --port 8080

# Or kill existing process
lsof -ti:7860 | xargs kill -9  # Unix/macOS
netstat -ano | findstr :7860    # Windows (find PID)
taskkill /PID <PID> /F          # Windows (kill process)
```
</details>

<details>
<summary><b>UV not installing packages</b></summary>

**Solution:**
```bash
# Upgrade UV
uv self update

# Clear cache
rm -rf ~/.cache/uv

# Reinstall
uv pip install -r requirements.txt --force-reinstall
```
</details>

See platform-specific guides for more help:
- **Windows**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **Environment**: [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)

## 📚 Documentation

### Complete Guides

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute getting started guide
- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Complete Windows setup (450+ lines)
- **[ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)** - Environment management (500+ lines)
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and statistics

### Code Documentation

- **[agent_langflow.py](agent_langflow.py)** - Well-commented main application
- **[Makefile](Makefile)** - Documented build automation
- **[pyproject.toml](pyproject.toml)** - Modern Python configuration

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/hello-watsonx-langflow.git
```

2. **Create a branch**
```bash
   git checkout -b feature/amazing-feature
```

3. **Make changes and test**
```bash
   make dev-setup  # Install dev dependencies
   make check      # Run all checks
```

4. **Commit and push**
```bash
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
```

5. **Open a Pull Request** on GitHub

### Development Setup
```bash
# Install with development dependencies
make dev-setup

# Run quality checks before committing
make format      # Format code
make lint        # Check style
make type-check  # Check types
make test        # Run tests
make check       # All checks
```

## 📊 Project Statistics

- **📁 Files**: 16 total
- **📝 Lines**: 4,000+ lines of code and documentation
- **📚 Documentation**: 2,500+ lines
- **🔧 Commands**: 30+ Makefile targets
- **🌍 Platforms**: Linux, macOS, Windows, WSL
- **🐍 Python**: 3.11+ required
- **⚡ Speed**: 10-100x faster with UV

## 🎯 Use Cases

### 1. Simple Chatbot
Build a basic chatbot with conversation memory.

### 2. RAG Pipeline
Create retrieval-augmented generation workflows visually.

### 3. Multi-Agent Systems
Integrate with CrewAI for collaborative agent workflows.

### 4. Document Processing
Build document analysis pipelines with vector stores.

### 5. Enterprise AI
Deploy production AI applications with watsonx.ai.

## 🚀 Next Steps

1. ✅ **Complete Quick Start** - Get the demo running
2. 🎨 **Explore LangFlow UI** - Build visual workflows
3. 🤖 **Try Different Models** - Experiment with Granite, Llama, Mixtral
4. 📊 **Build RAG Pipeline** - Add document retrieval
5. 🔧 **Create Custom Agents** - Extend with your own logic
6. 🚀 **Deploy to Production** - Use LangFlow's export features

## 📖 Additional Resources

### Official Documentation
- [LangFlow Documentation](https://docs.langflow.org/)
- [LangChain IBM Integration](https://python.langchain.com/docs/integrations/llms/ibm_watsonx)
- [IBM watsonx.ai Docs](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [UV Package Manager](https://github.com/astral-sh/uv)

### Tutorials
- [LangFlow Quickstart](https://docs.langflow.org/getting-started/quickstart)
- [watsonx.ai Getting Started](https://www.ibm.com/docs/en/watsonx/saas?topic=started-getting)
- [Building Multi-Agent Systems](https://docs.crewai.com/)

### Community
- [LangFlow GitHub](https://github.com/logspace-ai/langflow)
- [LangChain Community](https://github.com/langchain-ai/langchain)
- [IBM Developer](https://developer.ibm.com/components/watsonx-ai/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IBM watsonx.ai** - Enterprise AI platform with Granite foundation models
- **LangFlow** - Visual flow builder for LangChain applications
- **LangChain** - Framework for developing LLM applications
- **UV** - Ultra-fast Python package manager by Astral

## 💬 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/ruslanmv/hello-watsonx-langflow/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/ruslanmv/hello-watsonx-langflow/discussions)
- 📧 **Email**: [Contact](mailto:ruslanmv@example.com)

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=ruslanmv/hello-watsonx-langflow&type=Date)](https://star-history.com/#ruslanmv/hello-watsonx-langflow&Date)

---

**Built with ❤️ by [ruslanmv](https://github.com/ruslanmv)**

**Happy Building with watsonx.ai + LangFlow!** 🚀

---

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/ruslanmv/hello-watsonx-langflow?style=social)](https://github.com/ruslanmv/hello-watsonx-langflow/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ruslanmv/hello-watsonx-langflow?style=social)](https://github.com/ruslanmv/hello-watsonx-langflow/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/ruslanmv/hello-watsonx-langflow?style=social)](https://github.com/ruslanmv/hello-watsonx-langflow/watchers)

</div>