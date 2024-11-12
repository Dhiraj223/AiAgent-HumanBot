from typing import List, Dict, Optional
from agenthandlers.classhandler import Message, Persona
from agenthandlers.llmhandler import LLMHandler
from agenthandlers.personahandler import PersonaManager
from agenthandlers.memoryhandler import MemoryHandler
from agenthandlers.contexthandler import ContextHandler

class AIAgent():
    def __init__(
        self,
        llm_handler: LLMHandler,
        persona_manager: PersonaManager,
        memory_handler: MemoryHandler,
        context_handler : ContextHandler
    ):
        self.llm_handler = llm_handler
        self.persona_manager = persona_manager
        self.memory_handler = memory_handler
        self.context_handler = context_handler
        self.current_persona: Optional[Persona] = None

    def set_persona(self, persona_name: str) -> None:
        """Set the current persona for the agent"""
        if persona_name in self.persona_manager.personas:
            self.current_persona = self.persona_manager.personas[persona_name]
        else:
            raise ValueError(f"Persona '{persona_name}' not found")

    async def process_message(
        self,
        conversation_id : str,
        user_id: str,
        user_message: str,
        knowledge : List,
    ) -> str:
        message = Message(
            content=user_message,
            role="user"
        )
        self.context_handler.add_message(conversation_id=conversation_id, message=message)
        self.memory_handler.update_memories(user_id=user_id, message=message)
        memories = self.memory_handler.get_memories(user_id=user_id)
        context = self.context_handler.get_context(conversation_id=conversation_id)

        response_text = await self.llm_handler.generate_response(
            message=message,
            persona=self.current_persona,
            memories=memories,
            context=context,
            knowledge_base=knowledge
        )
        return response_text