from typing import Dict, List
from agenthandlers.classhandler import Message, Conversation

class ContextHandler:
    def __init__(self, max_context_length: int = 5):
        self.max_context_length = max_context_length
        self.conversations: Dict[str, Conversation] = {}

    def add_message(
        self,
        conversation_id: str,
        message: Message
    ) -> None:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation(
                conversation_id=conversation_id,
                messages=[],
                user_id=message.role,
                agent_id="default"
            )

        conversation = self.conversations[conversation_id]
        conversation.messages.append(message)

        if len(conversation.messages) > self.max_context_length:
            conversation.messages = conversation.messages[-self.max_context_length:]

    def get_context(
        self,
        conversation_id: str
    ) -> List[Dict]:
        if conversation_id not in self.conversations:
            return []

        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.conversations[conversation_id].messages
        ]