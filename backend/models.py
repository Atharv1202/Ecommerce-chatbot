from datetime import datetime
from turtle import st
from typing import Optional

from pydantic.main import BaseModel


class User(Basemodel):
    name:str
    email:str
    created_at: Optional[datetime] = None


class Converstaion(BaseModel):
    user_id:str
    started_at:Optional[datetime] = None
    last_updated:Optional[datetime] = None


class Message(BaseModel):
    converstaion_id:str
    sender:st
    message:str
    timestamp:OPtional[datetime] = None

