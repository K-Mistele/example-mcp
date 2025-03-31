from typing import Any, Type, get_type_hints
from pydantic import BaseModel
import httpx
from mcp.server.fastmcp import FastMCP
from functools import wraps
import inspect
import json


def crewai_to_mcp(
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
    mcp = FastMCP(name)

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
        print('Inputs:', inputs)
        result = crewai_class().crew().kickoff(inputs=inputs.model_dump())
        print('Result:', result)
        with open('result.json', 'w') as f:
            f.write(result.model_dump_json())
        print('Result:', result.model_dump_json())
        return result.model_dump_json()
    """

    # Create a namespace for the function
    namespace = {
        "input_schema": input_schema,
        "crewai_class": crewai_class,
        "json": json,
    }

    # Execute the function definition in the namespace
    exec(body_str, namespace)

    # Get the created function
    run_agent = namespace["run_agent"]

    # Add proper function metadata
    run_agent.__name__ = "run_agent"
    run_agent.__doc__ = description

    # Register the function with MCP
    mcp.add_tool(run_agent, name=name, description=description)

    # Return the MCP server instance
    return mcp
