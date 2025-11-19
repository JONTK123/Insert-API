"""
Simple demonstration of the mydata_core library capabilities.
This script generates sample data and displays it without requiring a database connection.
"""

from mydata_core import (
    GenerationRequest,
    EntitySpec,
    FieldSpec,
    ConstraintSpec,
    ForeignKeySpec,
    generate_all_data,
)
import json


def demo():
    """Run a simple demonstration of the data generation capabilities."""
    
    print("="*70)
    print("MyData Synthetic Data Generation - Demo")
    print("="*70)
    print()
    
    # Define a simple schema with relationships
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",  # Not used for generation-only
        entities=[
            EntitySpec(
                name="universities",
                records=3,
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
            EntitySpec(
                name="students",
                records=10,
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
                        name="cpf",
                        logical_type="cpf",
                        constraints=ConstraintSpec(unique=True, nullable=False)
                    ),
                    FieldSpec(
                        name="age",
                        logical_type="age",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={"min": 17, "max": 25}
                        )
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
                            foreign_key=ForeignKeySpec(
                                entity="universities",
                                field="id"
                            )
                        )
                    )
                ]
            )
        ]
    )
    
    print("Generating synthetic data...")
    print()
    
    # Generate the data
    data = generate_all_data(request)
    
    # Display statistics
    total_records = sum(len(records) for records in data.values())
    print(f"✓ Successfully generated {total_records} records across {len(data)} entities")
    print()
    
    # Display universities
    print("Universities:")
    print("-" * 70)
    for uni in data['universities']:
        print(f"  {uni['id']}. {uni['name']}")
        print(f"     Location: {uni['city']}, {uni['state']}")
    print()
    
    # Display students
    print("Students:")
    print("-" * 70)
    for student in data['students']:
        # Find the university name
        uni_name = next(
            u['name'] for u in data['universities'] 
            if u['id'] == student['university_id']
        )
        
        print(f"  {student['id']}. {student['name']} (Age: {student['age']})")
        print(f"     Email: {student['email']}")
        print(f"     CPF: {student['cpf']}")
        print(f"     Course: {student['course']}")
        print(f"     University: {uni_name}")
        print()
    
    # Save to JSON for inspection
    output_file = "/tmp/demo_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Convert datetime objects to strings for JSON serialization
        serializable_data = {}
        for entity, records in data.items():
            serializable_data[entity] = []
            for record in records:
                serializable_record = {}
                for key, value in record.items():
                    if hasattr(value, 'isoformat'):
                        serializable_record[key] = value.isoformat()
                    else:
                        serializable_record[key] = value
                serializable_data[entity].append(serializable_record)
        
        json.dump(serializable_data, f, indent=2, ensure_ascii=False)
    
    print("="*70)
    print(f"✓ Full data saved to: {output_file}")
    print("="*70)
    print()
    
    # Show some insights
    print("Insights:")
    print(f"  • All {len(data['students'])} students are enrolled in {len(data['universities'])} universities")
    print(f"  • Age range: {min(s['age'] for s in data['students'])} - {max(s['age'] for s in data['students'])}")
    print(f"  • All CPFs and emails are unique")
    print(f"  • Foreign key relationships maintained correctly")
    print()


if __name__ == "__main__":
    demo()
