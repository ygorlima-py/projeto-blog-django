from langchain.mcp import MCPAdapter
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from mcp.shared.exceptions import MCPError
from langchain_core.tools.base import BaseTool
from urllib.parse import urlparse

from rich import print

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


class ToolsMCP:
    def __init__(self, url: str, token: str | None) -> None:
        self.url = url
        self.token = token
        self._adapter: MCPAdapter | None = None

    async def __aenter__(self) -> "ToolsMCP":
        """Open one MCP session for the complete agent execution."""
        if self._adapter is not None:
            return self

        parsed_url = urlparse(self.url)

        headers = {}
        if parsed_url.hostname == "djangoapp":
            headers["X-Forwarded-Proto"] = "https"

        if not self.token:
            raise ValueError("Add token bareer in env files")

        adapter = MCPAdapter(
            Client(
                StreamableHttpTransport(self.url, headers=headers),
                auth=self.token,
            )
        )

        try:
            await adapter.__aenter__()
        except Exception:
            self._adapter = None
            raise

        self._adapter = adapter
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        adapter = self._adapter
        self._adapter = None

        if adapter is not None:
            await adapter.__aexit__(exc_type, exc_value, traceback)
        
    def _get_allowed_tools(self, tools:list[BaseTool], blocked_tools: list):
        
        _allowed_tools = []
        
        for tool in tools:
            if tool.name not in blocked_tools:
                
                _allowed_tools.append(tool)
                
        return _allowed_tools
    
    async def aget_tools(self, blocked: list[str] | None = None) -> list[BaseTool]:
        if self._adapter is None:
            raise RuntimeError(
                "A sessão MCP precisa estar aberta durante toda a execução "
                "do agente (use 'async with ToolsMCP(...)')."
            )

        try:
            tools = await self._adapter.list_tools()
        except MCPError as error:
            raise RuntimeError(
                f"Erro MCP {error.code}: {error.message} | dados: {error.data}"
            ) from error
        
        if blocked is None:
            return tools
        
        return self._get_allowed_tools(tools, blocked)
    

if __name__ == "__main__":
    token = os.getenv("MCP_TOKEN")
    
    tools_allowed = [
                'get_server_instructions',
                'create_post',
                'list_all_posts',
                'show_post_detail',
                'update_post',
                'list_affiliates_partner',
                'create_story_element',
                'list_published_stories',
                'show_story_detail_by_id',
                'update_story_element',
            ]
            
    
    tools_mcp = ToolsMCP(url="https://asiadeperto.com/mcp",token=token)

    async def load_tools():
        async with tools_mcp:
            return await tools_mcp.aget_tools(tools_allowed)

    tools = asyncio.run(load_tools())
    print(tools)
