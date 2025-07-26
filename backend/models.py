from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    created_at: Optional[datetime] = None


class Conversation(BaseModel):
    user_id: str
    started_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None


class Message(BaseModel):
    conversation_id: str
    sender: str
    message: str
    timestamp: Optional[datetime] = None
