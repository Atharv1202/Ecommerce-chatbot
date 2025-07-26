from pymongo import MongoClient

client = MongoClient ("mongodb://localhost:27017")
db = client ["ecommerce"]
users_collection = db["users"]
conversations_collection = db["conversations"]
messages_collection = db["messages"]
