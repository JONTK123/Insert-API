"""
Core data generation engine with Faker integration.
"""

import random
from typing import Any, Dict, List, Optional, Set, Tuple
from faker import Faker
from mydata_core.core.models import (
    EntitySpec,
    FieldSpec,
    GenerationRequest,
    GenerationResponse,
)
from mydata_core.providers.brazilian import BrazilianProvider


class DataGenerator:
    """Core engine for generating synthetic data."""
    
    def __init__(self, locale: str = "pt_BR"):
        """Initialize the data generator with Faker and custom providers."""
        self.fake = Faker(locale)
        self.fake.add_provider(BrazilianProvider)
        self.generated_data: Dict[str, List[Dict[str, Any]]] = {}
        self.pk_values: Dict[str, List[Any]] = {}
        self.unique_values: Dict[str, Set[Any]] = {}
        self.auto_increment_counters: Dict[str, int] = {}
    
    def resolve_entity_order(self, entities: List[EntitySpec]) -> List[EntitySpec]:
        """
        Resolve the correct order for generating entities based on foreign key dependencies.
        Entities with no dependencies come first.
        """
        entity_map = {entity.name: entity for entity in entities}
        dependencies: Dict[str, Set[str]] = {entity.name: set() for entity in entities}
        
        # Build dependency graph
        for entity in entities:
            for field in entity.fields:
                if field.constraints.foreign_key:
                    ref_entity = field.constraints.foreign_key.entity
                    if ref_entity in entity_map and ref_entity != entity.name:
                        dependencies[entity.name].add(ref_entity)
        
        # Topological sort
        ordered = []
        visited = set()
        temp_visited = set()
        
        def visit(name: str):
            if name in temp_visited:
                raise ValueError(f"Circular dependency detected involving entity: {name}")
            if name in visited:
                return
            
            temp_visited.add(name)
            for dep in dependencies[name]:
                visit(dep)
            temp_visited.remove(name)
            visited.add(name)
            ordered.append(entity_map[name])
        
        for entity in entities:
            if entity.name not in visited:
                visit(entity.name)
        
        return ordered
    
    def generate_value(self, field: FieldSpec, entity_name: str, record_index: int) -> Any:
        """Generate a single value based on field specification."""
        constraints = field.constraints
        field_key = f"{entity_name}.{field.name}"
        
        # Handle auto-increment
        if constraints.auto_increment:
            if field_key not in self.auto_increment_counters:
                self.auto_increment_counters[field_key] = 1
            value = self.auto_increment_counters[field_key]
            self.auto_increment_counters[field_key] += 1
            return value
        
        # Handle nullable early (but not for PKs, FKs, or unique fields)
        if constraints.nullable and not constraints.primary_key and not constraints.unique and not constraints.foreign_key:
            if random.random() < 0.1:  # 10% chance of null
                return None
        
        # Handle foreign keys
        if constraints.foreign_key:
            fk = constraints.foreign_key
            ref_key = f"{fk.entity}.{fk.field}"
            if ref_key not in self.pk_values or not self.pk_values[ref_key]:
                raise ValueError(f"No values available for foreign key reference: {ref_key}")
            return random.choice(self.pk_values[ref_key])
        
        # Generate value based on logical type
        value = self._generate_by_type(field.logical_type, constraints.extra)
        
        # Handle unique constraint - use Faker's unique provider for better uniqueness
        if constraints.unique:
            if field_key not in self.unique_values:
                self.unique_values[field_key] = set()
            
            max_attempts = 1000
            attempts = 0
            while value in self.unique_values[field_key] and attempts < max_attempts:
                value = self._generate_by_type(field.logical_type, constraints.extra)
                attempts += 1
            
            if attempts == max_attempts:
                # Append index to ensure uniqueness
                value = f"{value}_{record_index}"
            
            self.unique_values[field_key].add(value)
        
        return value
    
    def _generate_by_type(self, logical_type: str, extra: Dict[str, Any]) -> Any:
        """Generate value based on logical type using Faker or custom logic."""
        
        # Brazilian specific types
        if logical_type == "cpf":
            return self.fake.cpf()
        elif logical_type == "cnpj":
            return self.fake.cnpj()
        elif logical_type == "uf":
            return self.fake.uf()
        elif logical_type == "university_name":
            return self.fake.university_name()
        elif logical_type == "course_name":
            return self.fake.course_name()
        elif logical_type == "business_category":
            return self.fake.business_category()
        elif logical_type == "preference_type":
            return self.fake.preference_type()
        elif logical_type == "preference_name":
            pref_type = extra.get("preference_type")
            return self.fake.preference_name(pref_type)
        elif logical_type == "opening_hours":
            return self.fake.opening_hours()
        elif logical_type == "password_hash":
            return self.fake.password_hash()
        
        # Identity / people
        elif logical_type == "name":
            return self.fake.name()
        elif logical_type == "first_name":
            return self.fake.first_name()
        elif logical_type == "last_name":
            return self.fake.last_name()
        
        # Contact / internet
        elif logical_type == "email":
            return self.fake.email()
        elif logical_type == "username":
            return self.fake.user_name()
        elif logical_type == "phone":
            return self.fake.phone_number()
        elif logical_type == "ip_address":
            return self.fake.ipv4()
        elif logical_type == "url":
            return self.fake.url()
        elif logical_type == "domain":
            return self.fake.domain_name()
        
        # Location / addresses
        elif logical_type == "address":
            return self.fake.address()
        elif logical_type == "street_name":
            return self.fake.street_name()
        elif logical_type == "street_address":
            return self.fake.street_address()
        elif logical_type == "city":
            return self.fake.city()
        elif logical_type == "country":
            return self.fake.country()
        elif logical_type == "postcode":
            return self.fake.postcode()
        elif logical_type == "latitude":
            return float(self.fake.latitude())
        elif logical_type == "longitude":
            return float(self.fake.longitude())
        
        # Company / work
        elif logical_type == "company":
            return self.fake.company()
        elif logical_type == "job_title":
            return self.fake.job()
        
        # Dates / time
        elif logical_type == "date":
            return self.fake.date()
        elif logical_type == "datetime":
            return self.fake.date_time()
        elif logical_type == "date_past":
            return self.fake.date_between(start_date="-2y", end_date="today")
        elif logical_type == "date_future":
            return self.fake.date_between(start_date="today", end_date="+2y")
        
        # Numeric
        elif logical_type == "integer":
            min_val = extra.get("min", 0)
            max_val = extra.get("max", 100)
            return self.fake.random_int(min=min_val, max=max_val)
        elif logical_type == "float":
            min_val = extra.get("min", 0.0)
            max_val = extra.get("max", 100.0)
            return self.fake.pyfloat(min_value=min_val, max_value=max_val, right_digits=2)
        elif logical_type == "price":
            return float(self.fake.pydecimal(left_digits=5, right_digits=2, positive=True))
        elif logical_type == "age":
            min_age = extra.get("min", 17)
            max_age = extra.get("max", 60)
            return self.fake.random_int(min=min_age, max=max_age)
        
        # Weight/ratings
        elif logical_type == "weight_1_5":
            return self.fake.random_int(min=1, max=5)
        elif logical_type == "rating_1_5":
            return self.fake.pyfloat(min_value=1.0, max_value=5.0, right_digits=1)
        elif logical_type == "similarity_score":
            return self.fake.pyfloat(min_value=0.0, max_value=1.0, right_digits=2)
        
        # Text
        elif logical_type == "short_text":
            return self.fake.sentence()
        elif logical_type == "text":
            return self.fake.text(max_nb_chars=200)
        elif logical_type == "long_text":
            return self.fake.text(max_nb_chars=1000)
        
        # Others
        elif logical_type == "uuid":
            return self.fake.uuid4()
        elif logical_type == "boolean":
            return self.fake.boolean()
        elif logical_type == "color_name":
            return self.fake.color_name()
        elif logical_type == "hex_color":
            return self.fake.hex_color()
        
        else:
            # Default to text
            return self.fake.text(max_nb_chars=100)
    
    def generate_entity_data(self, entity: EntitySpec) -> List[Dict[str, Any]]:
        """Generate all records for a single entity."""
        records = []
        
        for i in range(entity.records):
            record = {}
            for field in entity.fields:
                value = self.generate_value(field, entity.name, i)
                record[field.name] = value
                
                # Store primary key values for foreign key references
                if field.constraints.primary_key:
                    pk_key = f"{entity.name}.{field.name}"
                    if pk_key not in self.pk_values:
                        self.pk_values[pk_key] = []
                    self.pk_values[pk_key].append(value)
            
            records.append(record)
        
        return records
    
    def generate_all_data(self, request: GenerationRequest) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate data for all entities in the correct order.
        Returns a dictionary mapping entity names to their generated records.
        """
        # Reset state
        self.generated_data = {}
        self.pk_values = {}
        self.unique_values = {}
        self.auto_increment_counters = {}
        
        # Resolve dependency order
        ordered_entities = self.resolve_entity_order(request.entities)
        
        # Generate data for each entity
        for entity in ordered_entities:
            records = self.generate_entity_data(entity)
            self.generated_data[entity.name] = records
        
        return self.generated_data


def generate_all_data(request: GenerationRequest) -> Dict[str, List[Dict[str, Any]]]:
    """
    Public API: Generate synthetic data for all entities.
    
    Args:
        request: Generation request with entity specifications
        
    Returns:
        Dictionary mapping entity names to lists of generated records
    """
    generator = DataGenerator()
    return generator.generate_all_data(request)


def generate_and_insert(request: GenerationRequest) -> GenerationResponse:
    """
    Public API: Generate and insert synthetic data into the specified database.
    
    Args:
        request: Generation request with database connection and entity specifications
        
    Returns:
        Generation response with insertion counts and status
    """
    from mydata_core.db.postgres import PostgresAdapter
    from mydata_core.db.mongo import MongoAdapter
    
    try:
        # Generate data
        generator = DataGenerator()
        data = generator.generate_all_data(request)
        
        # Insert into database
        inserted_counts = {}
        
        if request.database_type == "postgresql":
            adapter = PostgresAdapter(request.connection_uri)
            for entity_name, records in data.items():
                # Find entity spec for field information
                entity_spec = next(e for e in request.entities if e.name == entity_name)
                count = adapter.insert_data(entity_name, records, entity_spec)
                inserted_counts[entity_name] = count
            adapter.close()
            
        elif request.database_type == "mongodb":
            adapter = MongoAdapter(request.connection_uri)
            for entity_name, records in data.items():
                count = adapter.insert_data(entity_name, records)
                inserted_counts[entity_name] = count
            adapter.close()
        
        total_inserted = sum(inserted_counts.values())
        
        return GenerationResponse(
            success=True,
            database_type=request.database_type,
            inserted_counts=inserted_counts,
            message=f"Successfully generated and inserted {total_inserted} records across {len(inserted_counts)} entities."
        )
        
    except Exception as e:
        return GenerationResponse(
            success=False,
            database_type=request.database_type,
            inserted_counts={},
            message=f"Failed to generate and insert data: {str(e)}",
            errors=[str(e)]
        )
