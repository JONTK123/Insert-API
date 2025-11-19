"""
Pydantic models for data generation configuration and responses.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ForeignKeySpec(BaseModel):
    """Foreign key specification pointing to another entity's field."""
    entity: str = Field(..., description="Name of the referenced entity")
    field: str = Field(..., description="Name of the referenced field")


class ConstraintSpec(BaseModel):
    """Field constraints specification."""
    primary_key: bool = Field(default=False, description="Is this field a primary key")
    auto_increment: bool = Field(default=False, description="Should auto-increment (only for integers)")
    unique: bool = Field(default=False, description="Should values be unique")
    nullable: bool = Field(default=True, description="Can this field be null")
    foreign_key: Optional[ForeignKeySpec] = Field(default=None, description="Foreign key reference")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Extra metadata (ranges, enums, etc)")


class FieldSpec(BaseModel):
    """Specification for a single field in an entity."""
    name: str = Field(..., description="Field name")
    logical_type: str = Field(..., description="Logical type for data generation")
    constraints: ConstraintSpec = Field(default_factory=ConstraintSpec, description="Field constraints")


class EntitySpec(BaseModel):
    """Specification for an entity (table/collection)."""
    name: str = Field(..., description="Entity name (table/collection name)")
    records: int = Field(..., gt=0, description="Number of records to generate")
    fields: List[FieldSpec] = Field(..., description="List of field specifications")


class GenerationRequest(BaseModel):
    """Request for generating and inserting synthetic data."""
    database_type: str = Field(..., pattern="^(postgresql|mongodb)$", description="Database type")
    connection_uri: str = Field(..., description="Database connection URI")
    entities: List[EntitySpec] = Field(..., description="List of entities to generate")
    total_records: Optional[int] = Field(default=None, description="Optional total records validation")


class GenerationResponse(BaseModel):
    """Response from data generation and insertion."""
    success: bool = Field(..., description="Whether the operation was successful")
    database_type: str = Field(..., description="Database type used")
    inserted_counts: Dict[str, int] = Field(..., description="Number of records inserted per entity")
    message: str = Field(..., description="Summary message")
    errors: Optional[List[str]] = Field(default=None, description="List of errors if any")
