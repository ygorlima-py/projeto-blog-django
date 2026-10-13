from dotenv import load_dotenv
from dataclasses import dataclass
import os

load_dotenv()

@dataclass
class Settings:
    llm_token: str 
    mcp_token: str
    mcp_url: str
    
    
def load_settings() -> Settings:
    llm_token = os.getenv("LLM_API_KEY")
    mcp_token = os.getenv("MCP_TOKEN")
    mcp_url = os.getenv("URL_MCP")
    
    if not llm_token or not mcp_token or not mcp_url:
        raise ValueError("Config Incomplete error")
    
    return Settings(
        llm_token=llm_token,
        mcp_token=mcp_token,
        mcp_url=mcp_url,
    )
        
    
        