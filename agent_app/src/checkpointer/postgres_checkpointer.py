from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from config import load_settings

settings = load_settings()

@asynccontextmanager
async def start_postgres_checkpointer() ->  AsyncGenerator[AsyncPostgresSaver, None]:
    async with AsyncPostgresSaver.from_conn_string(settings.uri_checkpointer) as checkpointer:
        
        await checkpointer.setup()

        yield checkpointer
