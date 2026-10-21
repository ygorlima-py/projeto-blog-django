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
import logging

load_dotenv()


logger = logging.getLogger(__name__)
MCP_TIMEOUT_SECONDS = 30
MCP_CLEANUP_TIMEOUT_SECONDS = 5
MCP_MAX_ATTEMPTS = 2


class ToolsMCP:
    def __init__(self, url: str, token: str | None) -> None:
        self.url = url
        self.token = token
        self._adapter: MCPAdapter | None = None

    def _build_adapter(self) -> MCPAdapter:
        parsed_url = urlparse(self.url)

        headers = {}
        if parsed_url.hostname == "djangoapp":
            headers["X-Forwarded-Proto"] = "https"

        if not self.token:
            raise ValueError("Add token bareer in env files")

        return MCPAdapter(
            Client(
                StreamableHttpTransport(self.url, headers=headers),
                auth=self.token,
            )
        )

    async def _open_adapter(self) -> None:
        adapter = self._build_adapter()

        try:
            await asyncio.wait_for(
                adapter.__aenter__(),
                timeout=MCP_TIMEOUT_SECONDS,
            )
        except BaseException:
            try:
                await asyncio.wait_for(
                    adapter.__aexit__(None, None, None),
                    timeout=MCP_CLEANUP_TIMEOUT_SECONDS,
                )
            except BaseException:
                logger.debug("Falha ao limpar sessão MCP incompleta", exc_info=True)
            self._adapter = None
            raise

        self._adapter = adapter

    async def __aenter__(self) -> "ToolsMCP":
        """Open one MCP session for the complete agent execution."""
        if self._adapter is None:
            await self._open_adapter()

        return self

    async def _close_adapter(
        self,
        exc_type=None,
        exc_value=None,
        traceback=None,
    ) -> None:
        adapter = self._adapter
        self._adapter = None

        if adapter is not None:
            try:
                await asyncio.wait_for(
                    adapter.__aexit__(exc_type, exc_value, traceback),
                    timeout=MCP_CLEANUP_TIMEOUT_SECONDS,
                )
            except BaseException:
                logger.warning("Falha ao fechar sessão MCP", exc_info=True)

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._close_adapter(exc_type, exc_value, traceback)
        
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

        tools: list[BaseTool] | None = None
        last_error: Exception | None = None

        for attempt in range(1, MCP_MAX_ATTEMPTS + 1):
            try:
                tools = await asyncio.wait_for(
                    self._adapter.list_tools(),
                    timeout=MCP_TIMEOUT_SECONDS,
                )
                last_error = None
                break
            except Exception as error:
                last_error = error

                if attempt == MCP_MAX_ATTEMPTS:
                    break

                logger.warning(
                    "MCP list_tools falhou (%s/%s); fechando e reconectando",
                    attempt,
                    MCP_MAX_ATTEMPTS,
                    exc_info=True,
                )
                await self._close_adapter()
                await asyncio.sleep(1)
                await self._open_adapter()

        if tools is None and last_error is not None:
            if isinstance(last_error, MCPError):
                message = (
                    f"Erro MCP {last_error.code}: {last_error.message} "
                    f"| dados: {last_error.data}"
                )
            else:
                message = (
                    "MCP não respondeu dentro do limite de "
                    f"{MCP_TIMEOUT_SECONDS}s: "
                    f"{type(last_error).__name__}: {last_error}"
                )

            raise RuntimeError(message) from last_error

        if tools is None:
            raise RuntimeError("Não foi possível carregar as ferramentas MCP")
        
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
