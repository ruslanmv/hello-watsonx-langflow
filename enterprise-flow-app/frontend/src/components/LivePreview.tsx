/**
 * Live Preview Sidebar Component
 * Displays current configuration state and download button
 */

import React from 'react';
import { Download, Check, AlertCircle, Wrench, Users, ClipboardList } from 'lucide-react';
import { ToolConfig, AgentConfig, TaskConfig } from '../api/client';

interface LivePreviewProps {
  tools: ToolConfig[];
  agents: AgentConfig[];
  tasks: TaskConfig[];
  onDownload: () => void;
  isDownloading: boolean;
}

const LivePreview: React.FC<LivePreviewProps> = ({
  tools,
  agents,
  tasks,
  onDownload,
  isDownloading,
}) => {
  const isValid = agents.length > 0 && tasks.length > 0;
  const totalItems = tools.length + agents.length + tasks.length;

  return (
    <div className="h-full flex flex-col bg-gray-50 border-r border-gray-200">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 bg-white">
        <h2 className="text-xl font-bold text-gray-800 mb-2">Live Context</h2>
        <p className="text-sm text-gray-600">
          {totalItems} item{totalItems !== 1 ? 's' : ''} configured
        </p>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Tools Section */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Wrench className="w-5 h-5 text-ibm-blue" />
            <h3 className="font-semibold text-gray-800">Tools ({tools.length})</h3>
          </div>
          {tools.length === 0 ? (
            <p className="text-sm text-gray-500 italic ml-7">No tools defined yet</p>
          ) : (
            <div className="ml-7 space-y-2">
              {tools.map((tool) => (
                <div
                  key={tool.id}
                  className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-gray-800 text-sm">{tool.name}</p>
                      <p className="text-xs text-gray-500 mt-1">{tool.description}</p>
                      <span className="inline-block mt-2 px-2 py-1 text-xs font-medium rounded bg-blue-100 text-blue-800">
                        {tool.type.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Agents Section */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Users className="w-5 h-5 text-ibm-blue" />
            <h3 className="font-semibold text-gray-800">Agents ({agents.length})</h3>
          </div>
          {agents.length === 0 ? (
            <p className="text-sm text-gray-500 italic ml-7">No agents defined yet</p>
          ) : (
            <div className="ml-7 space-y-2">
              {agents.map((agent) => (
                <div
                  key={agent.id}
                  className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm"
                >
                  <p className="font-medium text-gray-800 text-sm">{agent.role}</p>
                  <p className="text-xs text-gray-500 mt-1">{agent.goal}</p>
                  {agent.tools.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {agent.tools.map((toolId) => (
                        <span
                          key={toolId}
                          className="px-2 py-0.5 text-xs bg-gray-100 text-gray-700 rounded"
                        >
                          {toolId}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Tasks Section */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <ClipboardList className="w-5 h-5 text-ibm-blue" />
            <h3 className="font-semibold text-gray-800">Tasks ({tasks.length})</h3>
          </div>
          {tasks.length === 0 ? (
            <p className="text-sm text-gray-500 italic ml-7">No tasks defined yet</p>
          ) : (
            <div className="ml-7 space-y-2">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm"
                >
                  <p className="font-medium text-gray-800 text-sm">
                    Task: {task.id}
                  </p>
                  <p className="text-xs text-gray-600 mt-1">{task.description}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    <span className="font-medium">Agent:</span> {task.assigned_agent}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Download Button */}
      <div className="p-6 border-t border-gray-200 bg-white">
        {isValid ? (
          <button
            onClick={onDownload}
            disabled={isDownloading}
            className="w-full bg-ibm-blue hover:bg-ibm-blue-dark text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isDownloading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Download className="w-5 h-5" />
                <span>Download Flow</span>
              </>
            )}
          </button>
        ) : (
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 text-amber-600 mb-2">
              <AlertCircle className="w-5 h-5" />
              <span className="text-sm font-medium">Configuration Incomplete</span>
            </div>
            <p className="text-xs text-gray-500">
              Define at least one agent and one task to continue
            </p>
          </div>
        )}

        {isValid && (
          <div className="mt-3 flex items-center justify-center space-x-2 text-green-600">
            <Check className="w-4 h-4" />
            <span className="text-xs font-medium">Ready to generate</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default LivePreview;
