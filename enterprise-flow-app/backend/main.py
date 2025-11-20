"""
FastAPI Backend for Universal CrewAI Flow Generator
Port: 8095
"""

import sys
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import json
import io

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import FlowRequest, FlowResponse, HealthResponse
from src.compiler import FlowCompiler
from src.layout_engine import LayoutEngine
from src.tool_builder import ToolBuilder
from src.crew_builder import CrewBuilder

# Initialize FastAPI app
app = FastAPI(
    title="Universal CrewAI Flow Generator API",
    description="Generate Langflow JSON files from configuration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default + React default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        service="Universal CrewAI Flow Generator"
    )


@app.post("/api/compile", response_model=FlowResponse)
async def compile_flow(request: FlowRequest):
    """
    Compile the flow configuration into a Langflow JSON.

    Args:
        request: FlowRequest containing tools, agents, and tasks

    Returns:
        FlowResponse with the compiled flow
    """
    try:
        # Initialize the compiler components
        layout_engine = LayoutEngine()
        tool_builder = ToolBuilder(layout_engine)
        crew_builder = CrewBuilder(layout_engine)

        # Convert Pydantic models to dicts
        tools_config = [tool.model_dump() for tool in request.tools]
        agents_config = [agent.model_dump() for agent in request.agents]
        tasks_config = [task.model_dump() for task in request.tasks]

        # Validate configuration
        validate_config(tools_config, agents_config, tasks_config)

        # Build nodes
        all_nodes = []
        all_edges = []

        # Step 1: Build Tool Nodes
        tool_nodes = tool_builder.build_tools(tools_config)
        all_nodes.extend(tool_nodes)

        # Step 2: Build Agent Nodes
        agent_nodes = crew_builder.build_agents(agents_config)
        all_nodes.extend(agent_nodes)

        # Step 3: Build Task Nodes
        task_nodes = crew_builder.build_tasks(tasks_config)
        all_nodes.extend(task_nodes)

        # Step 4: Build Crew Node
        crew_node = crew_builder.build_crew(
            crew_name=request.crew_name,
            process=request.process
        )
        all_nodes.append(crew_node)

        # Step 5: Create Edges
        # Tool -> Agent edges
        tool_agent_edges = crew_builder.create_tool_to_agent_edges(
            agents_config,
            tool_builder
        )
        all_edges.extend(tool_agent_edges)

        # Agent -> Task edges
        agent_task_edges = crew_builder.create_agent_to_task_edges(tasks_config)
        all_edges.extend(agent_task_edges)

        # Task -> Crew edges
        task_crew_edges = crew_builder.create_task_to_crew_edges(crew_node.id)
        all_edges.extend(task_crew_edges)

        # Build the final flow
        flow = {
            "nodes": [node.model_dump(exclude_none=True) for node in all_nodes],
            "edges": [edge.model_dump(exclude_none=True) for edge in all_edges],
            "viewport": {"x": 0, "y": 0, "zoom": 0.8}
        }

        # Get statistics
        stats = layout_engine.get_stats()
        stats["edges"] = len(all_edges)
        stats["total_nodes"] = len(all_nodes)

        return FlowResponse(
            success=True,
            message="Flow compiled successfully",
            flow=flow,
            stats=stats
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/download")
async def download_flow(request: FlowRequest):
    """
    Compile and download the flow as a JSON file.

    Args:
        request: FlowRequest containing tools, agents, and tasks

    Returns:
        StreamingResponse with the JSON file
    """
    try:
        # Compile the flow
        compile_result = await compile_flow(request)

        if not compile_result.success:
            raise HTTPException(status_code=400, detail=compile_result.message)

        # Convert to JSON string
        json_str = json.dumps(compile_result.flow, indent=2)

        # Create a file-like object
        json_bytes = io.BytesIO(json_str.encode())

        # Return as downloadable file
        return StreamingResponse(
            json_bytes,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=enterprise_flow.json"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")


def validate_config(
    tools_config: list,
    agents_config: list,
    tasks_config: list
):
    """
    Validate the configuration for common issues.

    Raises:
        ValueError: If validation fails
    """
    # Check that all agent tool references exist
    tool_ids = {t["id"] for t in tools_config}
    for agent in agents_config:
        for tool_id in agent.get("tools", []):
            if tool_id not in tool_ids:
                raise ValueError(
                    f"Agent '{agent['id']}' references unknown tool '{tool_id}'"
                )

    # Check that all task agent references exist
    agent_ids = {a["id"] for a in agents_config}
    for task in tasks_config:
        assigned_agent = task.get("assigned_agent")
        if assigned_agent not in agent_ids:
            raise ValueError(
                f"Task '{task['id']}' references unknown agent '{assigned_agent}'"
            )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Universal CrewAI Flow Generator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "compile": "/api/compile",
            "download": "/api/download"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8095)
