"""
Tool Builder: Converts MCP Servers and Custom Tools from YAML to Langflow Tool Nodes.
Handles both MCP (Model Context Protocol) and traditional OpenAPI/Custom tools.
"""

import json
from typing import Dict, List, Any
from uuid import uuid4
from .schemas import LangflowNode, NodePosition


class ToolBuilder:
    """
    Builds Langflow Tool nodes from YAML configuration.

    Supports:
        - MCP Servers (Model Context Protocol)
        - Custom Python Tools
        - OpenAPI Tools
    """

    def __init__(self, layout_engine):
        """
        Initialize the ToolBuilder.

        Args:
            layout_engine: LayoutEngine instance for positioning nodes
        """
        self.layout_engine = layout_engine
        self.tool_map: Dict[str, str] = {}  # Maps tool_id -> node_uuid

    def build_tools(self, tools_config: List[Dict[str, Any]]) -> List[LangflowNode]:
        """
        Build all tool nodes from configuration.

        Args:
            tools_config: List of tool configurations from YAML

        Returns:
            List of LangflowNode objects representing tools
        """
        nodes = []

        for tool_def in tools_config:
            node = self._create_tool_node(tool_def)
            nodes.append(node)

            # Store the mapping for later agent linking
            self.tool_map[tool_def["id"]] = node.id

        return nodes

    def _create_tool_node(self, tool_def: Dict[str, Any]) -> LangflowNode:
        """
        Create a single tool node based on its type.

        Args:
            tool_def: Tool configuration dictionary

        Returns:
            LangflowNode configured as a Tool
        """
        tool_id = tool_def.get("id")
        tool_type = tool_def.get("type")
        name = tool_def.get("name")
        description = tool_def.get("description", "")

        # Generate the tool code based on type
        if tool_type == "mcp":
            code = self._generate_mcp_code(tool_def)
        elif tool_type == "custom":
            code = self._generate_custom_tool_code(tool_def)
        elif tool_type == "openapi":
            code = self._generate_openapi_code(tool_def)
        else:
            code = f"# Unknown tool type: {tool_type}\n# Tool: {name}"

        # Get position from layout engine
        position = self.layout_engine.get_tool_position()

        # Create the node
        node_id = str(uuid4())
        node = LangflowNode(
            id=node_id,
            type="Tool",  # Generic Tool type for compatibility
            position=position,
            data={
                "type": "Tool",
                "node": {
                    "template": {
                        "tool_name": {"value": name},
                        "name": {"value": name},
                        "description": {"value": description},
                        "tool_code": {"value": code},
                        "code": {"value": code},
                        "return_direct": {"value": False},
                    },
                    "description": description,
                    "display_name": name,
                    "documentation": f"Auto-generated from {tool_id}",
                    "base_classes": ["Tool"],
                },
                "id": node_id,
            }
        )

        return node

    def _generate_mcp_code(self, tool_def: Dict[str, Any]) -> str:
        """
        Generate Python code for an MCP Server tool.

        Args:
            tool_def: MCP tool configuration

        Returns:
            Python code as a string
        """
        name = tool_def.get("name")
        description = tool_def.get("description", "")
        config = tool_def.get("config", {})

        command = config.get("command", "npx")
        args = config.get("args", [])

        config_str = json.dumps(config, indent=2)

        code = f'''"""
{name}
{description}

MCP Server Configuration:
{config_str}
"""

import subprocess
import json
from langchain.tools import Tool

# MCP Server Configuration
MCP_COMMAND = {repr(command)}
MCP_ARGS = {repr(args)}

def run_mcp_tool(query: str) -> str:
    """
    Execute MCP server command with the given query.

    Args:
        query: The query or command to send to the MCP server

    Returns:
        Response from the MCP server
    """
    try:
        # Build the command
        cmd = [MCP_COMMAND] + MCP_ARGS

        # Execute the MCP server
        # Note: This is a simplified implementation
        # Real MCP integration would use the MCP protocol
        result = subprocess.run(
            cmd,
            input=query.encode(),
            capture_output=True,
            timeout=30
        )

        if result.returncode == 0:
            return result.stdout.decode()
        else:
            return f"Error: {{result.stderr.decode()}}"

    except subprocess.TimeoutExpired:
        return "Error: MCP server timeout"
    except Exception as e:
        return f"Error executing MCP tool: {{str(e)}}"

# Create the tool
tool = Tool(
    name="{name}",
    description="{description}",
    func=run_mcp_tool
)
'''

        return code

    def _generate_custom_tool_code(self, tool_def: Dict[str, Any]) -> str:
        """
        Generate Python code for a custom tool.

        Args:
            tool_def: Custom tool configuration

        Returns:
            Python code as a string
        """
        name = tool_def.get("name")
        description = tool_def.get("description", "")
        dependencies = tool_def.get("python_dependencies", [])

        deps_str = "\n# ".join(dependencies) if dependencies else "None"

        code = f'''"""
{name}
{description}

Python Dependencies:
# {deps_str}
"""

from langchain.tools import Tool

def execute_tool(query: str) -> str:
    """
    Execute the custom tool logic.

    Args:
        query: The query or input for the tool

    Returns:
        Tool execution result
    """
    # TODO: Implement custom tool logic here
    # This is a placeholder for enterprise customization

    try:
        # Example implementation for web search
        if "search" in "{name.lower()}":
            # Import required for DuckDuckGo (if needed)
            # from duckduckgo_search import DDGS

            # Placeholder: Replace with actual search implementation
            return f"Search results for: {{query}}"

        return f"Executed {name} with query: {{query}}"

    except Exception as e:
        return f"Error: {{str(e)}}"

# Create the tool
tool = Tool(
    name="{name}",
    description="{description}",
    func=execute_tool
)
'''

        return code

    def _generate_openapi_code(self, tool_def: Dict[str, Any]) -> str:
        """
        Generate Python code for an OpenAPI tool.

        Args:
            tool_def: OpenAPI tool configuration

        Returns:
            Python code as a string
        """
        name = tool_def.get("name")
        description = tool_def.get("description", "")
        spec_url = tool_def.get("spec_url", "")

        code = f'''"""
{name}
{description}

OpenAPI Specification: {spec_url}
"""

from langchain.tools import Tool
import requests

OPENAPI_SPEC_URL = "{spec_url}"

def call_openapi_endpoint(query: str) -> str:
    """
    Call OpenAPI endpoint with the given query.

    Args:
        query: The query to send to the API

    Returns:
        API response
    """
    try:
        # TODO: Parse OpenAPI spec and make appropriate API call
        # This is a placeholder implementation

        response = requests.get(OPENAPI_SPEC_URL)
        return f"API Response: {{response.status_code}}"

    except Exception as e:
        return f"Error calling API: {{str(e)}}"

# Create the tool
tool = Tool(
    name="{name}",
    description="{description}",
    func=call_openapi_endpoint
)
'''

        return code

    def get_tool_uuid(self, tool_id: str) -> str:
        """
        Get the UUID of a tool node by its logical ID.

        Args:
            tool_id: The logical ID from YAML config

        Returns:
            The UUID of the corresponding node

        Raises:
            KeyError: If tool_id not found
        """
        return self.tool_map[tool_id]
