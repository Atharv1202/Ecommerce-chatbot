import os
import uuid
from datetime import datetime
from email import message

import requests
from database import (conversations_collection, messages_collection,
                      users_collection)
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Message

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        context = ""
        top_product = get_top_product()
        if top_product:
            context += f"Top-selling product:{top_product['name']} (Rs{top_product['price']})\n"

        full_prompt + f"{context}User asked:{message}"
        ai_response = query_groq(full_prompt)

        messages_collection.insert_one({
            "conversation_id":conversation_id,
            "sender":"user",
            "message":message,
            "timestamp":datetime.utcnow()
    })
    ai_response = query_groq(message)
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


def get_top_product():
    top = db.products.find().sort("sold_count", -1).limit(1)
    return top[0] if top else None


def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization":f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type":"application/json"
    }
    payload = {
        "model":"mixtral-8x7b-32768",
        "messages": [
            {"role":"system", "content": "you are a helpful e-commerce assistant. If unclear,ask Followup questions"},
            {"role":"user", "content":prompt}
        ]
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json()['choices'][0]['messages']['content']

