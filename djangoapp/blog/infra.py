from dataclasses import dataclass
from typing import Self

class BaseTools:...

class AIResponse:...

class ChatBase:
    def __init__(self):
        self.tools = []
        
    def bind_tools(self, tools:list[BaseTools]) -> Self:
        self.tools = tools
        return self
    
    def invoke(self, prompt:str) -> AIResponse: ...


@dataclass
class AgentBase:
    tools: list[BaseTools] | None
    llm_model: ChatBase | None
    temperature: int
    
    def _tool_node(self):...
        
    def _llm_node(self):...
    
    def _build_graph(self): ...
    
    def execulte(self):...
