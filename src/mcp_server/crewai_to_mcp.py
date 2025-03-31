from typing import Any, Type, get_type_hints
from pydantic import BaseModel
import httpx
from mcp.server.fastmcp import FastMCP
from functools import wraps
import json
import contextlib
import io


def crewai_to_mcp_tool(
    crewai_class: Any,
    name: str,
    description: str,
    input_schema: Type[BaseModel],
):
    """
    Convert a CrewAI class to a MCP server.

    Args:
        crewai_class: The CrewAI class to convert
        name: The name of the MCP server
        description: The description of the MCP server
        input_schema: The Pydantic model class defining the input schema
    """

    # Get the field names and types from the input schema
    schema_fields = input_schema.model_fields

    # Create the parameter string for the function signature
    params_str = ", ".join(
        f"{field_name}: {field_info.annotation.__name__}"
        for field_name, field_info in schema_fields.items()
    )

    # Create the function body that constructs the input schema
    body_str = f"""def run_agent({params_str}):
        inputs = input_schema({', '.join(f'{name}={name}' for name in schema_fields)})
        with contextlib.redirect_stdout(io.StringIO()):
            result = crewai_class().crew().kickoff(inputs=inputs.model_dump())
        return result.model_dump_json()
    """

    # Create a namespace for the function
    namespace = {
        "input_schema": input_schema,
        "crewai_class": crewai_class,
        "json": json,
        "contextlib": contextlib,
    }

    # Execute the function definition in the namespace
    exec(body_str, namespace)

    # Get the created function
    run_agent = namespace["run_agent"]

    # Add proper function metadata
    run_agent.__name__ = name
    run_agent.__doc__ = description

    return run_agent


def add_crew_to_mcp(
    mcp: FastMCP, crew: Any, name: str, description: str, input_schema: Type[BaseModel]
):

    tool = crewai_to_mcp_tool(
        crewai_class=crew,
        name=name,
        description=description,
        input_schema=input_schema,
    )
    mcp.add_tool(
        tool,
        name=name,
        description=description,
    )
