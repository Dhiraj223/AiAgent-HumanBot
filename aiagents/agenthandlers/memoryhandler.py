from agenthandlers.classhandler import Message
from typing import List
from mem0 import MemoryClient

class MemoryHandler:
    def __init__(self, mem0apikey):
        self.client = MemoryClient(api_key=mem0apikey)

    def update_memories(self, user_id : str, message: Message) :
        user_message = [{"role": message.role, "content": message.content}]
        self.client.add(user_message, user_id=user_id, output_format="v1.0")

    def get_memories(self, user_id:str) -> List :
        stored_memories = self.client.get_all(user_id=user_id, output_format="v1.0")
        memory = [data["memory"] for data in stored_memories]
        return memory