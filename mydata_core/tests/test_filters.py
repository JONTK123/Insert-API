"""
Tests for data generation filters (allowed_values).
"""

import pytest
from mydata_core.core.models import (
    FieldSpec,
    EntitySpec,
    GenerationRequest,
    ConstraintSpec,
)
from mydata_core.core.generator import DataGenerator, generate_all_data


def test_simple_filter():
    """Test that allowed_values filter restricts generated values."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=20,
        fields=[
            FieldSpec(
                name="city",
                logical_type="city",
                constraints=ConstraintSpec(
                    nullable=False,
                    extra={
                        "allowed_values": ["Campinas", "São Paulo", "Santos"]
                    }
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    cities = [record["city"] for record in records]
    
    # All cities should be one of the allowed values
    allowed = {"Campinas", "São Paulo", "Santos"}
    assert all(city in allowed for city in cities), f"Found unexpected cities: {set(cities) - allowed}"
    
    # Should use all allowed values (with 20 records, very likely)
    assert len(set(cities)) >= 2, "Should use multiple allowed values"


def test_category_filter():
    """Test filtering business categories."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=15,
        fields=[
            FieldSpec(
                name="category",
                logical_type="business_category",
                constraints=ConstraintSpec(
                    nullable=False,
                    extra={
                        "allowed_values": ["Restaurante", "Bar"]
                    }
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    categories = [record["category"] for record in records]
    
    # All categories should be one of the allowed values
    allowed = {"Restaurante", "Bar"}
    assert all(cat in allowed for cat in categories)


def test_single_value_filter():
    """Test filter with only one allowed value."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=10,
        fields=[
            FieldSpec(
                name="university",
                logical_type="university_name",
                constraints=ConstraintSpec(
                    nullable=False,
                    extra={
                        "allowed_values": ["Universidade Estadual de Campinas (UNICAMP)"]
                    }
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    universities = [record["university"] for record in records]
    
    # All should be exactly the one allowed value
    assert all(uni == "Universidade Estadual de Campinas (UNICAMP)" for uni in universities)


def test_mixed_filtered_and_unfiltered():
    """Test entity with both filtered and unfiltered fields."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=10,
        fields=[
            FieldSpec(
                name="city",
                logical_type="city",
                constraints=ConstraintSpec(
                    nullable=False,
                    extra={
                        "allowed_values": ["Campinas"]
                    }
                )
            ),
            FieldSpec(
                name="name",
                logical_type="name",
                constraints=ConstraintSpec(nullable=False)
                # No filter - should be random
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    
    # All cities should be Campinas (filtered)
    cities = [record["city"] for record in records]
    assert all(city == "Campinas" for city in cities)
    
    # Names should be diverse (not filtered)
    names = [record["name"] for record in records]
    assert len(set(names)) >= 5, "Names should be diverse without filter"


def test_filter_with_unique_constraint():
    """Test that filters work with unique constraints."""
    generator = DataGenerator()
    
    # With only 2 allowed values and unique constraint, we can only generate 2 records max
    entity = EntitySpec(
        name="test",
        records=2,
        fields=[
            FieldSpec(
                name="category",
                logical_type="business_category",
                constraints=ConstraintSpec(
                    unique=True,
                    nullable=False,
                    extra={
                        "allowed_values": ["Restaurante", "Bar"]
                    }
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    categories = [record["category"] for record in records]
    
    # Should have exactly 2 unique categories
    assert len(categories) == 2
    assert len(set(categories)) == 2
    assert set(categories) == {"Restaurante", "Bar"}


def test_numeric_filter():
    """Test that allowed_values works with numeric types too."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=10,
        fields=[
            FieldSpec(
                name="score",
                logical_type="integer",
                constraints=ConstraintSpec(
                    nullable=False,
                    extra={
                        "allowed_values": [1, 2, 3, 4, 5]
                    }
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    scores = [record["score"] for record in records]
    
    # All scores should be in the allowed list
    assert all(score in [1, 2, 3, 4, 5] for score in scores)


def test_empty_filter_ignored():
    """Test that empty allowed_values list is ignored."""
    generator = DataGenerator()
    
    entity = EntitySpec(
        name="test",
        records=5,
        fields=[
            FieldSpec(
                name="city",
                logical_type="city",
                constraints=ConstraintSpec(
                    nullable=False,
                    extra={
                        "allowed_values": []  # Empty list should be ignored
                    }
                )
            )
        ]
    )
    
    records = generator.generate_entity_data(entity)
    
    # Should generate normally (not restricted)
    assert len(records) == 5
    cities = [record["city"] for record in records]
    assert all(isinstance(city, str) for city in cities)


def test_filter_full_integration():
    """Full integration test with multiple filtered entities."""
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            EntitySpec(
                name="restaurants",
                records=10,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(
                            primary_key=True,
                            auto_increment=True
                        )
                    ),
                    FieldSpec(
                        name="city",
                        logical_type="city",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"allowed_values": ["Campinas"]}
                        )
                    ),
                    FieldSpec(
                        name="state",
                        logical_type="uf",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"allowed_values": ["SP"]}
                        )
                    )
                ]
            )
        ]
    )
    
    data = generate_all_data(request)
    
    # Verify all records have filtered values
    assert all(r["city"] == "Campinas" for r in data["restaurants"])
    assert all(r["state"] == "SP" for r in data["restaurants"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
