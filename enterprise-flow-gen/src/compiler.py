"""
Flow Compiler: Main orchestration engine that compiles YAML configs into Langflow JSON.

This is the "brain" of the Universal CrewAI Flow Generator.
It coordinates all builders and produces the final Langflow JSON file.
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from .schemas import LangflowNode, LangflowEdge, LangflowFlow
from .layout_engine import LayoutEngine
from .tool_builder import ToolBuilder
from .crew_builder import CrewBuilder


class FlowCompiler:
    """
    Main compiler that orchestrates the generation of Langflow flows.

    The compiler:
        1. Loads YAML configuration files
        2. Builds Tool nodes (MCP & Custom)
        3. Builds Agent nodes
        4. Builds Task nodes
        5. Builds the Crew orchestrator node
        6. Creates all edges (connections)
        7. Exports to Langflow JSON format
    """

    def __init__(self, config_dir: str = "config"):
        """
        Initialize the FlowCompiler.

        Args:
            config_dir: Directory containing YAML configuration files
        """
        self.config_dir = Path(config_dir)
        self.layout_engine = LayoutEngine()
        self.tool_builder = ToolBuilder(self.layout_engine)
        self.crew_builder = CrewBuilder(self.layout_engine)

        # Storage for loaded configs
        self.tools_config: List[Dict[str, Any]] = []
        self.agents_config: List[Dict[str, Any]] = []
        self.tasks_config: List[Dict[str, Any]] = []

        # Storage for generated nodes and edges
        self.all_nodes: List[LangflowNode] = []
        self.all_edges: List[LangflowEdge] = []

    def load_configs(self):
        """
        Load all YAML configuration files.

        Raises:
            FileNotFoundError: If any required config file is missing
            yaml.YAMLError: If any config file has invalid YAML syntax
        """
        print("📂 Loading configuration files...")

        # Load tools_mcp.yaml
        tools_file = self.config_dir / "tools_mcp.yaml"
        if not tools_file.exists():
            raise FileNotFoundError(f"Missing required file: {tools_file}")

        with open(tools_file, 'r') as f:
            tools_data = yaml.safe_load(f)
            self.tools_config = tools_data.get("tools", [])
            print(f"   ✓ Loaded {len(self.tools_config)} tools from {tools_file}")

        # Load agents.yaml
        agents_file = self.config_dir / "agents.yaml"
        if not agents_file.exists():
            raise FileNotFoundError(f"Missing required file: {agents_file}")

        with open(agents_file, 'r') as f:
            agents_data = yaml.safe_load(f)
            self.agents_config = agents_data.get("agents", [])
            print(f"   ✓ Loaded {len(self.agents_config)} agents from {agents_file}")

        # Load tasks.yaml
        tasks_file = self.config_dir / "tasks.yaml"
        if not tasks_file.exists():
            raise FileNotFoundError(f"Missing required file: {tasks_file}")

        with open(tasks_file, 'r') as f:
            tasks_data = yaml.safe_load(f)
            self.tasks_config = tasks_data.get("tasks", [])
            print(f"   ✓ Loaded {len(self.tasks_config)} tasks from {tasks_file}")

        print("✅ All configurations loaded successfully\n")

    def compile(self) -> LangflowFlow:
        """
        Compile all configurations into a complete Langflow flow.

        Returns:
            LangflowFlow object ready for JSON export

        Raises:
            ValueError: If configuration is invalid
        """
        print("🔧 Starting compilation process...\n")

        # Step 1: Build Tool Nodes
        print("🛠️  Step 1: Building Tool nodes...")
        tool_nodes = self.tool_builder.build_tools(self.tools_config)
        self.all_nodes.extend(tool_nodes)
        print(f"   ✓ Created {len(tool_nodes)} tool nodes\n")

        # Step 2: Build Agent Nodes
        print("👤 Step 2: Building Agent nodes...")
        agent_nodes = self.crew_builder.build_agents(self.agents_config)
        self.all_nodes.extend(agent_nodes)
        print(f"   ✓ Created {len(agent_nodes)} agent nodes\n")

        # Step 3: Build Task Nodes
        print("📋 Step 3: Building Task nodes...")
        task_nodes = self.crew_builder.build_tasks(self.tasks_config)
        self.all_nodes.extend(task_nodes)
        print(f"   ✓ Created {len(task_nodes)} task nodes\n")

        # Step 4: Build Crew Node
        print("🎯 Step 4: Building Crew orchestrator...")
        crew_node = self.crew_builder.build_crew(
            crew_name="Enterprise Security Crew",
            process="sequential"
        )
        self.all_nodes.append(crew_node)
        print(f"   ✓ Created crew node\n")

        # Step 5: Create Edges (Connections)
        print("🔗 Step 5: Creating node connections...")

        # 5a: Tool -> Agent edges
        tool_agent_edges = self.crew_builder.create_tool_to_agent_edges(
            self.agents_config,
            self.tool_builder
        )
        self.all_edges.extend(tool_agent_edges)
        print(f"   ✓ Created {len(tool_agent_edges)} tool-to-agent edges")

        # 5b: Agent -> Task edges
        agent_task_edges = self.crew_builder.create_agent_to_task_edges(
            self.tasks_config
        )
        self.all_edges.extend(agent_task_edges)
        print(f"   ✓ Created {len(agent_task_edges)} agent-to-task edges")

        # 5c: Task -> Crew edges
        task_crew_edges = self.crew_builder.create_task_to_crew_edges(
            crew_node.id
        )
        self.all_edges.extend(task_crew_edges)
        print(f"   ✓ Created {len(task_crew_edges)} task-to-crew edges")

        print(f"\n📊 Total: {len(self.all_edges)} edges created\n")

        # Step 6: Build the final flow
        print("🏗️  Step 6: Assembling final flow...")
        flow = LangflowFlow(
            nodes=self.all_nodes,
            edges=self.all_edges,
            viewport={"x": 0, "y": 0, "zoom": 0.8}
        )

        print("✅ Compilation complete!\n")
        self._print_summary()

        return flow

    def export_json(self, flow: LangflowFlow, output_file: str = "enterprise_demo.json"):
        """
        Export the compiled flow to a JSON file.

        Args:
            flow: The LangflowFlow to export
            output_file: Path to the output JSON file
        """
        print(f"💾 Exporting to {output_file}...")

        output_path = Path(output_file)

        # Convert Pydantic models to dict
        flow_dict = flow.model_dump(exclude_none=True)

        # Write to file with pretty formatting
        with open(output_path, 'w') as f:
            json.dump(flow_dict, f, indent=2)

        file_size = output_path.stat().st_size
        print(f"✅ Export complete! ({file_size:,} bytes)\n")
        print(f"📍 File location: {output_path.absolute()}")

    def _print_summary(self):
        """Print a summary of the compiled flow."""
        stats = self.layout_engine.get_stats()

        print("=" * 60)
        print("COMPILATION SUMMARY")
        print("=" * 60)
        print(f"  🛠️  Tools:       {stats['tools']}")
        print(f"  👤 Agents:      {stats['agents']}")
        print(f"  📋 Tasks:       {stats['tasks']}")
        print(f"  🎯 Crews:       {stats['crews']}")
        print(f"  🔗 Edges:       {len(self.all_edges)}")
        print(f"  📦 Total Nodes: {len(self.all_nodes)}")
        print("=" * 60)
        print()

    def validate_config(self):
        """
        Validate the loaded configuration for common issues.

        Raises:
            ValueError: If validation fails
        """
        print("🔍 Validating configuration...\n")

        # Check that all agent tool references exist
        tool_ids = {t["id"] for t in self.tools_config}
        for agent in self.agents_config:
            for tool_id in agent.get("tools", []):
                if tool_id not in tool_ids:
                    raise ValueError(
                        f"Agent '{agent['id']}' references unknown tool '{tool_id}'"
                    )

        # Check that all task agent references exist
        agent_ids = {a["id"] for a in self.agents_config}
        for task in self.tasks_config:
            assigned_agent = task.get("assigned_agent")
            if assigned_agent not in agent_ids:
                raise ValueError(
                    f"Task '{task['id']}' references unknown agent '{assigned_agent}'"
                )

        print("✅ Configuration is valid\n")

    def run(self, output_file: str = "enterprise_demo.json"):
        """
        Run the complete compilation pipeline.

        Args:
            output_file: Path to the output JSON file

        Returns:
            Path to the generated file
        """
        try:
            # Load configurations
            self.load_configs()

            # Validate
            self.validate_config()

            # Compile
            flow = self.compile()

            # Export
            self.export_json(flow, output_file)

            return Path(output_file).absolute()

        except Exception as e:
            print(f"\n❌ Error during compilation: {e}")
            raise


def main():
    """
    Main entry point for command-line usage.
    """
    import sys

    print("\n" + "=" * 60)
    print("UNIVERSAL CREWAI FLOW GENERATOR")
    print("Enterprise AI Architect & Python Tooling")
    print("=" * 60 + "\n")

    try:
        compiler = FlowCompiler(config_dir="config")
        output_file = compiler.run()

        print("\n" + "=" * 60)
        print("🎉 SUCCESS!")
        print("=" * 60)
        print(f"\nYour Langflow JSON is ready: {output_file}")
        print("\nNext steps:")
        print("  1. Open Langflow in your browser")
        print("  2. Click 'Import' and select enterprise_demo.json")
        print("  3. Review and customize the flow")
        print("  4. Run your enterprise AI workflow!")
        print()

    except FileNotFoundError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure all required YAML files exist in the config/ directory:")
        print("  - config/tools_mcp.yaml")
        print("  - config/agents.yaml")
        print("  - config/tasks.yaml")
        sys.exit(1)

    except yaml.YAMLError as e:
        print(f"\n❌ YAML Parsing Error: {e}")
        print("\nPlease check your YAML files for syntax errors.")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
