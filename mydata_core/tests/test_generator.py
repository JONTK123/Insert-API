"""
Basic tests for the data generation engine.
"""

import pytest
from mydata_core.core.models import (
    FieldSpec,
    EntitySpec,
    GenerationRequest,
    ConstraintSpec,
    ForeignKeySpec,
)
from mydata_core.core.generator import DataGenerator, generate_all_data


def test_simple_data_generation():
    """Test generating data for a simple entity without relationships."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="users",
        records=10,
        fields=[
            FieldSpec(
                name="id",
                logical_type="integer",
                constraints=ConstraintSpec(primary_key=True, auto_increment=True)
            ),
            FieldSpec(
                name="name",
                logical_type="name",
                constraints=ConstraintSpec(nullable=False)
            ),
            FieldSpec(
                name="email",
                logical_type="email",
                constraints=ConstraintSpec(unique=True)
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    
    assert len(records) == 10
    assert all("id" in record for record in records)
    assert all("name" in record for record in records)
    assert all("email" in record for record in records)
    
    # Check auto-increment works
    ids = [record["id"] for record in records]
    assert ids == list(range(1, 11))
    
    # Check unique constraint
    emails = [record["email"] for record in records]
    assert len(emails) == len(set(emails))


def test_foreign_key_relationship():
    """Test generating data with foreign key relationships."""
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://test",
        entities=[
            EntitySpec(
                name="categories",
                records=5,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(primary_key=True, auto_increment=True)
                    ),
                    FieldSpec(
                        name="name",
                        logical_type="business_category",
                        constraints=ConstraintSpec(nullable=False)
                    )
                ]
            ),
            EntitySpec(
                name="products",
                records=20,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(primary_key=True, auto_increment=True)
                    ),
                    FieldSpec(
                        name="name",
                        logical_type="short_text",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="category_id",
                        logical_type="integer",
                        constraints=ConstraintSpec(
                            nullable=False,
                            foreign_key=ForeignKeySpec(entity="categories", field="id")
                        )
                    )
                ]
            )
        ]
    )
    
    data = generate_all_data(request)
    
    # Check both entities generated
    assert "categories" in data
    assert "products" in data
    assert len(data["categories"]) == 5
    assert len(data["products"]) == 20
    
    # Check foreign key values are valid
    category_ids = {record["id"] for record in data["categories"]}
    product_category_ids = {record["category_id"] for record in data["products"]}
    
    # All product category_ids should reference existing categories
    assert product_category_ids.issubset(category_ids)


def test_brazilian_providers():
    """Test Brazilian-specific data types."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="users_br",
        records=5,
        fields=[
            FieldSpec(name="cpf", logical_type="cpf", constraints=ConstraintSpec(nullable=False)),
            FieldSpec(name="cnpj", logical_type="cnpj", constraints=ConstraintSpec(nullable=False)),
            FieldSpec(name="uf", logical_type="uf", constraints=ConstraintSpec(nullable=False)),
            FieldSpec(name="university", logical_type="university_name", constraints=ConstraintSpec(nullable=False)),
            FieldSpec(name="course", logical_type="course_name", constraints=ConstraintSpec(nullable=False)),
        ]
    )
    
    records = generator.generate_entity_data(entity)
    
    assert len(records) == 5
    
    # Check CPF format (XXX.XXX.XXX-XX)
    for record in records:
        cpf = record["cpf"]
        assert cpf is not None, "CPF should not be None"
        assert len(cpf) == 14
        assert cpf[3] == "." and cpf[7] == "." and cpf[11] == "-"
        
        # Check CNPJ format (XX.XXX.XXX/XXXX-XX)
        cnpj = record["cnpj"]
        assert cnpj is not None, "CNPJ should not be None"
        assert len(cnpj) == 18
        assert cnpj[2] == "." and cnpj[6] == "." and cnpj[10] == "/" and cnpj[15] == "-"
        
        # Check UF is valid Brazilian state
        assert record["uf"] is not None, "UF should not be None"
        assert len(record["uf"]) == 2
        assert record["uf"].isupper()


def test_unique_constraint():
    """Test that unique constraint generates unique values."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=50,
        fields=[
            FieldSpec(
                name="email",
                logical_type="email",
                constraints=ConstraintSpec(unique=True)
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    emails = [record["email"] for record in records]
    
    # All emails should be unique
    assert len(emails) == len(set(emails))


def test_nullable_fields():
    """Test that nullable fields sometimes generate None."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=100,
        fields=[
            FieldSpec(
                name="optional_field",
                logical_type="text",
                constraints=ConstraintSpec(nullable=True, unique=False)  # Make sure unique is false
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    values = [record["optional_field"] for record in records]
    
    # Count None values - with 100 records and 10% null rate, should have some nulls
    none_count = sum(1 for v in values if v is None)
    assert none_count > 0, "Expected at least some null values with nullable=True"


def test_entity_ordering_with_dependencies():
    """Test that entities are ordered correctly based on dependencies."""
    generator = DataGenerator()
    
    entities = [
        EntitySpec(
            name="products",
            records=10,
            fields=[
                FieldSpec(name="id", logical_type="integer", constraints=ConstraintSpec(primary_key=True)),
                FieldSpec(
                    name="category_id",
                    logical_type="integer",
                    constraints=ConstraintSpec(foreign_key=ForeignKeySpec(entity="categories", field="id"))
                )
            ]
        ),
        EntitySpec(
            name="categories",
            records=5,
            fields=[
                FieldSpec(name="id", logical_type="integer", constraints=ConstraintSpec(primary_key=True))
            ]
        )
    ]
    
    ordered = generator.resolve_entity_order(entities)
    
    # Categories should come before products
    assert ordered[0].name == "categories"
    assert ordered[1].name == "products"


def test_numeric_ranges():
    """Test that numeric types respect min/max constraints."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=20,
        fields=[
            FieldSpec(
                name="age",
                logical_type="integer",
                constraints=ConstraintSpec(
                    nullable=False,  # Ensure not nullable
                    extra={"min": 18, "max": 25}
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    ages = [record["age"] for record in records]
    
    # All ages should be in range and not None
    assert all(age is not None for age in ages), "Ages should not be None"
    assert all(18 <= age <= 25 for age in ages), f"Ages should be between 18 and 25, got {ages}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
