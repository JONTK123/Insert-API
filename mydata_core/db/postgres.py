"""
PostgreSQL database adapter for inserting generated data.
"""

from typing import Any, Dict, List
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, DateTime, Text, inspect
from sqlalchemy.sql import text
from mydata_core.core.models import EntitySpec, FieldSpec


class PostgresAdapter:
    """Adapter for PostgreSQL database operations."""
    
    def __init__(self, connection_uri: str):
        """Initialize PostgreSQL connection."""
        self.engine = create_engine(connection_uri)
        self.metadata = MetaData()
        self.connection = self.engine.connect()
    
    def _map_logical_type_to_sql(self, logical_type: str) -> Any:
        """Map logical type to SQLAlchemy column type."""
        # Numeric types
        if logical_type in ["integer", "age", "weight_1_5"]:
            return Integer
        elif logical_type in ["float", "price", "rating_1_5", "similarity_score", "latitude", "longitude"]:
            return Float
        
        # Boolean
        elif logical_type == "boolean":
            return Boolean
        
        # Date/time
        elif logical_type in ["date", "datetime", "date_past", "date_future"]:
            return DateTime
        
        # Long text
        elif logical_type in ["long_text", "text"]:
            return Text
        
        # Default to String
        else:
            return String(255)
    
    def create_table(self, entity_name: str, entity_spec: EntitySpec):
        """Create table if it doesn't exist."""
        inspector = inspect(self.engine)
        
        # Check if table already exists
        if inspector.has_table(entity_name):
            return
        
        columns = []
        for field in entity_spec.fields:
            col_type = self._map_logical_type_to_sql(field.logical_type)
            
            # Create column with constraints
            column = Column(
                field.name,
                col_type,
                primary_key=field.constraints.primary_key,
                unique=field.constraints.unique,
                nullable=field.constraints.nullable,
                autoincrement=field.constraints.auto_increment and field.constraints.primary_key
            )
            columns.append(column)
        
        # Create table
        table = Table(entity_name, self.metadata, *columns)
        self.metadata.create_all(self.engine)
    
    def insert_data(self, entity_name: str, records: List[Dict[str, Any]], entity_spec: EntitySpec) -> int:
        """
        Insert records into PostgreSQL table.
        
        Args:
            entity_name: Name of the table
            records: List of record dictionaries
            entity_spec: Entity specification for table creation
            
        Returns:
            Number of records inserted
        """
        if not records:
            return 0
        
        # Create table if needed
        self.create_table(entity_name, entity_spec)
        
        # Get table object
        table = Table(entity_name, self.metadata, autoload_with=self.engine)
        
        # Insert data in batches
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            # Filter out auto-increment fields if they should not be inserted
            filtered_batch = []
            for record in batch:
                filtered_record = {}
                for field in entity_spec.fields:
                    if field.name in record:
                        # Skip auto-increment PKs if the value is None or default
                        if field.constraints.auto_increment and field.constraints.primary_key:
                            continue
                        filtered_record[field.name] = record[field.name]
                filtered_batch.append(filtered_record)
            
            if filtered_batch:
                self.connection.execute(table.insert(), filtered_batch)
                self.connection.commit()
                total_inserted += len(filtered_batch)
        
        return total_inserted
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
