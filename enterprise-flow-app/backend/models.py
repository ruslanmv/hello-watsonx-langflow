"""
API Models for Universal CrewAI Flow Generator Backend
Pydantic models for request/response validation
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ToolConfig(BaseModel):
    """Configuration for a tool."""
    id: str
    type: str  # "mcp", "custom", "openapi"
    name: str
    description: str
    config: Optional[Dict[str, Any]] = None
    python_dependencies: Optional[List[str]] = None
    spec_url: Optional[str] = None


class AgentConfig(BaseModel):
    """Configuration for a CrewAI agent."""
    id: str
    role: str
    goal: str
    backstory: str
    llm_provider: str = "watsonx"
    tools: List[str] = Field(default_factory=list)


class TaskConfig(BaseModel):
    """Configuration for a CrewAI task."""
    id: str
    description: str
    expected_output: str
    assigned_agent: str


class FlowRequest(BaseModel):
    """Request model for flow compilation."""
    tools: List[ToolConfig] = Field(default_factory=list)
    agents: List[AgentConfig]
    tasks: List[TaskConfig]
    crew_name: str = "Enterprise AI Crew"
    process: str = "sequential"

    class Config:
        json_schema_extra = {
            "example": {
                "tools": [
                    {
                        "id": "mcp-filesystem",
                        "type": "mcp",
                        "name": "Filesystem MCP",
                        "description": "Allows agents to read local logs.",
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
                        "goal": "Analyze logs for breaches.",
                        "backstory": "You are a veteran cyber analyst.",
                        "llm_provider": "watsonx",
                        "tools": ["mcp-filesystem"]
                    }
                ],
                "tasks": [
                    {
                        "id": "task_log_scan",
                        "description": "Read logs and identify suspicious IPs.",
                        "expected_output": "A list of IP addresses.",
                        "assigned_agent": "agent_security"
                    }
                ],
                "crew_name": "Security Crew",
                "process": "sequential"
            }
        }


class FlowResponse(BaseModel):
    """Response model for flow compilation."""
    success: bool
    message: str
    flow: Optional[Dict[str, Any]] = None
    stats: Optional[Dict[str, int]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    service: str
