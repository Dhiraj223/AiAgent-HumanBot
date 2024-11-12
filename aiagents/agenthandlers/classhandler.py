from uuid import uuid4
from typing import List
from datetime import datetime
from pydantic import BaseModel

class Message(BaseModel):
    content: str
    role: str
    timestamp: datetime = datetime.now()
    message_id: str = str(uuid4())

class Persona(BaseModel):
    name: str
    description: str
    role: str
    personality_traits: List[str]
    communication_style: str
    domain_expertise: List[str]
    system_prompt: str

class Conversation(BaseModel):
    conversation_id: str = str(uuid4())
    messages: List[Message] = []
    user_id: str
    agent_id: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Agent(BaseModel):
    agent_id: str = str(uuid4())
    persona: Persona
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    created_by: str
    active: bool = True