"""
Example: Exporting generated data to SQL, MongoDB, CSV, and JSON formats.
"""

from mydata_core import (
    GenerationRequest,
    EntitySpec,
    FieldSpec,
    ConstraintSpec,
    generate_all_data,
    export_to_sql,
    export_to_mongodb,
    export_to_csv,
    export_to_json,
    export_all,
)


def example_sql_export():
    """Example: Generate data and export to SQL INSERT statements."""
    print("\n" + "="*70)
    print("Example 1: Export to SQL INSERT statements")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            EntitySpec(
                name="users",
                records=5,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(
                            primary_key=True,
                            auto_increment=True,
                            nullable=False
                        )
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
    
    # Export to SQL
    sql_commands = export_to_sql(data)
    
    print("Generated SQL Commands:")
    print("-" * 70)
    print(sql_commands)
    print()


def example_mongodb_export():
    """Example: Generate data and export to MongoDB insertMany commands."""
    print("\n" + "="*70)
    print("Example 2: Export to MongoDB insertMany commands")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="mongodb",
        connection_uri="mongodb://dummy",
        entities=[
            EntitySpec(
                name="products",
                records=5,
                fields=[
                    FieldSpec(
                        name="_id",
                        logical_type="integer",
                        constraints=ConstraintSpec(
                            primary_key=True,
                            auto_increment=True
                        )
                    ),
                    FieldSpec(
                        name="name",
                        logical_type="short_text",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="price",
                        logical_type="price",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="category",
                        logical_type="business_category",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="in_stock",
                        logical_type="boolean",
                        constraints=ConstraintSpec(nullable=False)
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Export to MongoDB
    mongo_commands = export_to_mongodb(data)
    
    print("Generated MongoDB Commands:")
    print("-" * 70)
    print(mongo_commands)
    print()


def example_csv_export():
    """Example: Generate data and export to CSV files."""
    print("\n" + "="*70)
    print("Example 3: Export to CSV files")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
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
                        name="age",
                        logical_type="age",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"min": 17, "max": 25}
                        )
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Export to CSV
    csv_files = export_to_csv(data, output_dir="/tmp/mydata_export")
    
    print("Generated CSV Files:")
    print("-" * 70)
    for entity, filepath in csv_files.items():
        print(f"  {entity}: {filepath}")
        
        # Show first few lines
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:6]  # Header + 5 records
            print(f"\n  Preview of {entity}.csv:")
            for line in lines:
                print(f"    {line.strip()}")
        print()


def example_json_export():
    """Example: Generate data and export to JSON files."""
    print("\n" + "="*70)
    print("Example 4: Export to JSON files")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            EntitySpec(
                name="restaurants",
                records=5,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(primary_key=True, auto_increment=True)
                    ),
                    FieldSpec(
                        name="name",
                        logical_type="company",
                        constraints=ConstraintSpec(nullable=False)
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
                        name="category",
                        logical_type="business_category",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"allowed_values": ["Restaurante", "Pizzaria"]}
                        )
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Export to JSON
    json_files = export_to_json(data, output_dir="/tmp/mydata_export")
    
    print("Generated JSON Files:")
    print("-" * 70)
    for entity, filepath in json_files.items():
        print(f"  {entity}: {filepath}")
        
        # Show content
        with open(filepath, 'r', encoding='utf-8') as f:
            import json
            content = json.load(f)
            print(f"\n  Content of {entity}.json ({len(content)} records):")
            for i, record in enumerate(content[:3], 1):  # Show first 3
                print(f"    {i}. {record}")
        print()


def example_export_all():
    """Example: Export to all formats at once."""
    print("\n" + "="*70)
    print("Example 5: Export to ALL formats at once")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            EntitySpec(
                name="campinas_restaurants",
                records=8,
                fields=[
                    FieldSpec(
                        name="id",
                        logical_type="integer",
                        constraints=ConstraintSpec(primary_key=True, auto_increment=True)
                    ),
                    FieldSpec(
                        name="name",
                        logical_type="company",
                        constraints=ConstraintSpec(nullable=False)
                    ),
                    FieldSpec(
                        name="category",
                        logical_type="business_category",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"allowed_values": ["Restaurante", "Pizzaria", "Lanchonete"]}
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
                        name="phone",
                        logical_type="phone",
                        constraints=ConstraintSpec(nullable=False)
                    )
                ]
            )
        ]
    )
    
    # Generate data
    data = generate_all_data(request)
    
    # Export to all formats
    results = export_all(data, output_dir="/tmp/mydata_export_all")
    
    print("Exported to ALL formats:")
    print("-" * 70)
    print(f"\n✓ SQL: {results['sql']}")
    print(f"✓ MongoDB: {results['mongodb']}")
    print(f"✓ CSV: {list(results['csv'].values())}")
    print(f"✓ JSON: {list(results['json'].values())}")
    print()
    
    # Show SQL commands preview
    with open(results['sql'], 'r', encoding='utf-8') as f:
        lines = f.readlines()[:20]
        print("\nSQL Commands Preview (first 20 lines):")
        print("-" * 70)
        for line in lines:
            print(line.rstrip())
    
    print("\n" + "="*70)
    print("✓ All files generated successfully!")
    print("="*70)


if __name__ == "__main__":
    # Run all examples
    example_sql_export()
    example_mongodb_export()
    example_csv_export()
    example_json_export()
    example_export_all()
    
    print("\n" + "="*70)
    print("✅ All export examples completed!")
    print("="*70)
    print("\nYou can now:")
    print("  - Copy SQL commands and run in your PostgreSQL database")
    print("  - Copy MongoDB commands and run in mongo shell")
    print("  - Import CSV files into any database")
    print("  - Use JSON files for data analysis or API testing")
    print()
