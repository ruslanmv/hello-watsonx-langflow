#!/usr/bin/env python3
"""
Quick test script for the backend API
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.models import FlowRequest, ToolConfig, AgentConfig, TaskConfig

# Create test data
test_request = FlowRequest(
    tools=[
        ToolConfig(
            id="mcp-filesystem",
            type="mcp",
            name="Filesystem MCP",
            description="Allows agents to read local logs.",
            config={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/var/logs"]
            }
        )
    ],
    agents=[
        AgentConfig(
            id="agent_security",
            role="Security Analyst",
            goal="Analyze logs for breaches.",
            backstory="You are a veteran cyber analyst.",
            llm_provider="watsonx",
            tools=["mcp-filesystem"]
        )
    ],
    tasks=[
        TaskConfig(
            id="task_log_scan",
            description="Read logs and identify suspicious IPs.",
            expected_output="A list of IP addresses.",
            assigned_agent="agent_security"
        )
    ],
    crew_name="Test Crew",
    process="sequential"
)

print("Testing Backend Compilation...")
print(f"Tools: {len(test_request.tools)}")
print(f"Agents: {len(test_request.agents)}")
print(f"Tasks: {len(test_request.tasks)}")
print()

# Test compilation logic
try:
    sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))
    from src.layout_engine import LayoutEngine
    from src.tool_builder import ToolBuilder
    from src.crew_builder import CrewBuilder

    layout_engine = LayoutEngine()
    tool_builder = ToolBuilder(layout_engine)
    crew_builder = CrewBuilder(layout_engine)

    # Convert to dicts
    tools_config = [tool.model_dump() for tool in test_request.tools]
    agents_config = [agent.model_dump() for agent in test_request.agents]
    tasks_config = [task.model_dump() for task in test_request.tasks]

    # Build nodes
    all_nodes = []
    tool_nodes = tool_builder.build_tools(tools_config)
    all_nodes.extend(tool_nodes)
    print(f"✓ Created {len(tool_nodes)} tool node(s)")

    agent_nodes = crew_builder.build_agents(agents_config)
    all_nodes.extend(agent_nodes)
    print(f"✓ Created {len(agent_nodes)} agent node(s)")

    task_nodes = crew_builder.build_tasks(tasks_config)
    all_nodes.extend(task_nodes)
    print(f"✓ Created {len(task_nodes)} task node(s)")

    crew_node = crew_builder.build_crew(test_request.crew_name, test_request.process)
    all_nodes.append(crew_node)
    print(f"✓ Created crew node")

    # Build edges
    all_edges = []
    tool_agent_edges = crew_builder.create_tool_to_agent_edges(agents_config, tool_builder)
    all_edges.extend(tool_agent_edges)
    print(f"✓ Created {len(tool_agent_edges)} tool-to-agent edge(s)")

    agent_task_edges = crew_builder.create_agent_to_task_edges(tasks_config)
    all_edges.extend(agent_task_edges)
    print(f"✓ Created {len(agent_task_edges)} agent-to-task edge(s)")

    task_crew_edges = crew_builder.create_task_to_crew_edges(crew_node.id)
    all_edges.extend(task_crew_edges)
    print(f"✓ Created {len(task_crew_edges)} task-to-crew edge(s)")

    print()
    print(f"Total nodes: {len(all_nodes)}")
    print(f"Total edges: {len(all_edges)}")
    print()
    print("✅ Backend compilation test PASSED!")

except Exception as e:
    print(f"❌ Backend compilation test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
