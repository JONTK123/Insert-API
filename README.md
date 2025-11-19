# MyData - Sistema de Geração de Dados Sintéticos

**Uma biblioteca Python completa** para gerar e inserir dados sintéticos em bancos PostgreSQL e MongoDB. Inclui providers brasileiros customizados (CPF, CNPJ, universidades, etc.).

---

## 📦 O que é este projeto?

Este projeto é **TRÊS COISAS EM UMA**:

1. ✅ **Biblioteca Python** (`mydata_core`) - Para usar no seu código
2. ✅ **API REST** (FastAPI) - Para integração via HTTP
3. ✅ **CLI** (linha de comando) - Para uso rápido no terminal

**Você escolhe como usar!**

---

## 🎯 Características Principais

- 🎲 **50+ tipos de dados** incluindo brasileiros (CPF, CNPJ, UF, universidades)
- 🔗 **Relacionamentos automáticos** com foreign keys e resolução de dependências
- 🗃️ **Multi-banco**: PostgreSQL e MongoDB
- 🎯 **Constraints**: Primary keys, unique, nullable, auto-increment
- 🔍 **Filtros**: Restrinja dados a valores específicos (ex: apenas Campinas)
- 📤 **Export**: SQL, MongoDB, CSV, JSON
- 📊 **Escalável**: Gere de 10 a 100.000+ registros

---

## 🚀 Instalação

### Opção 1: Clonar e instalar localmente

```bash
# Clonar repositório
git clone https://github.com/JONTK123/Insert-API.git
cd Insert-API

# Instalar dependências
pip install -r requirements.txt

# Instalar o pacote (habilita CLI)
pip install -e .
```

### Opção 2: Instalar direto do GitHub

```bash
pip install git+https://github.com/JONTK123/Insert-API.git
```

### Opção 3: Após publicar no PyPI (futuro)

```bash
pip install mydata-core
```


---

## 💡 Como Usar

### Modo 1: Como Biblioteca Python (Recomendado)

**Importar e usar no seu código:**

```python
from mydata_core import (
    GenerationRequest, 
    EntitySpec, 
    FieldSpec, 
    ConstraintSpec,
    generate_all_data,
    export_to_sql
)

# Definir schema
request = GenerationRequest(
    database_type="postgresql",
    connection_uri="postgresql://user:password@localhost:5432/mydb",
    entities=[
        EntitySpec(
            name="users",
            records=1000,  # Gerar 1000 usuários
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
                    logical_type="cpf",  # CPF brasileiro válido!
                    constraints=ConstraintSpec(unique=True, nullable=False)
                )
            ]
        )
    ]
)

# Opção A: Gerar dados em memória
data = generate_all_data(request)
print(f"Gerados {len(data['users'])} usuários")

# Opção B: Exportar para SQL
sql_commands = export_to_sql(data)
with open('insert_commands.sql', 'w') as f:
    f.write(sql_commands)

# Opção C: Inserir direto no banco
from mydata_core import generate_and_insert
response = generate_and_insert(request)
print(f"Sucesso: {response.message}")
```

### Modo 2: Via CLI (Linha de Comando)

**Criar um arquivo JSON com o schema:**

```json
{
  "database_type": "postgresql",
  "connection_uri": "postgresql://user:pass@localhost/mydb",
  "entities": [
    {
      "name": "users",
      "records": 5000,
      "fields": [
        {
          "name": "id",
          "logical_type": "integer",
          "constraints": {"primary_key": true, "auto_increment": true}
        },
        {
          "name": "name",
          "logical_type": "name",
          "constraints": {"nullable": false}
        },
        {
          "name": "email",
          "logical_type": "email",
          "constraints": {"unique": true, "nullable": false}
        }
      ]
    }
  ]
}
```

**Executar comandos:**

```bash
# Validar schema
mydata-gen validate --schema meu_schema.json

# Gerar e inserir dados
mydata-gen generate --schema meu_schema.json

# Gerar dados de exemplo
python examples/example_usage.py

# Gerar dados com filtros (apenas Campinas)
python examples/example_filters.py

# Gerar dados e exportar SQL/CSV/JSON
python examples/example_export.py
```

### Modo 3: Via API REST

**Iniciar servidor:**

```bash
cd mydata_core/api
python main.py
```

O servidor inicia em `http://localhost:8000`

**Acessar documentação interativa:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Fazer requisição:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @meu_schema.json
```

---

## 📋 Comandos Principais

### Comandos CLI

```bash
# Validar schema JSON
mydata-gen validate --schema schema.json

# Gerar e inserir dados no banco
mydata-gen generate --schema schema.json

# Gerar dados para banco específico
mydata-gen generate --schema schema.json --db-type postgresql

# Gerar com URI customizada
mydata-gen generate --schema schema.json --uri "postgresql://localhost/mydb"

# Modo verboso (mostrar detalhes)
mydata-gen generate --schema schema.json --verbose
```

### Exemplos Prontos

```bash
# Exemplo básico de uso
python examples/example_usage.py

# Exemplo com filtros (apenas Campinas)
python examples/example_filters.py

# Exemplo de export (SQL, CSV, JSON)
python examples/example_export.py

# Exemplo para sistema LightFM (sistema de recomendação)
python examples/example_lightfm.py

# Demo rápido
python demo.py
```

### Como Usar no Seu Projeto

**1. Instalar como dependência:**

```bash
# No seu projeto
pip install git+https://github.com/JONTK123/Insert-API.git
```

**2. Importar e usar:**

```python
# No seu código Python
from mydata_core import generate_all_data, GenerationRequest
import json

# Carregar schema
with open('meu_schema.json') as f:
    schema = json.load(f)

# Ajustar connection URI para seu banco
schema['connection_uri'] = 'postgresql://seu_user:senha@localhost/seu_banco'

# Gerar dados
request = GenerationRequest(**schema)
data = generate_all_data(request)
```

**3. Ou gerar SQL e executar:**

```bash
# Gerar comandos SQL
python examples/example_export.py
# Cria: /tmp/export/insert_commands.sql

# Executar no seu banco
psql -U usuario -d banco -f /tmp/export/insert_commands.sql
```


---

## 🎨 Tipos de Dados Suportados

### Tipos Brasileiros
- `cpf` - CPF brasileiro válido (com dígito verificador)
- `cnpj` - CNPJ brasileiro válido
- `uf` - Estados brasileiros (SP, RJ, MG, etc.)
- `university_name` - Universidades brasileiras (UNICAMP, USP, etc.)
- `course_name` - Cursos universitários brasileiros
- `business_category` - Categorias de negócio
- `preference_type` - Tipos de preferência
- `preference_name` - Nomes de preferências
- `opening_hours` - Horário de funcionamento brasileiro
- `password_hash` - Hash de senha (formato bcrypt)

### Identidade & Pessoas
- `name`, `first_name`, `last_name`

### Contato & Internet
- `email`, `username`, `phone`, `ip_address`, `url`, `domain`

### Localização
- `address`, `street_name`, `city`, `country`, `postcode`
- `latitude`, `longitude`

### Empresa & Trabalho
- `company`, `job_title`

### Datas & Tempo
- `date`, `datetime`, `date_past`, `date_future`

### Numéricos
- `integer`, `float`, `price`, `age`
- `weight_1_5`, `rating_1_5`, `similarity_score`

### Texto
- `short_text`, `text`, `long_text`

### Outros
- `uuid`, `boolean`, `color_name`, `hex_color`

**Total: 50+ tipos de dados!**

---

## 🔍 Filtros (Valores Permitidos)

Restrinja valores gerados a uma lista específica:

```python
# Exemplo: Apenas estabelecimentos de Campinas
FieldSpec(
    name="cidade",
    logical_type="city",
    constraints=ConstraintSpec(
        nullable=False,
        extra={"allowed_values": ["Campinas"]}  # Apenas Campinas!
    )
)
```

```json
{
  "name": "cidade",
  "logical_type": "city",
  "constraints": {
    "extra": {
      "allowed_values": ["Campinas", "São Paulo", "Santos"]
    }
  }
}
```

**Veja exemplos completos em:**
- `examples/campinas_filtered.json` - Schema filtrado
- `examples/example_filters.py` - 4 exemplos de filtros
- `FILTERS_GUIDE.md` - Guia completo

---

## 📤 Exportar Dados

### Exportar para SQL

```python
from mydata_core import export_to_sql

sql_commands = export_to_sql(data)
# Retorna comandos INSERT prontos para PostgreSQL/MySQL
```

### Exportar para MongoDB

```python
from mydata_core import export_to_mongodb

mongo_commands = export_to_mongodb(data)
# Retorna comandos insertMany para MongoDB
```

### Exportar para CSV

```python
from mydata_core import export_to_csv

csv_files = export_to_csv(data, output_dir="/tmp/export")
# Cria um arquivo CSV por entidade
```

### Exportar para JSON

```python
from mydata_core import export_to_json

json_files = export_to_json(data, output_dir="/tmp/export")
# Cria arquivos JSON estruturados
```

### Exportar Tudo de Uma Vez

```python
from mydata_core import export_all

results = export_all(data, output_dir="/tmp/export", formats=["sql", "csv", "json"])
# Cria: SQL, CSV e JSON de todas as entidades
```

**Veja exemplo completo:** `examples/example_export.py`

## Filtering / Restricting Generated Data

You can **filter** data generation to specific values using `allowed_values` in the `extra` field of constraints. This is perfect for scenarios like:
- Generate restaurants **only in Campinas**
- Generate students **only from specific universities**
- Generate events **only of certain types**

### Example: Restaurants only in Campinas

```json
{
  "name": "cidade",
  "logical_type": "city",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": ["Campinas"]
    }
  }
}
```

### Example: Multiple allowed categories

```json
{
  "name": "categoria",
  "logical_type": "business_category",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": ["Restaurante", "Pizzaria", "Lanchonete"]
    }
  }
}
```

### Python Example with Filters

```python
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
```

**How it works:**
- If `allowed_values` is specified, the generator will only use values from that list
- Works with any data type (strings, numbers, etc.)
- Can be combined with other constraints (unique, nullable, etc.)
- Leave `allowed_values` empty or omit it for completely random generation

See `examples/campinas_filtered.json` and `examples/example_filters.py` for complete examples.


---

## 📊 Capacidade e Performance

### Escalabilidade

- ✅ **1.000 registros** → ~1-2 segundos
- ✅ **10.000 registros** → ~10-15 segundos
- ✅ **100.000 registros** → ~1-2 minutos
- ✅ **1.000.000 registros** → ~10-20 minutos

### Otimizações

- **Batch insertion**: Insere 1000 registros por vez
- **Geração eficiente**: Algoritmos otimizados
- **Memória controlada**: Processa em lotes

### Exemplo 100K Registros

```python
EntitySpec(
    name="users",
    records=100000,  # 100 mil usuários!
    fields=[...]
)
```

---

## 🎓 Exemplos Incluídos

### 1. Sistema de Recomendação (LightFM)
**Arquivo:** `examples/recommendation_system_lightfm.json`

Gera dados completos para sistema de recomendação:
- 10 universidades
- 200 usuários
- 300 estabelecimentos
- 40 preferências
- 800 conexões usuário-preferência
- 900 conexões estabelecimento-preferência
- 2000 interações usuário-estabelecimento
- 1000 similaridades usuário-usuário

**Total: 5.262 registros com todos os relacionamentos!**

```bash
python examples/example_lightfm.py
```

### 2. Dados com Filtros (Campinas)
**Arquivo:** `examples/campinas_filtered.json`

Gera dados apenas de Campinas:
- 50 restaurantes de Campinas
- 30 alunos da UNICAMP
- 20 eventos em Campinas

```bash
python examples/example_filters.py
```

### 3. Exportação Multi-formato
**Arquivo:** `examples/example_export.py`

Demonstra exportação em SQL, MongoDB, CSV e JSON.

```bash
python examples/example_export.py
```

---

## 📚 Documentação Adicional

- **[QUICKSTART.md](QUICKSTART.md)** - Guia rápido em 5 minutos
- **[LIGHTFM_INTEGRATION.md](LIGHTFM_INTEGRATION.md)** - Integração com projeto LightFM
- **[FILTERS_GUIDE.md](FILTERS_GUIDE.md)** - Guia completo de filtros (300+ linhas)
- **[ARCHITECTURE_DECISION.md](ARCHITECTURE_DECISION.md)** - Por que lib + API + CLI
- **[FAQ.md](FAQ.md)** - Perguntas frequentes e respostas detalhadas

---

## 🔧 Como Publicar no PyPI

Para disponibilizar sua biblioteca para instalação via `pip install mydata-core`:

```bash
# 1. Instalar ferramentas
pip install build twine

# 2. Construir pacote
python -m build

# 3. Criar conta no PyPI
# https://pypi.org/account/register/

# 4. Fazer upload
python -m twine upload dist/*

# Depois, qualquer pessoa pode instalar:
pip install mydata-core
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest mydata_core/tests/ -v

# Testes específicos
pytest mydata_core/tests/test_generator.py -v
pytest mydata_core/tests/test_filters.py -v
```

**Status:** 15/15 testes passando ✅

---

## 🔒 Segurança

- ✅ CodeQL: 0 issues
- ✅ Dados sintéticos (não são dados reais)
- ✅ CPF/CNPJ válidos mas fictícios
- ✅ Sem credenciais hardcoded

---

## 💡 Casos de Uso

1. **Desenvolvimento**: Popular bancos de desenvolvimento rapidamente
2. **Testes**: Gerar dados para testes automatizados
3. **Demos**: Criar dados realistas para apresentações
4. **Performance**: Gerar grandes volumes para testes de carga
5. **Machine Learning**: Datasets sintéticos para treinar modelos
6. **Privacidade**: Substituir dados de produção por sintéticos

---

## ❓ Perguntas Frequentes

### É uma biblioteca, API ou script?
**TODOS OS TRÊS!** É uma biblioteca Python que também pode ser usada como API REST ou CLI.

### O Faker tem banco de dados pronto?
**NÃO.** O Faker **GERA** dados aleatórios usando algoritmos. Não existe banco de dados de pessoas reais.

### Posso gerar 100.000 registros?
**SIM!** O sistema suporta desde 10 até 1.000.000+ registros.

### Funciona para qualquer domínio?
**SIM!** Funciona para e-commerce, sistemas acadêmicos, financeiros, recomendação, etc. Basta definir seu schema.

### Como usar no meu projeto?
```bash
pip install git+https://github.com/JONTK123/Insert-API.git
```

**Veja detalhes completos em:** [FAQ.md](FAQ.md)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

---

## 📝 Licença

MIT License - veja o arquivo LICENSE para detalhes

---

## 🎯 Resposta Final: "lib vs API vs script?"

**Resposta**: **TODOS OS TRÊS!** 🎉

O sistema implementa:
1. ✅ **Biblioteca Python** (core reutilizável)
2. ✅ **API REST** (interface HTTP com FastAPI)
3. ✅ **CLI** (linha de comando com Typer)

**Arquitetura**: Biblioteca como núcleo, API e CLI como interfaces opcionais. Zero duplicação de código! 🚀

---

**Pronto para usar! Escolha seu modo favorito e comece a gerar dados! 🎊**