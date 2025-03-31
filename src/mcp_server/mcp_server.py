from .crewai_to_mcp import crewai_to_mcp
from marketing_posts.crew import MarketingPostsCrew
from pydantic import BaseModel


class InputSchema(BaseModel):
    customer_domain: str
    project_description: str


mcp = crewai_to_mcp(
    crewai_class=MarketingPostsCrew,
    name="MarketingPostsCrew",
    description="A crew that creates marketing posts",
    input_schema=InputSchema,
)


def serve_sse():
    mcp.run(transport="sse")


def serve_stdio():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve_stdio()
