#!/bin/bash

# Universal CrewAI Flow Generator - Full Stack Launcher
# Starts both Backend (FastAPI) and Frontend (React)

set -e

echo "======================================================"
echo "  Universal CrewAI Flow Generator"
echo "  Full Stack Application Launcher"
echo "======================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Setting up Backend...${NC}"
cd backend

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Start backend in background
echo -e "${BLUE}Step 2: Starting Backend (Port 8095)...${NC}"
python main.py &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 3

cd ../frontend

echo -e "${BLUE}Step 3: Setting up Frontend...${NC}"

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Start frontend
echo -e "${BLUE}Step 4: Starting Frontend (Port 5173)...${NC}"
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

echo "======================================================"
echo -e "${GREEN}  Application is running!${NC}"
echo "======================================================"
echo ""
echo "  Backend:  http://localhost:8095"
echo "  Frontend: http://localhost:5173"
echo ""
echo "  Press Ctrl+C to stop both services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "Services stopped."
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for processes
wait
