/**
 * Main Application Component
 * Universal CrewAI Flow Generator
 */

import React, { useState } from 'react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import LivePreview from './components/LivePreview';
import { api, ToolConfig, AgentConfig, TaskConfig } from './api/client';

const App: React.FC = () => {
  const [tools, setTools] = useState<ToolConfig[]>([]);
  const [agents, setAgents] = useState<AgentConfig[]>([]);
  const [tasks, setTasks] = useState<TaskConfig[]>([]);
  const [isDownloading, setIsDownloading] = useState(false);

  const handleAddTool = (tool: ToolConfig) => {
    // Check if tool already exists
    if (!tools.find((t) => t.id === tool.id)) {
      setTools((prev) => [...prev, tool]);
    }
  };

  const handleAddAgent = (agent: AgentConfig) => {
    setAgents((prev) => [...prev, agent]);
  };

  const handleAddTask = (task: TaskConfig) => {
    setTasks((prev) => [...prev, task]);
  };

  const handleDownload = async () => {
    try {
      setIsDownloading(true);

      // First compile to check for errors
      const compileResult = await api.compileFlow({
        tools,
        agents,
        tasks,
        crew_name: 'Enterprise AI Crew',
        process: 'sequential',
      });

      if (!compileResult.success) {
        alert(`Error: ${compileResult.message}`);
        return;
      }

      // Download the file
      const blob = await api.downloadFlow({
        tools,
        agents,
        tasks,
        crew_name: 'Enterprise AI Crew',
        process: 'sequential',
      });

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'enterprise_flow.json';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      alert('Flow downloaded successfully! You can now import it into Langflow.');
    } catch (error: any) {
      console.error('Download error:', error);
      alert(`Failed to download flow: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <Header />

      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar - Live Preview */}
        <div className="w-[30%] min-w-[320px] max-w-[400px]">
          <LivePreview
            tools={tools}
            agents={agents}
            tasks={tasks}
            onDownload={handleDownload}
            isDownloading={isDownloading}
          />
        </div>

        {/* Main Content - Chat Interface */}
        <div className="flex-1">
          <ChatInterface
            tools={tools}
            agents={agents}
            tasks={tasks}
            onAddTool={handleAddTool}
            onAddAgent={handleAddAgent}
            onAddTask={handleAddTask}
          />
        </div>
      </div>
    </div>
  );
};

export default App;
