from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from .connection import get_collection
from .history_schema import HistoryEntryCreate, HistoryEntryInDB, QueryType


class HistoryRepository:
    """Repository for query history database operations"""
    
    COLLECTION_NAME = "query_history"
    
    @classmethod
    def _get_collection(cls):
        return get_collection(cls.COLLECTION_NAME)
    
    @classmethod
    async def create_entry(cls, entry_data: HistoryEntryCreate) -> HistoryEntryInDB:
        """
        Create a new history entry
        
        Args:
            entry_data: History entry creation data
            
        Returns:
            Created history entry with database ID
        """
        collection = cls._get_collection()
        
        entry_dict = {
            "user_id": entry_data.user_id,
            "query": entry_data.query,
            "response": entry_data.response,
            "query_type": entry_data.query_type.value,
            "metadata": entry_data.metadata or {},
            "created_at": datetime.utcnow()
        }
        
        result = await collection.insert_one(entry_dict)
        entry_dict["_id"] = str(result.inserted_id)
        
        return HistoryEntryInDB(**entry_dict)
    
    @classmethod
    async def get_user_history(
        cls,
        user_id: str,
        limit: int = 50,
        skip: int = 0,
        query_type: Optional[QueryType] = None
    ) -> List[HistoryEntryInDB]:
        """
        Get history entries for a user
        
        Args:
            user_id: User's database ID
            limit: Maximum number of entries to return
            skip: Number of entries to skip (for pagination)
            query_type: Optional filter by query type
            
        Returns:
            List of history entries
        """
        collection = cls._get_collection()
        
        filter_query = {"user_id": user_id}
        if query_type:
            filter_query["query_type"] = query_type.value
        
        cursor = collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
        
        entries = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            entries.append(HistoryEntryInDB(**doc))
        
        return entries
    
    @classmethod
    async def get_entry_by_id(cls, entry_id: str) -> Optional[HistoryEntryInDB]:
        """
        Get a specific history entry by ID
        
        Args:
            entry_id: Entry's database ID
            
        Returns:
            History entry if found, None otherwise
        """
        collection = cls._get_collection()
        
        try:
            doc = await collection.find_one({"_id": ObjectId(entry_id)})
        except Exception:
            return None
        
        if doc:
            doc["_id"] = str(doc["_id"])
            return HistoryEntryInDB(**doc)
        
        return None
    
    @classmethod
    async def delete_entry(cls, entry_id: str, user_id: str) -> bool:
        """
        Delete a history entry (only if owned by user)
        
        Args:
            entry_id: Entry's database ID
            user_id: User's database ID (for ownership check)
            
        Returns:
            True if deleted, False otherwise
        """
        collection = cls._get_collection()
        
        try:
            result = await collection.delete_one({
                "_id": ObjectId(entry_id),
                "user_id": user_id
            })
            return result.deleted_count > 0
        except Exception:
            return False
    
    @classmethod
    async def delete_user_history(cls, user_id: str) -> int:
        """
        Delete all history entries for a user
        
        Args:
            user_id: User's database ID
            
        Returns:
            Number of deleted entries
        """
        collection = cls._get_collection()
        
        result = await collection.delete_many({"user_id": user_id})
        return result.deleted_count
    
    @classmethod
    async def get_user_history_count(cls, user_id: str) -> int:
        """
        Get total count of history entries for a user
        
        Args:
            user_id: User's database ID
            
        Returns:
            Count of history entries
        """
        collection = cls._get_collection()
        return await collection.count_documents({"user_id": user_id})
    
    @classmethod
    async def create_indexes(cls):
        """Create database indexes for better query performance"""
        collection = cls._get_collection()
        
        # Index on user_id for faster user history lookups
        await collection.create_index("user_id")
        
        # Compound index for user + created_at for sorted history
        await collection.create_index([("user_id", 1), ("created_at", -1)])
        
        # Index on query_type for filtering
        await collection.create_index("query_type")
        
        print("[OK] History collection indexes created")
