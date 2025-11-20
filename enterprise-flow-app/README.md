# Universal CrewAI Flow Generator

**Enterprise Full-Stack Web Application**

A professional web application that guides users through creating CrewAI workflows for Langflow, combining IBM Watsonx-style configuration with an intuitive chat interface.

## Architecture

### Backend (FastAPI - Port 8095)
- **Framework:** FastAPI with async support
- **Language:** Python 3.8+
- **Core Logic:** Flow compiler that generates Langflow JSON
- **API Endpoints:**
  - `GET /api/health` - Health check
  - `POST /api/compile` - Compile flow configuration
  - `POST /api/download` - Download compiled flow

### Frontend (React + TypeScript - Port 5173)
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Design:** Professional IBM/Anthropic-inspired UI
- **Key Features:**
  - Claude-style chat interface
  - Live configuration preview sidebar
  - Real-time validation

## Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git**

### Installation & Running

1. **Clone the repository:**
```bash
cd enterprise-flow-app
```

2. **Run the application:**
```bash
./run_suite.sh
```

This script will:
- Set up Python virtual environment
- Install backend dependencies
- Start FastAPI backend on port 8095
- Install frontend dependencies
- Start React frontend on port 5173

3. **Access the application:**
- Open your browser to: `http://localhost:5173`

### Manual Setup (Alternative)

If you prefer to run services separately:

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## User Guide

### Building Your Flow

1. **Start the Conversation:**
   - The Flow Architect chatbot will greet you
   - Follow the guided conversation to define your agents

2. **Define Agents:**
   - Provide a **role** (e.g., "Security Analyst")
   - Specify the agent's **goal**
   - Add a **backstory** for context
   - Choose **tools** (filesystem, web search, or none)

3. **Define Tasks:**
   - Describe what the agent should do
   - Specify the expected output format

4. **Continue or Finish:**
   - Add more agents and tasks as needed
   - When done, click "Download Flow" in the sidebar

5. **Import to Langflow:**
   - Open Langflow in your browser
   - Click "Import" and select your downloaded JSON
   - Your flow is ready to run!

## Project Structure

```
enterprise-flow-app/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # API Pydantic models
│   ├── requirements.txt        # Python dependencies
│   └── src/                    # Generator logic
│       ├── __init__.py
│       ├── schemas.py          # Langflow schemas
│       ├── tool_builder.py     # Tool node generation
│       ├── crew_builder.py     # Agent/Task generation
│       ├── layout_engine.py    # Grid layout system
│       └── compiler.py         # Main compiler
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx    # Chat UI
│   │   │   ├── LivePreview.tsx      # Sidebar
│   │   │   └── Header.tsx           # Header
│   │   ├── api/
│   │   │   └── client.ts            # API client
│   │   ├── App.tsx                  # Main app
│   │   ├── main.tsx                 # Entry point
│   │   └── index.css                # Styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── run_suite.sh                # Launcher script
└── README.md
```

## API Documentation

### POST /api/compile

Compile a flow configuration into Langflow JSON.

**Request Body:**
```json
{
  "tools": [
    {
      "id": "mcp-filesystem",
      "type": "mcp",
      "name": "Filesystem MCP",
      "description": "File access",
      "config": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/var/logs"]
      }
    }
  ],
  "agents": [
    {
      "id": "agent_security",
      "role": "Security Analyst",
      "goal": "Analyze logs",
      "backstory": "Expert analyst",
      "llm_provider": "watsonx",
      "tools": ["mcp-filesystem"]
    }
  ],
  "tasks": [
    {
      "id": "task_scan",
      "description": "Scan logs for issues",
      "expected_output": "Report of findings",
      "assigned_agent": "agent_security"
    }
  ],
  "crew_name": "Security Crew",
  "process": "sequential"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Flow compiled successfully",
  "flow": { /* Langflow JSON */ },
  "stats": {
    "tools": 1,
    "agents": 1,
    "tasks": 1,
    "crews": 1,
    "edges": 3,
    "total_nodes": 4
  }
}
```

### POST /api/download

Download the compiled flow as a JSON file.

**Request:** Same as `/api/compile`

**Response:** File download (application/json)

## Features

### Backend Features
- ✅ FastAPI with async support
- ✅ CORS enabled for frontend
- ✅ Pydantic validation
- ✅ MCP Server support
- ✅ Custom tool support
- ✅ Automatic edge generation
- ✅ Grid-based layout system
- ✅ Configuration validation

### Frontend Features
- ✅ Conversational UI (Claude-style)
- ✅ Real-time state updates
- ✅ Live configuration preview
- ✅ Visual validation feedback
- ✅ One-click download
- ✅ Professional enterprise design
- ✅ Responsive layout
- ✅ TypeScript type safety

## Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **PyYAML** - YAML processing

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## Development

### Backend Development

**Run with auto-reload:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8095
```

**Run tests:**
```bash
pytest
```

### Frontend Development

**Run development server:**
```bash
cd frontend
npm run dev
```

**Build for production:**
```bash
npm run build
```

**Preview production build:**
```bash
npm run preview
```

## Configuration

### Backend Port
Default: 8095

Change in `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8095)
```

### Frontend Port
Default: 5173

Change in `frontend/vite.config.ts`:
```typescript
server: {
  port: 5173
}
```

### CORS Settings
Configure allowed origins in `backend/main.py`:
```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

## Troubleshooting

### Backend won't start
- Check if port 8095 is available: `lsof -i :8095`
- Verify Python version: `python3 --version` (should be 3.8+)
- Check virtual environment is activated

### Frontend won't start
- Check if port 5173 is available: `lsof -i :5173`
- Verify Node.js version: `node --version` (should be 16+)
- Try deleting `node_modules` and running `npm install` again

### CORS errors
- Ensure backend is running before frontend
- Check CORS configuration in `backend/main.py`
- Verify API calls use correct base URL

### Download not working
- Check browser console for errors
- Verify backend `/api/download` endpoint is accessible
- Ensure configuration is valid (at least 1 agent and 1 task)

## Deployment

### Backend Deployment
```bash
# Using Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8095
```

### Frontend Deployment
```bash
# Build
npm run build

# Deploy dist/ folder to your hosting service
```

## License

Enterprise AI Architecture - Internal Use

## Authors

- **Backend:** Principal AI Architect
- **Frontend:** Full-Stack Developer
- **Architecture:** Enterprise AI Team

## Support

For issues and questions, please contact your enterprise AI team or create an issue in the repository.

---

**Powered by IBM Watsonx + Langflow**
