from abc import ABC
from typing import ClassVar, Any, cast
from collections.abc import AsyncIterator

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, SummarizationMiddleware
from langchain.agents.middleware.human_in_the_loop import InterruptOnConfig
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools.base import BaseTool
from langchain_core.runnables import RunnableConfig
from langchain.messages import HumanMessage
from langchain.agents.middleware.types import InputAgentState
from langchain_core.messages import BaseMessageChunk
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.types import Command

from tools import ToolsMCP
from config import load_settings
from infra import compress_context_model

settings = load_settings()

class AgentBase(ABC):
    
    blocked_tools: ClassVar[tuple[str, ...]] = ()
    
    tools: ToolsMCP | None = None
    
    human_in_the_loop: dict[str, bool | InterruptOnConfig] | None = None
    
    summarization: ClassVar[SummarizationMiddleware | None] = None
    
    system_prompt: str | None = None

    def __init__(
        self,
        model: str | BaseChatModel,
        checkpointer: BaseCheckpointSaver,
        ) -> None:
      
        self.model = model
        self.checkpointer = checkpointer
        self._agent = None
        self._pending_interrupts: dict[str, tuple[Any, ...]] = {}
    
    async def load_tools(self) -> list[BaseTool] | None:
        if not self.tools:
            return None
        
        return await self.tools.aget_tools(list(self.blocked_tools))
        
    def _build_human_in_the_loop(self) -> HumanInTheLoopMiddleware | None:
        if self.human_in_the_loop is None:
            return None
        
        return HumanInTheLoopMiddleware(interrupt_on=self.human_in_the_loop)
    
    async def build_agent(self):
        tools = await self.load_tools()
        
        _human_in_the_loop = self._build_human_in_the_loop()
        
        middleware = []
        if _human_in_the_loop:
            middleware.append(_human_in_the_loop)
        
        if self.summarization:
            middleware.append(self.summarization)            

        return create_agent(
            model=self.model,
            tools=tools,
            middleware=middleware if middleware else (),
            checkpointer=self.checkpointer,
            system_prompt=self.system_prompt,
        )
    
    async def ainvoke(
            self,
            _input,
            config: RunnableConfig | None = None,
        )-> dict[str, Any]:
        
        if not self._agent:
            self._agent = await self.build_agent()
            
        return await self._agent.ainvoke(_input, config)
    
    async def astream(
        self,
        user_input: str | Command,
        thread_id: str,
        )-> AsyncIterator[tuple[Any, dict[str, Any]]]:
        
        if self._agent is None:
            self._agent = await self.build_agent()
        
        self._pending_interrupts.pop(thread_id, None)
        
        config: RunnableConfig = {"configurable": {"thread_id": thread_id,}}
        
        _input: InputAgentState | Command
        
        if isinstance(user_input, Command):
            _input = user_input   
        
        else:
            _input = {"messages": [HumanMessage(content=user_input)]}
        
        stream = cast(
            AsyncIterator[dict[str, Any]],
            self._agent.astream(
                _input,
                config=config,
                stream_mode=["messages", "values"],
                version="v2",
            ),
        )
                   
        async for chunk in stream:
            if chunk["type"] == "messages":
                message_chunk, metadata = chunk["data"]
                
                yield message_chunk, metadata

            elif chunk["type"] == "values":
                interrupts = chunk.get("interrupts", ())

                if interrupts:
                    self._pending_interrupts[thread_id] = interrupts
                    return


    def get_pending_interrupt(self, thread_id: str) -> Any | None:
        interrupts = self._pending_interrupts.pop(thread_id, ())

        if interrupts:
            return interrupts[0]

        return None
        
class SupervisoryAgent(AgentBase):
    blocked_tools = (
        "create_story",
        "create_story_slide",
        "update_story",
        "update_story_slide",
    )
    
    tools = ToolsMCP(url=settings.mcp_url, token=settings.mcp_token)
    
    human_in_the_loop = {
        "create_post": {
            "allowed_decisions": ["approve", "edit", "reject"],
        },
        "update_post": {
            "allowed_decisions": ["approve", "edit", "reject"],
        },
        "create_story_element": {
            "allowed_decisions": ["approve", "edit", "reject"],
        },
        "update_story_element": {
            "allowed_decisions": ["approve", "edit", "reject"],
        },
        "list_affiliates_partner": {
            "allowed_decisions": ["approve", "reject"],
        },
    }
    
    summarization = SummarizationMiddleware(
        model=compress_context_model(),
        trigger=("tokens", 12_000),
        keep=("tokens", 4_000),
        trim_tokens_to_summarize=8_000,
    )
    
if __name__ == "__main__":
    from infra import load_llm
    import asyncio
    from langgraph.checkpoint.memory import InMemorySaver
    from rich import print
    
    graph = SupervisoryAgent(
                model=load_llm(),
                checkpointer=InMemorySaver(),
            )
    
    async def test():
        async for message_chunk, _ in graph.astream(user_input="Crie um post Aleatório", thread_id='teste'):
            if isinstance(message_chunk.content, str):
                print(message_chunk.content, end="", flush=True)

        interrupt = graph.get_pending_interrupt('test')
           
        if interrupt is not None:
            action_request = interrupt.value["action_requests"][0]
            review_configs = interrupt.value["review_configs"][0]
            decisions = [f"{keys}: {value}"for keys, value in action_request.get("args", {}).items()]
            print(
                f"\nInterrupção pendente: {action_request.get("name", "")}"
                f"\nArgumentos: {','.join(decisions)}"
                f"\nDecisão: {', '.join(review_configs.get("allowed_decisions"))}"
                )
            
    asyncio.run(test())