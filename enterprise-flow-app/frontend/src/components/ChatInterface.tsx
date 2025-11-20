/**
 * Chat Interface Component
 * Claude-style chatbot that guides users through building their flow
 */

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { ToolConfig, AgentConfig, TaskConfig } from '../api/client';

interface Message {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  tools: ToolConfig[];
  agents: AgentConfig[];
  tasks: TaskConfig[];
  onAddTool: (tool: ToolConfig) => void;
  onAddAgent: (agent: AgentConfig) => void;
  onAddTask: (task: TaskConfig) => void;
}

type ConversationStep =
  | 'welcome'
  | 'agent_role'
  | 'agent_goal'
  | 'agent_backstory'
  | 'agent_tools'
  | 'task_description'
  | 'task_output'
  | 'continue_or_finish';

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  tools,
  agents,
  tasks,
  onAddTool,
  onAddAgent,
  onAddTask,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [step, setStep] = useState<ConversationStep>('welcome');
  const [currentAgent, setCurrentAgent] = useState<Partial<AgentConfig>>({
    tools: [],
    llm_provider: 'watsonx',
  });
  const [currentTask, setCurrentTask] = useState<Partial<TaskConfig>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initial welcome message
    addAssistantMessage(
      `Hello! I'm the Flow Architect, and I'm here to help you build your CrewAI workflow for Langflow.\n\n` +
      `Let's start by defining your first AI agent. Every agent needs:\n` +
      `- A **role** (e.g., "Security Analyst", "Data Scientist")\n` +
      `- A **goal** (what they're trying to achieve)\n` +
      `- A **backstory** (their expertise and context)\n\n` +
      `What role would you like your first agent to have?`
    );
    setStep('agent_role');
  }, []);

  const addAssistantMessage = (content: string) => {
    const message: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, message]);
  };

  const addUserMessage = (content: string) => {
    const message: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, message]);
  };

  const generateId = (prefix: string) => {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userInput = input.trim();
    addUserMessage(userInput);
    setInput('');

    // Process based on current step
    setTimeout(() => {
      processStep(userInput);
    }, 500);
  };

  const processStep = (userInput: string) => {
    switch (step) {
      case 'agent_role':
        setCurrentAgent((prev) => ({
          ...prev,
          role: userInput,
          id: generateId('agent'),
        }));
        addAssistantMessage(
          `Great! Your agent will be a "${userInput}".\n\n` +
          `Now, what is the primary **goal** of this agent? What are they trying to accomplish?`
        );
        setStep('agent_goal');
        break;

      case 'agent_goal':
        setCurrentAgent((prev) => ({ ...prev, goal: userInput }));
        addAssistantMessage(
          `Excellent goal. Now let's give this agent some context.\n\n` +
          `What is the **backstory** of this agent? Describe their expertise and why they're qualified for this role.`
        );
        setStep('agent_backstory');
        break;

      case 'agent_backstory':
        setCurrentAgent((prev) => ({ ...prev, backstory: userInput }));
        addAssistantMessage(
          `Perfect! Now, does this agent need any **tools**?\n\n` +
          `You can:\n` +
          `- Type "filesystem" for MCP Filesystem access\n` +
          `- Type "search" for web search capabilities\n` +
          `- Type "none" if no tools are needed\n` +
          `- Type custom tool names separated by commas\n\n` +
          `What tools should this agent have?`
        );
        setStep('agent_tools');
        break;

      case 'agent_tools':
        handleToolSelection(userInput);
        break;

      case 'task_description':
        setCurrentTask((prev) => ({
          ...prev,
          description: userInput,
          id: generateId('task'),
        }));
        addAssistantMessage(
          `Good task description. What is the **expected output** of this task?\n\n` +
          `For example: "A detailed report in markdown format" or "A list of suspicious IP addresses"`
        );
        setStep('task_output');
        break;

      case 'task_output':
        // Complete the task and agent
        const completedTask: TaskConfig = {
          id: currentTask.id!,
          description: currentTask.description!,
          expected_output: userInput,
          assigned_agent: currentAgent.id!,
        };

        const completedAgent: AgentConfig = {
          id: currentAgent.id!,
          role: currentAgent.role!,
          goal: currentAgent.goal!,
          backstory: currentAgent.backstory!,
          llm_provider: currentAgent.llm_provider!,
          tools: currentAgent.tools!,
        };

        onAddAgent(completedAgent);
        onAddTask(completedTask);

        addAssistantMessage(
          `Excellent! I've created:\n\n` +
          `✓ **Agent:** ${completedAgent.role}\n` +
          `✓ **Task:** ${completedTask.description.substring(0, 50)}...\n\n` +
          `Would you like to:\n` +
          `- Type "add" to add another agent and task\n` +
          `- Type "done" to finish and download your flow`
        );

        // Reset for next agent
        setCurrentAgent({ tools: [], llm_provider: 'watsonx' });
        setCurrentTask({});
        setStep('continue_or_finish');
        break;

      case 'continue_or_finish':
        if (userInput.toLowerCase().includes('add') || userInput.toLowerCase().includes('another')) {
          addAssistantMessage(
            `Great! Let's create another agent.\n\n` +
            `What role should this new agent have?`
          );
          setStep('agent_role');
        } else {
          addAssistantMessage(
            `Perfect! Your flow is ready.\n\n` +
            `✓ ${agents.length + 1} agent(s) configured\n` +
            `✓ ${tasks.length + 1} task(s) defined\n` +
            `✓ ${tools.length} tool(s) available\n\n` +
            `Click the **Download Flow** button in the sidebar to get your Langflow JSON file!`
          );
        }
        break;
    }
  };

  const handleToolSelection = (userInput: string) => {
    const input = userInput.toLowerCase();
    const agentTools: string[] = [];

    if (input.includes('none')) {
      // No tools needed
    } else {
      // Check for filesystem
      if (input.includes('filesystem') || input.includes('file')) {
        const fsToolId = 'mcp-filesystem';
        agentTools.push(fsToolId);

        // Add tool if not exists
        if (!tools.find((t) => t.id === fsToolId)) {
          onAddTool({
            id: fsToolId,
            type: 'mcp',
            name: 'Filesystem MCP',
            description: 'Allows agents to read and access local files.',
            config: {
              command: 'npx',
              args: ['-y', '@modelcontextprotocol/server-filesystem', '/var/logs'],
            },
          });
        }
      }

      // Check for search
      if (input.includes('search') || input.includes('web')) {
        const searchToolId = 'tool-web-search';
        agentTools.push(searchToolId);

        // Add tool if not exists
        if (!tools.find((t) => t.id === searchToolId)) {
          onAddTool({
            id: searchToolId,
            type: 'custom',
            name: 'Web Search',
            description: 'Search the web for information.',
            python_dependencies: ['duckduckgo-search==4.1.0'],
          });
        }
      }
    }

    setCurrentAgent((prev) => ({ ...prev, tools: agentTools }));

    addAssistantMessage(
      `Got it! ${agentTools.length === 0 ? 'No tools assigned' : `Tools assigned: ${agentTools.join(', ')}`}.\n\n` +
      `Now let's define a **task** for this agent.\n\n` +
      `What should the "${currentAgent.role}" do? Describe the task in detail.`
    );
    setStep('task_description');
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex items-start space-x-3 ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {message.role === 'assistant' && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-ibm-blue flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
            )}
            <div
              className={`max-w-[70%] rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-ibm-blue text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="text-sm whitespace-pre-line">{message.content}</p>
            </div>
            {message.role === 'user' && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
                <User className="w-5 h-5 text-gray-700" />
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="border-t border-gray-200 p-4 bg-gray-50">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your response..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ibm-blue focus:border-transparent"
          />
          <button
            type="submit"
            disabled={!input.trim()}
            className="px-6 py-3 bg-ibm-blue text-white rounded-lg hover:bg-ibm-blue-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Send className="w-5 h-5" />
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
