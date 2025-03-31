import warnings
from typing import Any
from .crewai_to_mcp import crewai_to_mcp_tool, add_crew_to_mcp
from marketing_posts.crew import MarketingPostsCrew
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP


class InputSchema(BaseModel):
    customer_domain: str
    project_description: str


mcp = FastMCP("my MCP Server")
name = "Marketing Crew"
description = "A crew that creates marketing posts"
input_schema = InputSchema

# we can add more than once crew!

tool = crewai_to_mcp_tool(
    crewai_class=MarketingPostsCrew,
    name=name,
    description=description,
    input_schema=input_schema,
)
mcp.add_tool(
    tool,
    name=name,
    description=description,
)


def serve_sse():
    mcp.run(transport="sse")


def serve_stdio():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve_stdio()
