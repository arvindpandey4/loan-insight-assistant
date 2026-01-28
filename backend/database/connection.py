import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

# MongoDB connection instance
_client: Optional[AsyncIOMotorClient] = None
_db = None


async def connect_to_mongo():
    """Initialize MongoDB connection"""
    global _client, _db
    
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")
    
    _client = AsyncIOMotorClient(mongo_uri)
    _db = _client.loan_insight_db  # Database name
    
    # Verify connection
    try:
        await _client.admin.command('ping')
        print("[OK] Connected to MongoDB successfully")
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        raise e
    
    return _db


async def close_mongo_connection():
    """Close MongoDB connection"""
    global _client
    if _client:
        _client.close()
        print("[OK] MongoDB connection closed")


def get_database():
    """Get the database instance"""
    global _db
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return _db


def get_collection(collection_name: str):
    """Get a collection from the database"""
    db = get_database()
    return db[collection_name]
