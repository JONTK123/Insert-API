"""
MongoDB database adapter for inserting generated data.
"""

from typing import Any, Dict, List
from pymongo import MongoClient
from datetime import datetime


class MongoAdapter:
    """Adapter for MongoDB database operations."""
    
    def __init__(self, connection_uri: str):
        """Initialize MongoDB connection."""
        self.client = MongoClient(connection_uri)
        # Extract database name from URI or use default
        if "/" in connection_uri.split("://")[1]:
            db_name = connection_uri.split("/")[-1].split("?")[0]
            if db_name:
                self.db = self.client[db_name]
            else:
                self.db = self.client["mydata"]
        else:
            self.db = self.client["mydata"]
    
    def _convert_types(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Python types to MongoDB-compatible types."""
        converted = {}
        for key, value in record.items():
            if value is None:
                converted[key] = None
            elif isinstance(value, (datetime,)):
                converted[key] = value
            else:
                converted[key] = value
        return converted
    
    def insert_data(self, collection_name: str, records: List[Dict[str, Any]]) -> int:
        """
        Insert records into MongoDB collection.
        
        Args:
            collection_name: Name of the collection
            records: List of record dictionaries
            
        Returns:
            Number of records inserted
        """
        if not records:
            return 0
        
        collection = self.db[collection_name]
        
        # Convert records to MongoDB-compatible format
        converted_records = [self._convert_types(record) for record in records]
        
        # Insert in batches
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(converted_records), batch_size):
            batch = converted_records[i:i + batch_size]
            result = collection.insert_many(batch)
            total_inserted += len(result.inserted_ids)
        
        return total_inserted
    
    def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()
