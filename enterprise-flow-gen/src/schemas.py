"""
Pydantic models for Langflow JSON schema validation.
Ensures the generated flow conforms to Langflow's expected structure.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4


class NodePosition(BaseModel):
    """Position of a node on the Langflow canvas."""
    x: int
    y: int


class NodeTemplate(BaseModel):
    """Template structure for node configuration."""
    # Allow any field structure since different node types have different templates
    class Config:
        extra = "allow"


class NodeData(BaseModel):
    """Data structure for a Langflow node."""
    node: Dict[str, Any] = Field(default_factory=dict)
    type: Optional[str] = None
    id: Optional[str] = None

    class Config:
        extra = "allow"


class LangflowNode(BaseModel):
    """
    Represents a single node in the Langflow graph.

    Fields:
        id: Unique identifier (UUID)
        type: Node type (e.g., "Tool", "CrewAIAgent", "CrewAITask", "CrewAICrew")
        data: Configuration data for the node
        position: X,Y coordinates on the canvas
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)
    position: NodePosition
    selected: bool = False
    dragging: bool = False
    positionAbsolute: Optional[NodePosition] = None

    class Config:
        extra = "allow"


class LangflowEdge(BaseModel):
    """
    Represents a connection between two nodes.

    Fields:
        source: Source node ID
        target: Target node ID
        sourceHandle: Output handle name on source node
        targetHandle: Input handle name on target node
    """
    source: str
    target: str
    sourceHandle: str = "id"
    targetHandle: str
    id: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = f"edge_{self.source}_{self.target}"


class LangflowFlow(BaseModel):
    """
    Complete Langflow flow structure.

    Fields:
        nodes: List of all nodes in the flow
        edges: List of all connections between nodes
        viewport: Canvas viewport settings
    """
    nodes: List[LangflowNode] = Field(default_factory=list)
    edges: List[LangflowEdge] = Field(default_factory=list)
    viewport: Dict[str, Any] = Field(
        default_factory=lambda: {"x": 0, "y": 0, "zoom": 0.8}
    )

    class Config:
        extra = "allow"


# Helper functions for creating specific node types

def create_tool_template(name: str, description: str, code: str) -> Dict[str, Any]:
    """Create a template structure for a Tool node."""
    return {
        "template": {
            "name": {"value": name},
            "description": {"value": description},
            "code": {"value": code},
            "tool_code": {"value": code},
        }
    }


def create_agent_template(
    role: str,
    goal: str,
    backstory: str,
    llm_provider: str = "watsonx"
) -> Dict[str, Any]:
    """Create a template structure for a CrewAI Agent node."""
    return {
        "template": {
            "role": {"value": role},
            "goal": {"value": goal},
            "backstory": {"value": backstory},
            "allow_delegation": {"value": False},
            "verbose": {"value": True},
            "llm": {"value": llm_provider},
            "tools": {"value": []},
        }
    }


def create_task_template(
    description: str,
    expected_output: str
) -> Dict[str, Any]:
    """Create a template structure for a CrewAI Task node."""
    return {
        "template": {
            "description": {"value": description},
            "expected_output": {"value": expected_output},
            "async_execution": {"value": False},
        }
    }


def create_crew_template(
    crew_name: str = "Enterprise Security Crew",
    process: str = "sequential"
) -> Dict[str, Any]:
    """Create a template structure for a CrewAI Crew node."""
    return {
        "template": {
            "name": {"value": crew_name},
            "process": {"value": process},
            "verbose": {"value": True},
            "memory": {"value": False},
            "tasks": {"value": []},
        }
    }
