# Quick Start Guide

Get up and running with LangFlow + watsonx.ai in 5 minutes!

## 🚀 Super Quick Start

```bash
# 1. Install dependencies
./run.sh install

# 2. Setup credentials
./run.sh setup

# 3. Start chatting!
./run.sh demo
```

## 📋 Prerequisites

- Python 3.10+
- IBM watsonx.ai account ([Sign up](https://www.ibm.com/watsonx))
- API Key ([Get one](https://cloud.ibm.com/iam/apikeys))

## 🔑 Get Your Credentials

### 1. API Key
1. Go to [IBM Cloud IAM](https://cloud.ibm.com/iam/apikeys)
2. Click "Create +"
3. Name it and copy the key

### 2. Project ID
1. Go to [watsonx.ai](https://dataplatform.cloud.ibm.com/)
2. Open your project
3. Click "Manage" → "General"
4. Copy the Project ID

### 3. Choose Region

| Region | URL |
|--------|-----|
| 🇺🇸 Dallas | `https://us-south.ml.cloud.ibm.com` |
| 🇩🇪 Frankfurt | `https://eu-de.ml.cloud.ibm.com` |
| 🇬🇧 London | `https://eu-gb.ml.cloud.ibm.com` |

## 🎯 What You Can Do

### Interactive Chat
```bash
./run.sh demo
```

Start a conversation with watsonx.ai Granite models.

### Simple Test
```bash
./run.sh simple
```

Run automated test questions.

### Visual Builder
```bash
./run.sh ui
```

Launch LangFlow UI at `http://localhost:7860`

### Custom Model
```bash
python agent_langflow.py --model ibm/granite-13b-instruct-v2
```

## 📝 Manual Setup

If you prefer not to use the script:

1. **Install packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run the demo:**
   ```bash
   python agent_langflow.py
   ```

## 💬 Chat Commands

Once in the interactive demo:

| Command | Action |
|---------|--------|
| `/help` | Show help |
| `/clear` | Clear history |
| `/history` | Show conversation |
| `/model` | Show model info |
| `/exit` | Quit |

## 🎨 Using LangFlow UI

1. Start the UI: `./run.sh ui`
2. Open browser: `http://localhost:7860`
3. Create a new flow
4. Add components:
   - Search "ChatWatsonx"
   - Configure with your credentials
   - Connect components
5. Test in the UI!

## 🐛 Troubleshooting

### "Module not found"
```bash
./run.sh install
```

### "Missing credentials"
```bash
./run.sh setup
```

### "Port already in use"
```bash
# Kill existing process
lsof -ti:7860 | xargs kill -9

# Or use different port
langflow run --port 8080
```

### Connection errors
Check your `.env` file:
- API key is correct
- URL matches your region
- Project ID is from the right project

## 📚 Next Steps

1. ✅ Complete this quick start
2. 📖 Read the full [README.md](README.md)
3. 🎨 Explore LangFlow visual builder
4. 🚀 Build your own flows
5. 📦 Deploy to production

## 🆘 Need Help?

- Full docs: [README.md](README.md)
- LangFlow docs: https://docs.langflow.org/
- watsonx.ai docs: https://www.ibm.com/docs/en/watsonx-as-a-service

---

**Happy Building!** 🎉
