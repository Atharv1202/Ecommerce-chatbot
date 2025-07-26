import uuid
from datetime import datetime
from email import message

import requests
from database import (conversations_collection, messages_collection,
                      users_collection)
from fastapi import Body, FastAPI
from models import Message

app = FastAPI()


@app.post("/api/chat")
def chat(
    message:str=Body(...),
    conversation_id:str=Body(None),
    user_id:str=Body(...)
):
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        conversations_collection.insert_one({
            "_id": conversation_id,
            "user_id":user_id,
            "started_at": datetime.utcnow(),
            "last_updated":datetime.utcnow()
        })
    messages_collection.insert_one({
            "conversation_id":conversation_id,
            "sender":"user",
            "message":message,
            "timestamp":datetime.utcnow()
    })
    ai_response = "Thanks! WE'll get back shortly"
    messages_collection.insert_one({
        "conversation_id":conversation_id,
        "sender":"bot",
        "message":ai_response,
        "timestamp":datetime.utcnow()
        })
    conversations_collection.update_one(
        {"_id":conversation_id},
        {"$set": {"last_updated": datetime.utcnow()}}
    )
    return {"conversation_id":conversation_id, "response":ai_response}

