import pandas as pd
from pymongo import Mongoclient

client = MongoClient ("mongodb://localhost:2701")
db = client["ecommerce"]
df = pd.read_csv("data/products.csv")
db.products.insert_many(df.to_dict("records"))

