# ONEFORALL/mongo.py
from pymongo import MongoClient
import os

# ────────────────────────────
# MongoDB connection
# ────────────────────────────
# Make sure you set MONGO_URL in your .env file
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster")  # e.g. mongodb+srv://username:password@cluster.mongodb.net

if not MONGO_URL:
    raise Exception("❌ MONGO_URL not set in environment variables")

# Connect to MongoDB cluster
cluster = MongoClient(MONGO_URL)

# Database for your Waifu bot
db = cluster["TEAMZYRO_WAIFU"]

# ────────────────────────────
# Collections
# ────────────────────────────
# Waifu auto-upload / GLOGS channel logs
waifu_logs = db.waifu_logs  # stores {msg_id, channel_id}

# Economy system
roshni_economy = db.roshni_economy  # user balances, kills, deaths, etc
roshni_cooldowns = db.roshni_cooldowns  # daily, rob, gift, shield timers
roshni_inventory = db.roshni_inventory  # items owned by users

# Optional: you can add more collections here if needed
