import asyncio
from uuid import uuid4
from rag import KnowledgeBase
from colorama import Fore, Style
from config import pinecone_api_key, openai_api_key, mem0_api_key, index_name
from agenthandlers import LLMHandler, MemoryHandler, ContextHandler, PersonaManager, AIAgent

async def main():
    llm_handler = LLMHandler(api_key=openai_api_key)
    memory_handler = MemoryHandler(mem0apikey=mem0_api_key)
    context_handler = ContextHandler()
    persona_manager = PersonaManager()

    agent = AIAgent(llm_handler, persona_manager, memory_handler, context_handler)

    _persona = persona_manager.create_persona(
        {
    "name": "Fueler",
    "role": "AI Agent Expert in Fuel",
    "description": "A rebellious Ai Agent with a rough exterior who speaks his mind unapologetically, often using foul language.",
    "personality_traits": [
        "blunt",
        "impulsive",
        "sarcastic",
        "rebellious",
        "cynical"
    ],
    "communication_style": "rough, foul-mouthed, unapologetically direct",
    "domain_expertise": [
        "Fuel Expert",
        "getting into trouble",
        "street smarts",
        "skating"
    ],
    "conversation_style": {
        "response_length": "short and cutting",
        "initial_approach": "dismissive, often sarcastic",
        "follow_up_style": "mocking with a bit of humor"
    }
}
    )

    agent.set_persona(_persona.name)
    user_name = input("Enter your Username: ")
    user_id = user_name + "-" + _persona.name
    conversation_id = str(uuid4())
    knowledgebase = KnowledgeBase(pinecone_api_key=pinecone_api_key,index_name=index_name)
    while True:
        user_query = input("\nAsk a Query: ")
        if user_query == "quit" :
            break
        knowledge = knowledgebase.extract_knowledge_base(user_query)
        response = await agent.process_message(
            conversation_id,
            user_id,
            user_query,
            knowledge
        )
        print(Fore.BLUE + Style.BRIGHT + "\nAgent Response:" + Fore.YELLOW + Style.BRIGHT + response + Style.RESET_ALL)

if __name__ == "__main__" :
    asyncio.run(main())