"""
Grid-based layout engine for organizing nodes on the Langflow canvas.
Ensures the generated flow is visually clean and readable.
"""

from typing import Tuple
from .schemas import NodePosition


class LayoutEngine:
    """
    Manages the spatial arrangement of nodes in a grid layout.

    Column Layout:
        - Column 0 (x=0):    MCP Servers & Tools
        - Column 1 (x=500):  CrewAI Agents
        - Column 2 (x=1000): CrewAI Tasks
        - Column 3 (x=1500): CrewAI Crew (final output)

    Row Layout:
        - Each node is spaced vertically by 200px
        - Starting Y position: 100px
    """

    # Column definitions (X coordinates)
    COL_TOOLS = 0
    COL_AGENTS = 500
    COL_TASKS = 1000
    COL_CREW = 1500

    # Spacing constants
    VERTICAL_SPACING = 200
    START_Y = 100

    def __init__(self):
        """Initialize layout counters for each column."""
        self.tool_count = 0
        self.agent_count = 0
        self.task_count = 0
        self.crew_count = 0

    def get_tool_position(self) -> NodePosition:
        """
        Get the next available position for a Tool node.

        Returns:
            NodePosition in the Tools column
        """
        y = self.START_Y + (self.tool_count * self.VERTICAL_SPACING)
        self.tool_count += 1
        return NodePosition(x=self.COL_TOOLS, y=y)

    def get_agent_position(self) -> NodePosition:
        """
        Get the next available position for an Agent node.

        Returns:
            NodePosition in the Agents column
        """
        y = self.START_Y + (self.agent_count * self.VERTICAL_SPACING)
        self.agent_count += 1
        return NodePosition(x=self.COL_AGENTS, y=y)

    def get_task_position(self) -> NodePosition:
        """
        Get the next available position for a Task node.

        Returns:
            NodePosition in the Tasks column
        """
        y = self.START_Y + (self.task_count * self.VERTICAL_SPACING)
        self.task_count += 1
        return NodePosition(x=self.COL_TASKS, y=y)

    def get_crew_position(self) -> NodePosition:
        """
        Get the next available position for a Crew node.

        Returns:
            NodePosition in the Crew column
        """
        y = self.START_Y + (self.crew_count * self.VERTICAL_SPACING)
        self.crew_count += 1
        return NodePosition(x=self.COL_CREW, y=y)

    def reset(self):
        """Reset all position counters."""
        self.tool_count = 0
        self.agent_count = 0
        self.task_count = 0
        self.crew_count = 0

    def get_stats(self) -> dict:
        """
        Get statistics about node placement.

        Returns:
            Dictionary with counts of each node type
        """
        return {
            "tools": self.tool_count,
            "agents": self.agent_count,
            "tasks": self.task_count,
            "crews": self.crew_count,
        }


def calculate_custom_position(column: int, row: int) -> NodePosition:
    """
    Calculate a custom position based on column and row indices.

    Args:
        column: Column index (0-3)
        row: Row index (0-based)

    Returns:
        NodePosition at the specified grid location
    """
    column_x = [
        LayoutEngine.COL_TOOLS,
        LayoutEngine.COL_AGENTS,
        LayoutEngine.COL_TASKS,
        LayoutEngine.COL_CREW,
    ]

    x = column_x[column] if column < len(column_x) else column * 500
    y = LayoutEngine.START_Y + (row * LayoutEngine.VERTICAL_SPACING)

    return NodePosition(x=x, y=y)
