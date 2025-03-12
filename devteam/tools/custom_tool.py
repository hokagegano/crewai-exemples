import os
from typing import Type, Any
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    url: str = Field(..., description="URL of the website to scrape.")

class MyCustomTool(BaseTool):
    name: str = "Firecrawl Scrape Website Tool"
    description: str = "This tool scrapes a website and returns the text content."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, **kwargs: Any) -> Any:

        url = kwargs.get("url")
        app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        scrape_result = app.scrape_url(url, params={'formats': ['markdown', 'html']})

        return scrape_result
