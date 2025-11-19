"""
Example: Using filters to restrict generated data to specific values.

This example shows how to use the 'allowed_values' filter to generate
data only with specific values (e.g., only restaurants in Campinas).
"""

from mydata_core import (
    GenerationRequest,
    EntitySpec,
    FieldSpec,
    ConstraintSpec,
    generate_all_data,
)


def example_filtered_restaurants():
    """Example: Generate restaurants only in Campinas, SP."""
    print("\n" + "="*70)
    print("Example 1: Restaurants ONLY in Campinas")
    print("="*70 + "\n")
    
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
                            auto_increment=True,
                            nullable=False
                        )
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
                            extra={
                                "allowed_values": ["Restaurante", "Pizzaria", "Lanchonete"]
                            }
                        )
                    ),
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
                        name="state",
                        logical_type="uf",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={
                                "allowed_values": ["SP"]
                            }
                        )
                    ),
                    FieldSpec(
                        name="neighborhood",
                        logical_type="text",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={
                                "allowed_values": [
                                    "Cambuí",
                                    "Centro",
                                    "Taquaral",
                                    "Barão Geraldo"
                                ]
                            }
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
    
    data = generate_all_data(request)
    
    print(f"Generated {len(data['restaurants'])} restaurants:\n")
    
    # Show that ALL restaurants are in Campinas
    for restaurant in data['restaurants']:
        print(f"✓ {restaurant['name']}")
        print(f"  Category: {restaurant['category']}")
        print(f"  Location: {restaurant['neighborhood']}, {restaurant['city']} - {restaurant['state']}")
        print(f"  Phone: {restaurant['phone']}")
        print()
    
    # Verify the filter worked
    cities = {r['city'] for r in data['restaurants']}
    states = {r['state'] for r in data['restaurants']}
    categories = {r['category'] for r in data['restaurants']}
    
    print("Filter Verification:")
    print(f"  Cities: {cities} (should only be 'Campinas')")
    print(f"  States: {states} (should only be 'SP')")
    print(f"  Categories: {categories} (should be Restaurante/Pizzaria/Lanchonete)")
    print()


def example_filtered_students():
    """Example: Generate students only from UNICAMP with specific courses."""
    print("\n" + "="*70)
    print("Example 2: Students ONLY from UNICAMP in CS-related courses")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            EntitySpec(
                name="students",
                records=8,
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
                        name="university",
                        logical_type="university_name",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={
                                "allowed_values": ["Universidade Estadual de Campinas (UNICAMP)"]
                            }
                        )
                    ),
                    FieldSpec(
                        name="course",
                        logical_type="course_name",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={
                                "allowed_values": [
                                    "Ciência da Computação",
                                    "Engenharia da Computação",
                                    "Sistemas de Informação"
                                ]
                            }
                        )
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
    
    data = generate_all_data(request)
    
    print(f"Generated {len(data['students'])} students:\n")
    
    for student in data['students']:
        print(f"✓ {student['name']} (Age: {student['age']})")
        print(f"  Email: {student['email']}")
        print(f"  University: {student['university']}")
        print(f"  Course: {student['course']}")
        print()
    
    # Verify the filter worked
    universities = {s['university'] for s in data['students']}
    courses = {s['course'] for s in data['students']}
    
    print("Filter Verification:")
    print(f"  Universities: {universities}")
    print(f"  Courses: {courses}")
    print()


def example_mixed_filters():
    """Example: Mix of filtered and unfiltered fields."""
    print("\n" + "="*70)
    print("Example 3: Mixed - Some fields filtered, others random")
    print("="*70 + "\n")
    
    request = GenerationRequest(
        database_type="postgresql",
        connection_uri="postgresql://dummy",
        entities=[
            EntitySpec(
                name="establishments",
                records=6,
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
                        logical_type="company",
                        constraints=ConstraintSpec(nullable=False)
                        # No filter - generates random company names
                    ),
                    FieldSpec(
                        name="city",
                        logical_type="city",
                        constraints=ConstraintSpec(
                            nullable=False,
                            extra={
                                "allowed_values": ["Campinas", "São Paulo", "Santos"]
                            }
                        )
                        # Filter - only these 3 cities
                    ),
                    FieldSpec(
                        name="category",
                        logical_type="business_category",
                        constraints=ConstraintSpec(nullable=False)
                        # No filter - any category
                    )
                ]
            )
        ]
    )
    
    data = generate_all_data(request)
    
    print(f"Generated {len(data['establishments'])} establishments:\n")
    
    for est in data['establishments']:
        print(f"✓ {est['name']}")
        print(f"  City: {est['city']} (filtered)")
        print(f"  Category: {est['category']} (not filtered)")
        print()
    
    cities = {e['city'] for e in data['establishments']}
    print(f"Cities used: {cities} (filtered to Campinas/São Paulo/Santos)")
    print()


def example_no_filters():
    """Example: No filters - completely random data."""
    print("\n" + "="*70)
    print("Example 4: No filters - completely random (comparison)")
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
                        name="city",
                        logical_type="city",
                        constraints=ConstraintSpec(nullable=False)
                        # No filter - any Brazilian city
                    ),
                    FieldSpec(
                        name="state",
                        logical_type="uf",
                        constraints=ConstraintSpec(nullable=False)
                        # No filter - any Brazilian state
                    )
                ]
            )
        ]
    )
    
    data = generate_all_data(request)
    
    print(f"Generated {len(data['users'])} users (no filters):\n")
    
    for user in data['users']:
        print(f"✓ {user['name']} - {user['city']}/{user['state']}")
    
    print("\n(Notice how cities and states are diverse and random)")
    print()


if __name__ == "__main__":
    # Run all examples
    example_filtered_restaurants()
    example_filtered_students()
    example_mixed_filters()
    example_no_filters()
    
    print("="*70)
    print("✓ All filter examples completed!")
    print("="*70)
    print()
    print("Key Takeaway:")
    print("  Use 'allowed_values' in constraints.extra to filter/restrict")
    print("  generated values to a specific list of options.")
    print()
