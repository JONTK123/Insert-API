"""
MyData Core - Synthetic Data Generation Library

A comprehensive library for generating and inserting synthetic data into PostgreSQL and MongoDB databases.
"""

from mydata_core.core.models import (
    FieldSpec,
    EntitySpec,
    GenerationRequest,
    GenerationResponse,
    ConstraintSpec,
    ForeignKeySpec,
)
from mydata_core.core.generator import generate_all_data, generate_and_insert

__version__ = "0.1.0"
__all__ = [
    "FieldSpec",
    "EntitySpec", 
    "GenerationRequest",
    "GenerationResponse",
    "ConstraintSpec",
    "ForeignKeySpec",
    "generate_all_data",
    "generate_and_insert",
]
