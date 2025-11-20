"""
Crew Builder: Converts Agents and Tasks from YAML to Langflow CrewAI Nodes.
Handles the creation of CrewAI Agents, Tasks, and the final Crew orchestrator.
"""

from typing import Dict, List, Any, Tuple
from uuid import uuid4
from .schemas import LangflowNode, LangflowEdge


class CrewBuilder:
    """
    Builds CrewAI nodes (Agents, Tasks, Crew) from YAML configuration.

    The CrewBuilder creates:
        - Agent nodes with their configurations
        - Task nodes linked to agents
        - A Crew node that orchestrates all tasks
    """

    def __init__(self, layout_engine):
        """
        Initialize the CrewBuilder.

        Args:
            layout_engine: LayoutEngine instance for positioning nodes
        """
        self.layout_engine = layout_engine
        self.agent_map: Dict[str, str] = {}  # Maps agent_id -> node_uuid
        self.task_map: Dict[str, str] = {}   # Maps task_id -> node_uuid

    def build_agents(
        self,
        agents_config: List[Dict[str, Any]]
    ) -> List[LangflowNode]:
        """
        Build all agent nodes from configuration.

        Args:
            agents_config: List of agent configurations from YAML

        Returns:
            List of LangflowNode objects representing agents
        """
        nodes = []

        for agent_def in agents_config:
            node = self._create_agent_node(agent_def)
            nodes.append(node)

            # Store the mapping for later task linking
            self.agent_map[agent_def["id"]] = node.id

        return nodes

    def build_tasks(
        self,
        tasks_config: List[Dict[str, Any]]
    ) -> List[LangflowNode]:
        """
        Build all task nodes from configuration.

        Args:
            tasks_config: List of task configurations from YAML

        Returns:
            List of LangflowNode objects representing tasks
        """
        nodes = []

        for task_def in tasks_config:
            node = self._create_task_node(task_def)
            nodes.append(node)

            # Store the mapping for crew linking
            self.task_map[task_def["id"]] = node.id

        return nodes

    def build_crew(
        self,
        crew_name: str = "Enterprise Security Crew",
        process: str = "sequential"
    ) -> LangflowNode:
        """
        Build the Crew orchestrator node.

        Args:
            crew_name: Name of the crew
            process: Execution process ("sequential" or "hierarchical")

        Returns:
            LangflowNode configured as a CrewAI Crew
        """
        position = self.layout_engine.get_crew_position()
        node_id = str(uuid4())

        node = LangflowNode(
            id=node_id,
            type="CrewAICrew",
            position=position,
            data={
                "type": "CrewAICrew",
                "node": {
                    "template": {
                        "crew_name": {"value": crew_name},
                        "name": {"value": crew_name},
                        "process": {"value": process},
                        "verbose": {"value": True},
                        "memory": {"value": False},
                        "cache": {"value": True},
                        "max_rpm": {"value": 100},
                        "share_crew": {"value": False},
                        "tasks": {"value": []},
                    },
                    "description": "CrewAI Crew orchestrator",
                    "display_name": "Crew",
                    "documentation": "Orchestrates the execution of all tasks",
                    "base_classes": ["Crew"],
                },
                "id": node_id,
            }
        )

        return node

    def _create_agent_node(self, agent_def: Dict[str, Any]) -> LangflowNode:
        """
        Create a single agent node.

        Args:
            agent_def: Agent configuration dictionary

        Returns:
            LangflowNode configured as a CrewAI Agent
        """
        agent_id = agent_def.get("id")
        role = agent_def.get("role")
        goal = agent_def.get("goal")
        backstory = agent_def.get("backstory")
        llm_provider = agent_def.get("llm_provider", "watsonx")

        position = self.layout_engine.get_agent_position()
        node_id = str(uuid4())

        node = LangflowNode(
            id=node_id,
            type="CrewAIAgent",
            position=position,
            data={
                "type": "CrewAIAgent",
                "node": {
                    "template": {
                        "role": {"value": role},
                        "goal": {"value": goal},
                        "backstory": {"value": backstory},
                        "allow_delegation": {"value": False},
                        "verbose": {"value": True},
                        "cache": {"value": True},
                        "max_iter": {"value": 25},
                        "max_rpm": {"value": None},
                        "llm": {"value": None},  # Will be connected via edge
                        "tools": {"value": []},   # Will be connected via edges
                        "function_calling_llm": {"value": None},
                        "step_callback": {"value": None},
                    },
                    "description": f"CrewAI Agent: {role}",
                    "display_name": "Agent",
                    "documentation": f"Agent ID: {agent_id}",
                    "base_classes": ["Agent"],
                },
                "id": node_id,
            }
        )

        return node

    def _create_task_node(self, task_def: Dict[str, Any]) -> LangflowNode:
        """
        Create a single task node.

        Args:
            task_def: Task configuration dictionary

        Returns:
            LangflowNode configured as a CrewAI Task
        """
        task_id = task_def.get("id")
        description = task_def.get("description")
        expected_output = task_def.get("expected_output")

        position = self.layout_engine.get_task_position()
        node_id = str(uuid4())

        node = LangflowNode(
            id=node_id,
            type="CrewAITask",
            position=position,
            data={
                "type": "CrewAITask",
                "node": {
                    "template": {
                        "description": {"value": description},
                        "expected_output": {"value": expected_output},
                        "async_execution": {"value": False},
                        "agent": {"value": None},  # Will be connected via edge
                        "context": {"value": []},
                        "output_file": {"value": ""},
                        "output_json": {"value": None},
                        "output_pydantic": {"value": None},
                        "tools": {"value": []},
                    },
                    "description": f"CrewAI Task: {task_id}",
                    "display_name": "Task",
                    "documentation": f"Task ID: {task_id}",
                    "base_classes": ["Task"],
                },
                "id": node_id,
            }
        )

        return node

    def create_tool_to_agent_edges(
        self,
        agents_config: List[Dict[str, Any]],
        tool_builder
    ) -> List[LangflowEdge]:
        """
        Create edges connecting tools to agents.

        Args:
            agents_config: List of agent configurations
            tool_builder: ToolBuilder instance with tool_map

        Returns:
            List of LangflowEdge objects
        """
        edges = []

        for agent_def in agents_config:
            agent_id = agent_def.get("id")
            tools = agent_def.get("tools", [])

            # Get the agent's node UUID
            agent_uuid = self.agent_map[agent_id]

            # Create an edge for each tool
            for tool_id in tools:
                try:
                    tool_uuid = tool_builder.get_tool_uuid(tool_id)

                    edge = LangflowEdge(
                        source=tool_uuid,
                        target=agent_uuid,
                        sourceHandle="tool",
                        targetHandle="tools",
                    )
                    edges.append(edge)

                except KeyError:
                    print(f"Warning: Tool '{tool_id}' not found for agent '{agent_id}'")

        return edges

    def create_agent_to_task_edges(
        self,
        tasks_config: List[Dict[str, Any]]
    ) -> List[LangflowEdge]:
        """
        Create edges connecting agents to their assigned tasks.

        Args:
            tasks_config: List of task configurations

        Returns:
            List of LangflowEdge objects
        """
        edges = []

        for task_def in tasks_config:
            task_id = task_def.get("id")
            assigned_agent_id = task_def.get("assigned_agent")

            # Get the UUIDs
            task_uuid = self.task_map[task_id]
            agent_uuid = self.agent_map[assigned_agent_id]

            # Create edge from agent to task
            edge = LangflowEdge(
                source=agent_uuid,
                target=task_uuid,
                sourceHandle="agent",
                targetHandle="agent",
            )
            edges.append(edge)

        return edges

    def create_task_to_crew_edges(
        self,
        crew_node_id: str
    ) -> List[LangflowEdge]:
        """
        Create edges connecting all tasks to the crew node.

        Args:
            crew_node_id: UUID of the crew node

        Returns:
            List of LangflowEdge objects
        """
        edges = []

        for task_id, task_uuid in self.task_map.items():
            edge = LangflowEdge(
                source=task_uuid,
                target=crew_node_id,
                sourceHandle="task",
                targetHandle="tasks",
            )
            edges.append(edge)

        return edges

    def get_agent_uuid(self, agent_id: str) -> str:
        """Get the UUID of an agent node by its logical ID."""
        return self.agent_map[agent_id]

    def get_task_uuid(self, task_id: str) -> str:
        """Get the UUID of a task node by its logical ID."""
        return self.task_map[task_id]
