# Database.py
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URI (heroku me set karo as env variable)
import os
MONGO_URI = os.getenv("mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # set in Heroku config vars

client = AsyncIOMotorClient(MONGO_URI)
db = client["TEAMZYRO"]  # database name

# Collections
user_collection = db["users"]         # users data
characters_col = db["characters"]     # waifu/characters data
