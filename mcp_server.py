from marketing_posts.crewai_to_mcp import crewai_to_mcp
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

if __name__ == "__main__":
    mcp.run(transport="sse")
