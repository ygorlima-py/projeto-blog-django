from langchain.mcp import MCPAdapter
from fastmcp.client import Client
from mcp.shared.exceptions import MCPError
from langchain_core.tools.base import BaseTool

from rich import print

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


class ToolsMCP:
    def __init__(self, url: str, token: str | None) -> None:
        self.url = url
        self.token = token
        
    def _get_allowed_tools(self, tools:list[BaseTool], blocked_tools: list):
        
        _allowed_tools = []
        
        for tool in tools:
            if tool.name not in blocked_tools:
                
                _allowed_tools.append(tool)
                
        return _allowed_tools
    
    async def aget_tools(self, blocked: list[str] | None = None) -> list[BaseTool]:
        
        if not self.token:
            raise ValueError("Add token bareer in env files")
        
        try:
            async with MCPAdapter(Client(self.url, auth=self.token)) as adapter:
            
                tools = await adapter.list_tools()
           
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
    
    tools = asyncio.run(tools_mcp.aget_tools(tools_allowed))
    print(tools)