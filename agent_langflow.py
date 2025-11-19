#!/usr/bin/env python3
"""
LangFlow + IBM watsonx.ai Integration Demo

This script demonstrates how to use watsonx.ai with LangChain and LangFlow
for building AI-powered applications.

Features:
- Environment variable configuration
- watsonx.ai LLM integration
- Interactive chat interface
- Conversation history
- Error handling

Usage:
    python agent_langflow.py
    python agent_langflow.py --model ibm/granite-13b-instruct-v2
"""

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
from langchain_ibm import ChatWatsonx
from langchain.schema import HumanMessage, AIMessage, SystemMessage


# ============================================================================
# Configuration
# ============================================================================

def load_configuration():
    """Load configuration from environment variables."""
    load_dotenv()
    
    config = {
        'api_key': os.getenv('WATSONX_APIKEY'),
        'url': os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
        'project_id': os.getenv('WATSONX_PROJECT_ID'),
        'model_id': os.getenv('DEFAULT_MODEL', 'ibm/granite-3-8b-instruct'),
        'temperature': float(os.getenv('TEMPERATURE', '0.7')),
        'max_tokens': int(os.getenv('MAX_TOKENS', '1000')),
    }
    
    # Validate required fields
    missing = []
    if not config['api_key']:
        missing.append('WATSONX_APIKEY')
    if not config['project_id']:
        missing.append('WATSONX_PROJECT_ID')
    
    if missing:
        print("❌ Error: Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\n💡 Tip: Create a .env file with your credentials:")
        print("   WATSONX_APIKEY=your_api_key")
        print("   WATSONX_PROJECT_ID=your_project_id")
        sys.exit(1)
    
    return config


# ============================================================================
# watsonx.ai Chat Interface
# ============================================================================

class WatsonxChatBot:
    """Simple chatbot using watsonx.ai through LangChain."""
    
    def __init__(self, config: Dict):
        """Initialize the chatbot with watsonx.ai configuration."""
        self.config = config
        self.history: List = []
        
        print(f"🤖 Initializing watsonx.ai chatbot...")
        print(f"   Model: {config['model_id']}")
        print(f"   Temperature: {config['temperature']}")
        print(f"   URL: {config['url']}")
        
        try:
            self.chat = ChatWatsonx(
                model_id=config['model_id'],
                url=config['url'],
                project_id=config['project_id'],
                params={
                    'temperature': config['temperature'],
                    'max_tokens': config['max_tokens'],
                    'top_p': 1.0,
                }
            )
            print("✅ watsonx.ai connection established!\n")
        except Exception as e:
            print(f"❌ Error connecting to watsonx.ai: {e}")
            sys.exit(1)
    
    def add_system_message(self, content: str):
        """Add a system message to set context."""
        self.history.append(SystemMessage(content=content))
    
    def chat_with_history(self, user_input: str) -> str:
        """
        Send a message and get a response, maintaining conversation history.
        
        Args:
            user_input: The user's message
            
        Returns:
            The AI's response
        """
        # Add user message to history
        self.history.append(HumanMessage(content=user_input))
        
        try:
            # Get response from watsonx.ai
            response = self.chat.invoke(self.history)
            
            # Add AI response to history
            self.history.append(AIMessage(content=response.content))
            
            return response.content
        
        except Exception as e:
            error_msg = f"Error getting response: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def chat_simple(self, user_input: str) -> str:
        """
        Send a message without maintaining history (stateless).
        
        Args:
            user_input: The user's message
            
        Returns:
            The AI's response
        """
        try:
            response = self.chat.invoke([HumanMessage(content=user_input)])
            return response.content
        except Exception as e:
            return f"Error: {e}"
    
    def clear_history(self):
        """Clear conversation history."""
        self.history.clear()
        print("🔄 Conversation history cleared.")


# ============================================================================
# Interactive Demo
# ============================================================================

def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("  LangFlow + IBM watsonx.ai Demo")
    print("  Interactive Chat Interface")
    print("=" * 70)
    print()


def print_help():
    """Print help message."""
    print("\n📖 Available Commands:")
    print("   /help      - Show this help message")
    print("   /clear     - Clear conversation history")
    print("   /history   - Show conversation history")
    print("   /model     - Show current model info")
    print("   /exit      - Exit the application")
    print()


def show_history(bot: WatsonxChatBot):
    """Display conversation history."""
    if not bot.history:
        print("\n📭 No conversation history yet.")
        return
    
    print("\n" + "=" * 70)
    print("📜 Conversation History")
    print("=" * 70)
    
    for i, msg in enumerate(bot.history, 1):
        role = "System" if isinstance(msg, SystemMessage) else \
               "You" if isinstance(msg, HumanMessage) else "AI"
        print(f"\n[{i}] {role}:")
        print(f"    {msg.content}")
    
    print("=" * 70)


def show_model_info(config: Dict):
    """Display current model configuration."""
    print("\n" + "=" * 70)
    print("🤖 Current Model Configuration")
    print("=" * 70)
    print(f"Model ID: {config['model_id']}")
    print(f"Temperature: {config['temperature']}")
    print(f"Max Tokens: {config['max_tokens']}")
    print(f"URL: {config['url']}")
    print("=" * 70)


def interactive_demo():
    """Run the interactive chat demo."""
    print_banner()
    
    # Load configuration
    config = load_configuration()
    
    # Initialize chatbot
    bot = WatsonxChatBot(config)
    
    # Set initial system message
    bot.add_system_message(
        "You are a helpful AI assistant powered by IBM watsonx.ai. "
        "You provide clear, concise, and accurate responses. "
        "You are friendly and professional."
    )
    
    print("💬 Chat Interface Ready!")
    print("   Type your message and press Enter.")
    print("   Type /help for available commands.")
    print("   Type /exit to quit.")
    print()
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == '/exit':
                print("\n👋 Goodbye! Thanks for using watsonx.ai!")
                break
            
            elif user_input.lower() == '/help':
                print_help()
                continue
            
            elif user_input.lower() == '/clear':
                bot.clear_history()
                bot.add_system_message(
                    "You are a helpful AI assistant powered by IBM watsonx.ai."
                )
                continue
            
            elif user_input.lower() == '/history':
                show_history(bot)
                continue
            
            elif user_input.lower() == '/model':
                show_model_info(config)
                continue
            
            # Get AI response
            print("\nAI: ", end="", flush=True)
            response = bot.chat_with_history(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using watsonx.ai!")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Type /exit to quit or continue chatting.\n")


# ============================================================================
# Simple Demo (Non-Interactive)
# ============================================================================

def simple_demo():
    """Run a simple non-interactive demo."""
    print_banner()
    
    config = load_configuration()
    bot = WatsonxChatBot(config)
    
    print("🧪 Running Simple Demo...\n")
    
    # Test questions
    questions = [
        "What is IBM watsonx.ai?",
        "Explain the benefits of using AI in business.",
        "What are foundation models?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n[Question {i}]")
        print(f"You: {question}")
        print("\nAI: ", end="", flush=True)
        
        response = bot.chat_simple(question)
        print(response)
        print("\n" + "-" * 70)
    
    print("\n✅ Demo complete!")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='LangFlow + watsonx.ai Demo Application'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='Model ID to use (overrides environment variable)'
    )
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Run simple demo instead of interactive chat'
    )
    parser.add_argument(
        '--temperature',
        type=float,
        help='Temperature for model (0.0-1.0)'
    )
    
    args = parser.parse_args()
    
    # Override environment variables if specified
    if args.model:
        os.environ['DEFAULT_MODEL'] = args.model
    if args.temperature is not None:
        os.environ['TEMPERATURE'] = str(args.temperature)
    
    # Run appropriate demo
    if args.simple:
        simple_demo()
    else:
        interactive_demo()


if __name__ == '__main__':
    main()
