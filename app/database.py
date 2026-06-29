from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["healthcamp"]

# Collections
camps_collection = db["camps"]
patients_collection = db["patients"]
vitals_collection = db["vitals"]
followups_collection = db["followups"]

print("✅ Connected to MongoDB!")