/**
 * API Client for Universal CrewAI Flow Generator Backend
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8095';

export interface ToolConfig {
  id: string;
  type: 'mcp' | 'custom' | 'openapi';
  name: string;
  description: string;
  config?: {
    command?: string;
    args?: string[];
  };
  python_dependencies?: string[];
  spec_url?: string;
}

export interface AgentConfig {
  id: string;
  role: string;
  goal: string;
  backstory: string;
  llm_provider: string;
  tools: string[];
}

export interface TaskConfig {
  id: string;
  description: string;
  expected_output: string;
  assigned_agent: string;
}

export interface FlowRequest {
  tools: ToolConfig[];
  agents: AgentConfig[];
  tasks: TaskConfig[];
  crew_name?: string;
  process?: string;
}

export interface FlowResponse {
  success: boolean;
  message: string;
  flow?: any;
  stats?: {
    tools: number;
    agents: number;
    tasks: number;
    crews: number;
    edges: number;
    total_nodes: number;
  };
}

export interface HealthResponse {
  status: string;
  version: string;
  service: string;
}

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>('/api/health');
    return response.data;
  },

  /**
   * Compile flow configuration into Langflow JSON
   */
  async compileFlow(request: FlowRequest): Promise<FlowResponse> {
    const response = await apiClient.post<FlowResponse>('/api/compile', request);
    return response.data;
  },

  /**
   * Download the compiled flow as a JSON file
   */
  async downloadFlow(request: FlowRequest): Promise<Blob> {
    const response = await apiClient.post('/api/download', request, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
