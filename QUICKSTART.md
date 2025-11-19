# Quick Start Guide

Get up and running with MyData in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/JONTK123/Insert-API.git
cd Insert-API

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Test (No Database Required)

Run the demo to see the system in action without any database:

```bash
python demo.py
```

This will generate sample data and show it on screen!

## Usage Methods

### Method 1: As a Python Library

```python
from mydata_core import GenerationRequest, EntitySpec, FieldSpec, ConstraintSpec, generate_all_data

request = GenerationRequest(
    database_type="postgresql",
    connection_uri="postgresql://dummy",
    entities=[
        EntitySpec(
            name="users",
            records=10,
            fields=[
                FieldSpec(name="id", logical_type="integer", 
                         constraints=ConstraintSpec(primary_key=True, auto_increment=True)),
                FieldSpec(name="name", logical_type="name"),
                FieldSpec(name="email", logical_type="email", 
                         constraints=ConstraintSpec(unique=True))
            ]
        )
    ]
)

# Generate data (no database insertion)
data = generate_all_data(request)
print(f"Generated {len(data['users'])} users")
```

### Method 2: Using the CLI

```bash
# Validate a schema
mydata-gen validate --schema examples/simple_mongodb.json

# Generate and insert data
mydata-gen generate --schema examples/recommendation_system_postgres.json
```

### Method 3: Using the REST API

```bash
# Start the API server
cd mydata_core/api
python main.py

# In another terminal, send a request
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @../../examples/simple_mongodb.json

# Or visit http://localhost:8000/docs for interactive API docs
```

## Running Tests

```bash
pytest mydata_core/tests/test_generator.py -v
```

## Example Schemas

Check the `examples/` directory:

- `recommendation_system_postgres.json` - Complex schema with 9 related tables
- `simple_mongodb.json` - Simple MongoDB example
- `example_usage.py` - Python code examples

## Supported Data Types

### Brazilian Types
- `cpf`, `cnpj`, `uf`, `university_name`, `course_name`, `business_category`

### Standard Types
- **Identity**: `name`, `email`, `username`, `phone`
- **Location**: `address`, `city`, `country`, `latitude`, `longitude`
- **Dates**: `date`, `datetime`, `date_past`, `date_future`
- **Numbers**: `integer`, `float`, `price`, `age`
- **Text**: `short_text`, `text`, `long_text`
- **Others**: `uuid`, `boolean`, `url`

[See full list in README.md]

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [ARCHITECTURE_DECISION.md](ARCHITECTURE_DECISION.md) for design rationale
3. Explore example schemas in `examples/`
4. Try generating data for your own database!

## Need Help?

- Check the examples in `examples/`
- Read the comprehensive README
- Look at the test cases in `mydata_core/tests/`
- Visit the API docs at http://localhost:8000/docs (when running the API)
