"""
Example: Using mydata_core as a Python library
"""

from mydata_core import (
    GenerationRequest,
    EntitySpec,
    FieldSpec,
    ConstraintSpec,
    ForeignKeySpec,
    generate_all_data,
    generate_and_insert,
)


def example_generate_data_only():
    """Example: Generate data without inserting into database."""
    print("\n=== Example 1: Generate data only ===\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",  # Not used when only generating
        entities=[
            EntitySpec(
                name="users",
                records=5,
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
                        constraints=ConstraintSpec(unique=True, nullable=False)
                    ),
                    FieldSpec(
                        name="cpf",
                        logical_type="cpf",
                        constraints=ConstraintSpec(unique=True, nullable=False)
                    ),
                    FieldSpec(
                        name="age",
                        logical_type="age",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"min": 18, "max": 65}
                        )
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Display results
    print(f"Generated {len(data['users'])} users:")
    for i, user in enumerate(data['users'], 1):
        print(f"\nUser {i}:")
        for key, value in user.items():
            print(f"  {key}: {value}")


def example_with_relationships():
    """Example: Generate data with foreign key relationships."""
    print("\n=== Example 2: Data with relationships ===\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            # Parent entity
            EntitySpec(
                name="universities",
                records=3,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(primary_key=True, auto_increment=True)
                    ),
                    FieldSpec(
                        name="name",
                        logical_type="university_name",
                        constraints=ConstraintSpec(unique=True, nullable=False)
                    ),
                    FieldSpec(
                        name="city",
                        logical_type="city",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="state",
                        logical_type="uf",
                        constraints=ConstraintSpec(nullable=False)
                    )
                ]
            ),
            # Child entity with foreign key
            EntitySpec(
                name="students",
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
                        constraints=ConstraintSpec(unique=True, nullable=False)
                    ),
                    FieldSpec(
                        name="course",
                        logical_type="course_name",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="university_id",
                        logical_type="integer",
                        constraints=ConstraintSpec(
                            nullable=False,
                            foreign_key=ForeignKeySpec(entity="universities", field="id")
                        )
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Display results
    print(f"Generated {len(data['universities'])} universities:")
    for uni in data['universities']:
        print(f"  - {uni['name']} ({uni['city']}, {uni['state']})")
    
    print(f"\nGenerated {len(data['students'])} students:")
    for student in data['students']:
        uni_id = student['university_id']
        uni_name = next(u['name'] for u in data['universities'] if u['id'] == uni_id)
        print(f"  - {student['name']} ({student['course']}) at {uni_name}")


def example_brazilian_data():
    """Example: Generate Brazilian-specific data."""
    print("\n=== Example 3: Brazilian data types ===\n")
    
    request = GenerationRequest(
        database_type="mongodb",
        connection_uri="mongodb://dummy",
        entities=[
            EntitySpec(
                name="establishments",
                records=5,
                fields=[
                    FieldSpec(
                        name="name",
                        logical_type="company",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="cnpj",
                        logical_type="cnpj",
                        constraints=ConstraintSpec(unique=True, nullable=False)
                    ),
                    FieldSpec(
                        name="category",
                        logical_type="business_category",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="address",
                        logical_type="address",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="opening_hours",
                        logical_type="opening_hours",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="owner_name",
                        logical_type="name",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="owner_cpf",
                        logical_type="cpf",
                        constraints=ConstraintSpec(nullable=False)
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Display results
    print(f"Generated {len(data['establishments'])} establishments:")
    for est in data['establishments']:
        print(f"\n{est['name']} ({est['category']})")
        print(f"  CNPJ: {est['cnpj']}")
        print(f"  Hours: {est['opening_hours']}")
        print(f"  Owner: {est['owner_name']} (CPF: {est['owner_cpf']})")
        print(f"  Address: {est['address']}")


if __name__ == "__main__":
    # Run examples
    example_generate_data_only()
    example_with_relationships()
    example_brazilian_data()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60 + "\n")
