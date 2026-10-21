from dotenv import load_dotenv
from dataclasses import dataclass
import os

load_dotenv()

@dataclass
class Settings:
    llm_token: str 
    mcp_token: str
    mcp_url: str
    uri_broker: str
    uri_checkpointer: str
    checkpointer: bool
    telegram_token: str | None
    
def load_settings() -> Settings:
    llm_token = os.getenv("LLM_API_KEY")
    mcp_token = os.getenv("MCP_TOKEN")
    mcp_url = os.getenv("URL_MCP")
    uri_broker = os.getenv("URL_BROKER")
    uri_checkpointer = os.getenv("DB_CHECKPOINTER_URI")
    _checkpointer = os.getenv("CHECKPOINTER", "1")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    
    if (
        not llm_token
        or 
        not mcp_token 
        or 
        not mcp_url
        or 
        not uri_broker
        or 
        not uri_checkpointer
        ):
        raise ValueError("Config Incomplete error")
    
    if _checkpointer not in ['0', '1']:
        raise ValueError("The checkpointer value can not different 0 or 1")
    
    if _checkpointer == "1":
        checkpointer = True
    
    else:
        checkpointer = False
        
    return Settings(
        llm_token=llm_token,
        mcp_token=mcp_token,
        mcp_url=mcp_url,
        uri_broker=uri_broker,
        uri_checkpointer=uri_checkpointer,
        checkpointer=checkpointer,
        telegram_token=telegram_token,
    )
