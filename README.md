# MyData - Synthetic Data Generation System

A comprehensive Python library for generating and inserting synthetic data into PostgreSQL and MongoDB databases. Built with Faker and custom Brazilian data providers.

## Features

- 🎲 **Comprehensive Data Generation**: Support for 50+ logical data types
- 🇧🇷 **Brazilian Data Types**: CPF, CNPJ, Brazilian states, universities, and more
- 🔗 **Relationship Support**: Automatic foreign key handling and dependency resolution
- 🗃️ **Multi-Database**: PostgreSQL and MongoDB adapters included
- 🎯 **Constraints**: Primary keys, unique, nullable, auto-increment support
- 📦 **Three Usage Modes**: Library, REST API, and CLI

## Architecture

The system is built with three layers:

1. **Core Library** (`mydata_core`): Reusable data generation engine
2. **API Layer** (`mydata_core.api`): FastAPI REST interface
3. **CLI Layer** (`mydata_core.cli`): Command-line interface

## Installation

```bash
# Clone repository
git clone https://github.com/JONTK123/Insert-API.git
cd Insert-API

# Install dependencies
pip install -r requirements.txt

# Install package (optional, for CLI command)
pip install -e .
```

## Quick Start

### 1. As a Python Library

```python
from mydata_core import GenerationRequest, generate_and_insert, FieldSpec, EntitySpec, ConstraintSpec

# Define your schema
request = GenerationRequest(
    database_type="postgresql",
    connection_uri="postgresql://user:password@localhost:5432/mydb",
    entities=[
        EntitySpec(
            name="users",
            records=100,
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
                )
            ]
        )
    ]
)

# Generate and insert data
response = generate_and_insert(request)
print(f"Success: {response.success}")
print(f"Inserted: {response.inserted_counts}")
```

### 2. As a REST API

```bash
# Start the API server
cd mydata_core/api
python main.py

# Server runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

Send a POST request to `/generate`:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @examples/simple_mongodb.json
```

### 3. Using the CLI

```bash
# Using installed command
mydata-gen --schema examples/recommendation_system_postgres.json

# Or run directly
python -m mydata_core.cli.main generate --schema examples/simple_mongodb.json

# Validate schema without generating data
mydata-gen validate --schema examples/recommendation_system_postgres.json
```

## Supported Data Types

### Brazilian-Specific Types
- `cpf` - Brazilian CPF with validation
- `cnpj` - Brazilian CNPJ with validation
- `uf` - Brazilian state abbreviation
- `university_name` - Brazilian university names
- `course_name` - Brazilian course names
- `business_category` - Business categories
- `preference_type` - User preference types
- `preference_name` - Preference names
- `opening_hours` - Brazilian business hours format
- `password_hash` - Mock password hash

### Identity & People
- `name`, `first_name`, `last_name`

### Contact & Internet
- `email`, `username`, `phone`, `ip_address`, `url`, `domain`

### Location & Addresses
- `address`, `street_name`, `street_address`, `city`, `country`, `postcode`
- `latitude`, `longitude`

### Company & Work
- `company`, `job_title`

### Dates & Time
- `date`, `datetime`, `date_past`, `date_future`

### Numeric
- `integer`, `float`, `price`, `age`
- `weight_1_5`, `rating_1_5`, `similarity_score`

### Text
- `short_text`, `text`, `long_text`

### Others
- `uuid`, `boolean`, `color_name`, `hex_color`

## Schema Format

Create a JSON file with your schema:

```json
{
  "database_type": "postgresql",
  "connection_uri": "postgresql://user:pass@localhost/dbname",
  "entities": [
    {
      "name": "table_name",
      "records": 100,
      "fields": [
        {
          "name": "field_name",
          "logical_type": "name",
          "constraints": {
            "primary_key": false,
            "auto_increment": false,
            "unique": false,
            "nullable": true,
            "foreign_key": {
              "entity": "other_table",
              "field": "id"
            },
            "extra": {
              "min": 0,
              "max": 100
            }
          }
        }
      ]
    }
  ]
}
```

## Examples

See the `examples/` directory for complete schema examples:

- `recommendation_system_postgres.json` - Complex recommendation system with 9 related tables
- `simple_mongodb.json` - Simple MongoDB example with users and products

## Dependencies

- **faker** - Core data generation
- **pydantic** - Data validation
- **sqlalchemy** - PostgreSQL support
- **psycopg2-binary** - PostgreSQL driver
- **pymongo** - MongoDB support
- **fastapi** - REST API
- **typer** - CLI interface
- **rich** - CLI formatting

## Development

```bash
# Install in development mode
pip install -e .

# Run tests (when available)
pytest

# Run API in development mode with auto-reload
uvicorn mydata_core.api.main:app --reload
```

## Roadmap

- [ ] Phase 1: Core library with Faker integration ✅
- [ ] Phase 2: Database adapters (PostgreSQL, MongoDB) ✅
- [ ] Phase 3: API and CLI interfaces ✅
- [ ] Phase 4: Unit and integration tests
- [ ] Phase 5: LLM integration for complex text generation
- [ ] Phase 6: Dataset connectors for real data mixing
- [ ] Phase 7: Web scraping profiles for domain-specific data

## Use Cases

- **Development & Testing**: Populate development databases quickly
- **Demo & Training**: Generate realistic demo data for presentations
- **Performance Testing**: Create large datasets for load testing
- **Privacy Compliance**: Replace production data with synthetic alternatives
- **Machine Learning**: Generate training datasets with controlled distributions

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Answer: lib vs API vs script?

**Resposta**: Todos! 🎉

O sistema foi arquitetado como:

1. **LIB (núcleo obrigatório)**: Toda a lógica de geração está na biblioteca reutilizável `mydata_core`
2. **API (interface HTTP)**: FastAPI em cima da lib para integração externa
3. **Script/CLI (interface linha de comando)**: CLI com Typer para uso local rápido

Esta arquitetura permite:
- Usar a biblioteca diretamente em código Python
- Expor via API REST para outros times/serviços
- Executar via CLI para tarefas de DevOps e desenvolvimento

A lib é o core, API e CLI são apenas "cascas" em cima dela. Sem duplicação de lógica! 🚀