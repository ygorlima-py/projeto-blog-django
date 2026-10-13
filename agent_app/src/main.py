from agent import SupervisoryAgent, AgentBase
from infra import load_llm

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from rich import print
import asyncio


async def main(graph: AgentBase, user_input: str | Command, thread_id: str,):

    async for message_chunk, _ in graph.astream(user_input=user_input, thread_id=thread_id):
        if isinstance(message_chunk.content, str):
            print(message_chunk.content, end="", flush=True)

    interrupt = graph.get_pending_interrupt(thread_id)

    if interrupt is not None:
        action_request = interrupt.value["action_requests"][0]
        review_configs = interrupt.value["review_configs"][0]
        
        args = []
        for key, value in action_request.get("args", {}).items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    args.append(f"{nested_key}: {nested_value}")
            else:
                args.append(f"{key}: {value}")
            
        print(
            f"\nInterrupção pendente: {action_request.get("name", "")}"
            f"\nArgumentos: {', '.join(args)}"
            f"\nDecisão: {', '.join(review_configs.get("allowed_decisions"))}"
            )
    
if __name__ == "__main__":
    
    async def runner() -> None:
        graph = SupervisoryAgent(
            model=load_llm(),
            checkpointer=InMemorySaver(),
        )

        while True:
            user_input = input("\nVocê: ")

            if user_input.lower() in {"sair", "exit", "quit"}:
                break

            await main(
                graph,
                user_input,
                "teste",
            )
    asyncio.run(runner())
