# Database module
from .connection import connect_to_mongo, close_mongo_connection, get_database, get_collection
from .user_repository import UserRepository
from .history_repository import HistoryRepository

__all__ = [
    "connect_to_mongo",
    "close_mongo_connection", 
    "get_database",
    "get_collection",
    "UserRepository",
    "HistoryRepository"
]
