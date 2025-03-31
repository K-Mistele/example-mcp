# CrewAI to MCP

A bridge between CrewAI and Model Context Protocol (MCP) that allows you to expose CrewAI agents and crews as MCP tools.

## Overview

This project provides a simple integration between CrewAI and the Model Context Protocol (MCP), enabling you to expose CrewAI agents and crews as MCP-compatible tools. This allows for easy integration of CrewAI's powerful agent orchestration capabilities into any MCP-compatible system.

For the sake of illustration, we use CrewAI's marketing crew example.

## Features

- Convert CrewAI classes to MCP servers
- Automatic input schema validation using Pydantic
- Support for SSE (Server-Sent Events) transport
- JSON serialization of CrewAI outputs
- Easy-to-use API for creating MCP tools from CrewAI classes

## Installation

```shell
uv sync
```

### Configuration
Configure your OpenAI API key and Serper API key in `.env`
```
OPENAI_API_KEY=
SERPER_API_KEY=
```

## Usage

### Basic Example

```python
from crewai_to_mcp import crewai_to_mcp
from pydantic import BaseModel
from your_crew import YourCrew

# Define your input schema to describe what the inputs to the crew look like.
class InputSchema(BaseModel):
    customer_domain: str
    project_description: str

# Create an MCP server from your CrewAI class
mcp = crewai_to_mcp(
    crewai_class=YourCrew,
    name="YourCrewName",
    description="A description of what your crew does",
    input_schema=InputSchema
)

# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse")
```

### Configuration

The MCP server can be configured using environment variables or a configuration file. See the MCP documentation for more details on configuration options.

Example of Cursor configuration for SSE transport:

```json
{
  "mcpServers": {
    "crew": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

Example of Cursor configuration for STDIO transport:
```json
{
    "mcpServers": {
        "crew": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/K-Mistele/example-mcp serve_stdio"
            ],
            "env": {
                "OPENAI_API_KEY": "KEY GOES HERE",
                "SERVER_API_KEY": "KEY GOES HERE"
            }
        }
    }
}
```

## API Reference

### crewai_to_mcp

```python
def crewai_to_mcp(
    crewai_class: Any,
    name: str,
    description: str,
    input_schema: Type[BaseModel],
) -> FastMCP
```

Parameters:
- `crewai_class`: The CrewAI class to convert
- `name`: The name of the MCP server
- `description`: The description of the MCP server
- `input_schema`: A Pydantic model class defining the input schema

Returns:
- A FastMCP server instance

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

