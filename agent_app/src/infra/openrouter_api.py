from langchain_openai import ChatOpenAI
from config import load_settings

settings = load_settings()

def load_llm() -> ChatOpenAI:
    
    return ChatOpenAI(
        model="deepseek/deepseek-v4.1-flash",
        temperature=0.3,
        openai_api_key=settings.llm_token, #type: ignore
        base_url="https://openrouter.ai/api/v1",
        max_retries=3,
    )
    
def compress_context_model() -> ChatOpenAI:
    
    return ChatOpenAI(
        model="deepseek/deepseek-v4.1-flash",
        temperature=0.3,
        openai_api_key=settings.llm_token, #type: ignore
        base_url="https://openrouter.ai/api/v1",
        max_retries=3,
    )

if __name__ == "__main__":
    from rich import print
    
    llm = load_llm()
    
    result = llm.invoke("Olá testando llm como vc aceita vide base64 ou url?")
    
    print(result)