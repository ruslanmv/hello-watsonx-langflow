#!/bin/bash

# ============================================================================
# LangFlow + watsonx.ai Demo Runner Script
# ============================================================================
# 
# This script provides convenient commands for running the LangFlow demo.
#
# Usage:
#   ./run.sh install    - Install dependencies
#   ./run.sh demo       - Run interactive demo
#   ./run.sh simple     - Run simple demo
#   ./run.sh ui         - Start LangFlow UI
#   ./run.sh setup      - Setup environment
#   ./run.sh test       - Test connection
#   ./run.sh help       - Show help
#
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# ============================================================================
# Installation
# ============================================================================

install_dependencies() {
    print_header "Installing Dependencies"
    
    echo "Installing Python packages..."
    pip install langflow langchain-ibm python-dotenv
    
    print_success "Dependencies installed successfully!"
    echo ""
    print_info "Installed packages:"
    echo "  - langflow (Visual flow builder)"
    echo "  - langchain-ibm (watsonx.ai integration)"
    echo "  - python-dotenv (Environment variables)"
}

# ============================================================================
# Environment Setup
# ============================================================================

setup_environment() {
    print_header "Environment Setup"
    
    if [ -f .env ]; then
        print_info ".env file already exists."
        read -p "Do you want to overwrite it? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Keeping existing .env file."
            return
        fi
    fi
    
    echo "Creating .env file..."
    echo ""
    
    # Get credentials from user
    read -p "Enter your watsonx.ai API Key: " api_key
    read -p "Enter your watsonx.ai Project ID: " project_id
    
    # Default URL
    echo ""
    echo "Select your region:"
    echo "  1) US South (Dallas) - https://us-south.ml.cloud.ibm.com"
    echo "  2) EU (Frankfurt) - https://eu-de.ml.cloud.ibm.com"
    echo "  3) UK (London) - https://eu-gb.ml.cloud.ibm.com"
    echo "  4) Japan (Tokyo) - https://jp-tok.ml.cloud.ibm.com"
    echo "  5) Australia (Sydney) - https://au-syd.ml.cloud.ibm.com"
    read -p "Enter choice (1-5) [1]: " region_choice
    
    case ${region_choice:-1} in
        1) url="https://us-south.ml.cloud.ibm.com" ;;
        2) url="https://eu-de.ml.cloud.ibm.com" ;;
        3) url="https://eu-gb.ml.cloud.ibm.com" ;;
        4) url="https://jp-tok.ml.cloud.ibm.com" ;;
        5) url="https://au-syd.ml.cloud.ibm.com" ;;
        *) url="https://us-south.ml.cloud.ibm.com" ;;
    esac
    
    # Create .env file
    cat > .env << EOF
# IBM watsonx.ai Configuration
WATSONX_APIKEY=${api_key}
WATSONX_URL=${url}
WATSONX_PROJECT_ID=${project_id}

# Optional: Model Configuration
DEFAULT_MODEL=ibm/granite-3-8b-instruct
TEMPERATURE=0.7
MAX_TOKENS=1000

# Optional: LangFlow Configuration
LANGFLOW_PORT=7860
LANGFLOW_HOST=0.0.0.0
EOF
    
    print_success ".env file created successfully!"
    echo ""
    print_info "Your credentials have been saved to .env"
    print_info "Remember to add .env to your .gitignore!"
}

# ============================================================================
# Testing
# ============================================================================

test_connection() {
    print_header "Testing watsonx.ai Connection"
    
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo "Run: ./run.sh setup"
        exit 1
    fi
    
    echo "Testing connection to watsonx.ai..."
    python agent_langflow.py --simple
}

# ============================================================================
# Running Applications
# ============================================================================

run_demo() {
    print_header "Running Interactive Demo"
    
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo "Run: ./run.sh setup"
        exit 1
    fi
    
    python agent_langflow.py
}

run_simple_demo() {
    print_header "Running Simple Demo"
    
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo "Run: ./run.sh setup"
        exit 1
    fi
    
    python agent_langflow.py --simple
}

run_ui() {
    print_header "Starting LangFlow UI"
    
    print_info "LangFlow UI will start at http://localhost:7860"
    print_info "Press Ctrl+C to stop the server"
    echo ""
    
    # Check if custom port is specified in .env
    if [ -f .env ]; then
        source .env
        if [ ! -z "$LANGFLOW_PORT" ]; then
            echo "Starting on port $LANGFLOW_PORT..."
            langflow run --port $LANGFLOW_PORT --host ${LANGFLOW_HOST:-0.0.0.0}
        else
            langflow run
        fi
    else
        langflow run
    fi
}

# ============================================================================
# Help
# ============================================================================

show_help() {
    cat << EOF
${BLUE}============================================================================
  LangFlow + watsonx.ai Demo - Command Reference
============================================================================${NC}

${GREEN}Installation Commands:${NC}
  ./run.sh install      Install all required dependencies
  ./run.sh setup        Setup environment variables (.env file)

${GREEN}Running Applications:${NC}
  ./run.sh demo         Run interactive chat demo
  ./run.sh simple       Run simple non-interactive demo
  ./run.sh ui           Start LangFlow UI (http://localhost:7860)

${GREEN}Testing:${NC}
  ./run.sh test         Test watsonx.ai connection

${GREEN}Utility:${NC}
  ./run.sh help         Show this help message
  ./run.sh version      Show version information

${YELLOW}Quick Start:${NC}
  1. ./run.sh install   # Install dependencies
  2. ./run.sh setup     # Configure credentials
  3. ./run.sh demo      # Start chatting!

${YELLOW}Examples:${NC}
  # Full setup from scratch
  ./run.sh install && ./run.sh setup && ./run.sh demo
  
  # Quick test
  ./run.sh test
  
  # Start visual builder
  ./run.sh ui
  
  # Run with custom model
  python agent_langflow.py --model ibm/granite-13b-instruct-v2

${YELLOW}Environment Variables (.env):${NC}
  WATSONX_APIKEY       Your IBM Cloud API key
  WATSONX_URL           Regional endpoint URL
  WATSONX_PROJECT_ID    Your watsonx.ai project ID
  DEFAULT_MODEL         Model to use (default: granite-3-8b-instruct)
  TEMPERATURE           Model temperature (default: 0.7)
  MAX_TOKENS            Max tokens in response (default: 1000)

${YELLOW}Need Help?${NC}
  - Check README.md for detailed documentation
  - Visit: https://docs.langflow.org/
  - Visit: https://www.ibm.com/docs/en/watsonx-as-a-service

${BLUE}============================================================================${NC}
EOF
}

show_version() {
    print_header "Version Information"
    
    echo "Python version:"
    python --version
    echo ""
    
    echo "Checking installed packages..."
    pip show langflow 2>/dev/null | grep "Name\|Version" || echo "LangFlow: Not installed"
    pip show langchain-ibm 2>/dev/null | grep "Name\|Version" || echo "langchain-ibm: Not installed"
    pip show python-dotenv 2>/dev/null | grep "Name\|Version" || echo "python-dotenv: Not installed"
}

# ============================================================================
# Main Script Logic
# ============================================================================

main() {
    case "${1:-help}" in
        install)
            install_dependencies
            ;;
        setup)
            setup_environment
            ;;
        demo)
            run_demo
            ;;
        simple)
            run_simple_demo
            ;;
        ui)
            run_ui
            ;;
        test)
            test_connection
            ;;
        version)
            show_version
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
