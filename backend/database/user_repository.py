from datetime import datetime
from typing import Optional
from bson import ObjectId
from .connection import get_collection
from .user_schema import UserCreate, UserInDB, UserUpdate, AuthProvider


class UserRepository:
    """Repository for user database operations"""
    
    COLLECTION_NAME = "users"
    
    @classmethod
    def _get_collection(cls):
        return get_collection(cls.COLLECTION_NAME)
    
    @classmethod
    async def create_user(cls, user_data: UserCreate) -> UserInDB:
        """
        Create a new user in the database
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user with database ID
        """
        collection = cls._get_collection()
        
        user_dict = {
            "email": user_data.email,
            "name": user_data.name,
            "picture": user_data.picture,
            "google_id": user_data.google_id,
            "auth_provider": user_data.auth_provider.value,
            "is_active": True,
            "is_verified": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": datetime.utcnow()
        }
        
        result = await collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        return UserInDB(**user_dict)
    
    @classmethod
    async def get_user_by_email(cls, email: str) -> Optional[UserInDB]:
        """
        Get a user by email address
        
        Args:
            email: User's email address
            
        Returns:
            User if found, None otherwise
        """
        collection = cls._get_collection()
        user_doc = await collection.find_one({"email": email})
        
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        
        return None
    
    @classmethod
    async def get_user_by_google_id(cls, google_id: str) -> Optional[UserInDB]:
        """
        Get a user by Google ID
        
        Args:
            google_id: User's Google ID
            
        Returns:
            User if found, None otherwise
        """
        collection = cls._get_collection()
        user_doc = await collection.find_one({"google_id": google_id})
        
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        
        return None
    
    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Optional[UserInDB]:
        """
        Get a user by database ID
        
        Args:
            user_id: User's database ID
            
        Returns:
            User if found, None otherwise
        """
        collection = cls._get_collection()
        
        try:
            user_doc = await collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        
        return None
    
    @classmethod
    async def update_user(cls, user_id: str, update_data: UserUpdate) -> Optional[UserInDB]:
        """
        Update a user's information
        
        Args:
            user_id: User's database ID
            update_data: Fields to update
            
        Returns:
            Updated user if found, None otherwise
        """
        collection = cls._get_collection()
        
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        update_dict["updated_at"] = datetime.utcnow()
        
        try:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": update_dict},
                return_document=True
            )
        except Exception:
            return None
        
        if result:
            result["_id"] = str(result["_id"])
            return UserInDB(**result)
        
        return None
    
    @classmethod
    async def update_last_login(cls, user_id: str) -> None:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User's database ID
        """
        collection = cls._get_collection()
        
        try:
            await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}}
            )
        except Exception:
            pass
    
    @classmethod
    async def find_or_create_google_user(
        cls,
        email: str,
        name: str,
        google_id: str,
        picture: Optional[str] = None
    ) -> tuple[UserInDB, bool]:
        """
        Find existing user or create new one from Google OAuth data
        
        Args:
            email: User's email
            name: User's display name
            google_id: Google account ID
            picture: Profile picture URL
            
        Returns:
            Tuple of (user, is_new_user)
        """
        # First try to find by Google ID
        existing_user = await cls.get_user_by_google_id(google_id)
        
        if existing_user:
            # Update last login
            await cls.update_last_login(existing_user.id)
            return existing_user, False
        
        # Try to find by email (user might have signed up differently before)
        existing_user = await cls.get_user_by_email(email)
        
        if existing_user:
            # Link Google account to existing user
            collection = cls._get_collection()
            await collection.update_one(
                {"_id": ObjectId(existing_user.id)},
                {
                    "$set": {
                        "google_id": google_id,
                        "picture": picture or existing_user.picture,
                        "last_login": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            existing_user.google_id = google_id
            existing_user.picture = picture or existing_user.picture
            return existing_user, False
        
        # Create new user
        new_user = await cls.create_user(UserCreate(
            email=email,
            name=name,
            picture=picture,
            google_id=google_id,
            auth_provider=AuthProvider.GOOGLE
        ))
        
        return new_user, True
    
    @classmethod
    async def delete_user(cls, user_id: str) -> bool:
        """
        Delete a user from the database
        
        Args:
            user_id: User's database ID
            
        Returns:
            True if deleted, False otherwise
        """
        collection = cls._get_collection()
        
        try:
            result = await collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    @classmethod
    async def create_indexes(cls):
        """Create database indexes for better query performance"""
        collection = cls._get_collection()
        
        # Unique index on email
        await collection.create_index("email", unique=True)
        
        # Index on google_id for faster OAuth lookups
        await collection.create_index("google_id", sparse=True)
        
        print("[OK] User collection indexes created")
