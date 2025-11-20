# Universal CrewAI Flow Generator

**Enterprise AI Architect & Python Tooling Specialist**

A production-ready Python application that compiles YAML configuration files into Langflow JSON flows, combining the best of IBM Watsonx Orchestrate-style configuration with Model Context Protocol (MCP) tool integration.

## Features

- 🛠️ **MCP Server Integration**: Define Model Context Protocol servers as tools
- 🔧 **Custom Tools**: Support for Python-based custom tools with dependency management
- 👥 **Agent Configuration**: Watsonx-style agent definitions with roles, goals, and backstories
- 📋 **Task Management**: Define tasks and assign them to agents
- 🔗 **Automatic Linking**: Smart edge creation between tools, agents, tasks, and crews
- 📐 **Grid Layout**: Clean, organized visual layout in Langflow
- ✅ **Validation**: Built-in configuration validation with helpful error messages

## Project Structure

```
enterprise-flow-gen/
├── config/
│   ├── tools_mcp.yaml       # MCP Servers & Custom Tools
│   ├── agents.yaml          # CrewAI Agents
│   └── tasks.yaml           # CrewAI Tasks
├── src/
│   ├── __init__.py          # Package initialization
│   ├── schemas.py           # Pydantic models for validation
│   ├── tool_builder.py      # Tool node generation
│   ├── crew_builder.py      # Agent/Task/Crew node generation
│   ├── layout_engine.py     # Grid-based positioning
│   └── compiler.py          # Main orchestration logic
├── generate_flow.py         # Entry point script
└── enterprise_demo.json     # Generated Langflow JSON (output)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
cd enterprise-flow-gen
pip install pyyaml pydantic
```

## Usage

### Basic Usage

Generate the Langflow JSON from the provided YAML configurations:

```bash
python generate_flow.py
```

This will create `enterprise_demo.json` in the current directory.

### Custom Output File

Specify a custom output file:

```bash
python generate_flow.py my_custom_flow.json
```

### Validate Configuration Only

Check your YAML files without generating output:

```bash
python generate_flow.py --validate-only
```

### Custom Configuration Directory

Use a different config directory:

```bash
python generate_flow.py --config ./my_configs --output ./output/flow.json
```

### Command-Line Options

```
usage: generate_flow.py [-h] [--config CONFIG] [--output OUTPUT_FILE_FLAG]
                        [--validate-only] [--quiet]
                        [output_file]

positional arguments:
  output_file           Output JSON file path (default: enterprise_demo.json)

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Configuration directory path (default: config)
  --output OUTPUT_FILE_FLAG, -o OUTPUT_FILE_FLAG
                        Output JSON file path
  --validate-only, -v   Only validate configuration without generating output
  --quiet, -q           Suppress all output except errors
```

## Configuration Files

### 1. tools_mcp.yaml

Define MCP servers and custom tools:

```yaml
tools:
  - id: "mcp-filesystem"
    type: "mcp"
    name: "Filesystem MCP"
    description: "Allows agents to read local logs."
    config:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/var/logs"]

  - id: "tool-web-search"
    type: "custom"
    name: "DuckDuckGo Search"
    description: "Search the web for competitors."
    python_dependencies:
      - "duckduckgo-search==4.1.0"
```

**Supported Tool Types:**
- `mcp`: Model Context Protocol servers
- `custom`: Python-based custom tools
- `openapi`: OpenAPI/REST API tools

### 2. agents.yaml

Define CrewAI agents with their configurations:

```yaml
agents:
  - id: "agent_security"
    role: "Security Analyst"
    goal: "Analyze logs for breaches."
    backstory: "You are a veteran cyber analyst using IBM Granite."
    llm_provider: "watsonx"
    tools:
      - "mcp-filesystem"
      - "tool-web-search"
```

### 3. tasks.yaml

Define tasks and assign them to agents:

```yaml
tasks:
  - id: "task_log_scan"
    description: "Read /var/logs/access.log and identify suspicious IPs."
    expected_output: "A list of IP addresses."
    assigned_agent: "agent_security"
```

## Architecture

### Layout System

The generator uses a 4-column grid layout for optimal readability:

- **Column 0 (x=0)**: MCP Servers & Tools
- **Column 1 (x=500)**: CrewAI Agents
- **Column 2 (x=1000)**: CrewAI Tasks
- **Column 3 (x=1500)**: CrewAI Crew (orchestrator)

Vertical spacing is 200px between nodes, starting at y=100.

### Edge Creation Logic

The compiler automatically creates connections:

1. **Tool → Agent**: For each tool referenced in an agent's `tools` list
2. **Agent → Task**: For each task's `assigned_agent`
3. **Task → Crew**: All tasks connect to the crew orchestrator

### Compilation Pipeline

1. **Load**: Read all YAML configuration files
2. **Validate**: Check for missing references and invalid configurations
3. **Build Tools**: Create Tool nodes with MCP/Custom configurations
4. **Build Agents**: Create Agent nodes with roles and goals
5. **Build Tasks**: Create Task nodes with descriptions
6. **Build Crew**: Create Crew orchestrator node
7. **Link**: Generate all edges between nodes
8. **Export**: Write Langflow JSON file

## Importing into Langflow

1. Start Langflow:
   ```bash
   langflow run
   ```

2. Open Langflow in your browser (typically http://localhost:7860)

3. Click the "Import" button

4. Select `enterprise_demo.json`

5. Review the generated flow:
   - Tools on the left
   - Agents in the middle-left
   - Tasks in the middle-right
   - Crew orchestrator on the right

6. Customize as needed and run your workflow!

## Error Handling

The generator provides helpful error messages for common issues:

- **Missing Files**: Clear indication of which YAML file is missing
- **Invalid References**: Shows exactly which tool/agent reference is broken
- **YAML Syntax Errors**: Displays the parsing error with line information
- **Validation Errors**: Explains configuration issues before compilation

## Enterprise Integration

### IBM Watsonx

The agents are configured to use IBM Watsonx as the LLM provider. Ensure your Langflow environment has Watsonx credentials configured.

### MCP Servers

MCP (Model Context Protocol) servers can be:
- Filesystem access servers
- Database query servers
- API integration servers
- Custom enterprise tool servers

### Security Considerations

- MCP server commands are sandboxed by configuration
- Tool dependencies are explicitly declared
- Agent permissions are controlled via tool assignments
- All configurations are version-controlled YAML

## Development

### Adding New Tool Types

Extend `tool_builder.py` to support additional tool types:

```python
def _generate_new_tool_type_code(self, tool_def: Dict[str, Any]) -> str:
    # Your custom tool generation logic
    pass
```

### Customizing Layout

Modify `layout_engine.py` to adjust positioning:

```python
COL_TOOLS = 0      # Adjust X coordinate
VERTICAL_SPACING = 200  # Adjust Y spacing
```

### Extending Validation

Add custom validation rules in `compiler.py`:

```python
def validate_config(self):
    # Your custom validation logic
    pass
```

## Troubleshooting

### Import Errors

If you get import errors, ensure the `src` directory is in your Python path:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python generate_flow.py
```

### YAML Parsing Errors

Validate your YAML syntax online or use a YAML validator:

```bash
python -c "import yaml; yaml.safe_load(open('config/tools_mcp.yaml'))"
```

### Missing Dependencies

Install all required packages:

```bash
pip install pyyaml pydantic
```

## License

Enterprise AI Architecture - Internal Use

## Author

Principal Enterprise AI Architect & Python Tooling Specialist

## Support

For issues and feature requests, please contact your enterprise AI team.
