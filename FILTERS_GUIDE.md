# Guia de Filtros de Dados (Data Filters Guide)

## 🎯 Visão Geral

O sistema MyData permite **filtrar/restringir** a geração de dados para valores específicos usando o campo `allowed_values` dentro de `constraints.extra`.

## 📋 Por que usar filtros?

Filtros são úteis quando você quer gerar dados **realistas** e **contextualizados**:

- ✅ Restaurantes **apenas de Campinas**
- ✅ Alunos **apenas da UNICAMP**
- ✅ Estabelecimentos **apenas de certas categorias**
- ✅ Eventos **apenas em locais específicos**

## 🔧 Como Usar

### Sintaxe Básica (JSON)

```json
{
  "name": "nome_do_campo",
  "logical_type": "tipo_logico",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": ["valor1", "valor2", "valor3"]
    }
  }
}
```

### Sintaxe Básica (Python)

```python
FieldSpec(
    name="nome_do_campo",
    logical_type="tipo_logico",
    constraints=ConstraintSpec(
        nullable=False,
        extra={
            "allowed_values": ["valor1", "valor2", "valor3"]
        }
    )
)
```

## 📚 Exemplos Práticos

### 1. Cidade Única (Campinas)

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

**Resultado**: Todos os registros terão `cidade = "Campinas"`

### 2. Múltiplas Cidades (Região de Campinas)

```json
{
  "name": "cidade",
  "logical_type": "city",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": [
        "Campinas",
        "Jundiaí",
        "Valinhos",
        "Vinhedo",
        "Indaiatuba"
      ]
    }
  }
}
```

**Resultado**: Cidade será uma dessas 5 opções (escolha aleatória)

### 3. Categorias Específicas de Estabelecimentos

```json
{
  "name": "categoria",
  "logical_type": "business_category",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": ["Restaurante", "Bar", "Pizzaria"]
    }
  }
}
```

**Resultado**: Apenas essas 3 categorias serão geradas

### 4. Universidade Específica

```json
{
  "name": "universidade",
  "logical_type": "university_name",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": ["Universidade Estadual de Campinas (UNICAMP)"]
    }
  }
}
```

**Resultado**: Todos os alunos serão da UNICAMP

### 5. Cursos de Computação

```json
{
  "name": "curso",
  "logical_type": "course_name",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": [
        "Ciência da Computação",
        "Engenharia da Computação",
        "Sistemas de Informação",
        "Engenharia de Software"
      ]
    }
  }
}
```

**Resultado**: Apenas cursos relacionados a computação

### 6. Estado de São Paulo

```json
{
  "name": "estado",
  "logical_type": "uf",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": ["SP"]
    }
  }
}
```

**Resultado**: Todos os registros em São Paulo

### 7. Bairros de Campinas

```json
{
  "name": "bairro",
  "logical_type": "text",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": [
        "Cambuí",
        "Centro",
        "Taquaral",
        "Barão Geraldo",
        "Jardim Guanabara",
        "Vila Brandina"
      ]
    }
  }
}
```

**Resultado**: Apenas esses bairros serão usados

### 8. Tipos de Eventos

```json
{
  "name": "tipo_evento",
  "logical_type": "text",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": [
        "Show Musical",
        "Teatro",
        "Festa",
        "Workshop",
        "Palestra"
      ]
    }
  }
}
```

### 9. Locais de Eventos em Campinas

```json
{
  "name": "local",
  "logical_type": "text",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": [
        "Parque Portugal",
        "Lagoa do Taquaral",
        "Centro de Convivência",
        "Teatro Castro Mendes",
        "Shopping Iguatemi"
      ]
    }
  }
}
```

### 10. Valores Numéricos Específicos

```json
{
  "name": "nota",
  "logical_type": "integer",
  "constraints": {
    "nullable": false,
    "extra": {
      "allowed_values": [1, 2, 3, 4, 5]
    }
  }
}
```

**Resultado**: Apenas notas de 1 a 5

## 🔀 Combinando Filtros com Outros Campos

### Exemplo Completo: Restaurantes de Campinas

```json
{
  "name": "restaurantes_campinas",
  "records": 50,
  "fields": [
    {
      "name": "id",
      "logical_type": "integer",
      "constraints": {"primary_key": true, "auto_increment": true}
    },
    {
      "name": "nome",
      "logical_type": "company",
      "constraints": {"nullable": false}
    },
    {
      "name": "categoria",
      "logical_type": "business_category",
      "constraints": {
        "nullable": false,
        "extra": {"allowed_values": ["Restaurante", "Pizzaria"]}
      }
    },
    {
      "name": "cidade",
      "logical_type": "city",
      "constraints": {
        "nullable": false,
        "extra": {"allowed_values": ["Campinas"]}
      }
    },
    {
      "name": "bairro",
      "logical_type": "text",
      "constraints": {
        "nullable": false,
        "extra": {"allowed_values": ["Cambuí", "Centro", "Taquaral"]}
      }
    },
    {
      "name": "telefone",
      "logical_type": "phone",
      "constraints": {"nullable": false}
    }
  ]
}
```

**Resultado**:
- `nome`: Aleatório (sem filtro)
- `categoria`: Apenas "Restaurante" ou "Pizzaria"
- `cidade`: Sempre "Campinas"
- `bairro`: Apenas "Cambuí", "Centro" ou "Taquaral"
- `telefone`: Aleatório (sem filtro)

## ⚙️ Comportamento dos Filtros

### Como Funciona

1. **Com `allowed_values`**: O gerador escolhe aleatoriamente um valor da lista
2. **Sem `allowed_values`**: O gerador usa a lógica padrão do tipo (Faker)
3. **Lista vazia `[]`**: Ignorado, comporta-se como se não houvesse filtro

### Compatibilidade

- ✅ Funciona com **qualquer tipo de dado** (strings, números, etc.)
- ✅ Funciona com **constraints** (unique, nullable, etc.)
- ✅ Funciona com **foreign keys**
- ✅ Funciona com **todos os tipos lógicos**

### Combinação com Unique

```json
{
  "name": "categoria",
  "logical_type": "business_category",
  "constraints": {
    "unique": true,
    "nullable": false,
    "extra": {"allowed_values": ["Restaurante", "Bar", "Café"]}
  }
}
```

⚠️ **Atenção**: Com `unique=true` e 3 valores permitidos, você só pode gerar **no máximo 3 registros**!

## 📊 Exemplos Completos

### 1. Schema de Campinas

Veja: `examples/campinas_filtered.json`

Este schema gera:
- 50 restaurantes exclusivamente de Campinas
- 30 alunos exclusivamente da UNICAMP
- 20 eventos exclusivamente em Campinas

### 2. Exemplos Python

Veja: `examples/example_filters.py`

Este arquivo contém 4 exemplos completos:
1. Restaurantes apenas em Campinas
2. Alunos apenas da UNICAMP
3. Campos mistos (alguns filtrados, outros não)
4. Sem filtros (comparação)

## 🚀 Como Usar

### Via CLI

```bash
# Validar schema com filtros
mydata-gen validate --schema examples/campinas_filtered.json

# Gerar dados filtrados
mydata-gen generate --schema examples/campinas_filtered.json
```

### Via Python

```python
from mydata_core import generate_all_data, GenerationRequest

# Carregar seu schema com filtros
request = GenerationRequest(**schema_data)

# Gerar dados
data = generate_all_data(request)
```

### Via API

```bash
# POST /generate com schema JSON contendo allowed_values
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @examples/campinas_filtered.json
```

## 💡 Casos de Uso

### 1. E-commerce Regional

Gere lojas apenas em cidades onde você opera:

```json
"cidade": {
  "logical_type": "city",
  "constraints": {
    "extra": {
      "allowed_values": ["Campinas", "São Paulo", "Santos"]
    }
  }
}
```

### 2. Sistema Universitário

Gere alunos apenas de universidades parceiras:

```json
"universidade": {
  "logical_type": "university_name",
  "constraints": {
    "extra": {
      "allowed_values": ["UNICAMP", "USP", "UNESP"]
    }
  }
}
```

### 3. Plataforma de Delivery

Gere restaurantes apenas de categorias disponíveis:

```json
"categoria": {
  "logical_type": "business_category",
  "constraints": {
    "extra": {
      "allowed_values": [
        "Restaurante",
        "Pizzaria",
        "Hamburgeria",
        "Japonês",
        "Italiano"
      ]
    }
  }
}
```

### 4. Sistema de Eventos

Gere eventos apenas em locais homologados:

```json
"local": {
  "logical_type": "text",
  "constraints": {
    "extra": {
      "allowed_values": [
        "Centro de Convenções",
        "Teatro Municipal",
        "Estádio"
      ]
    }
  }
}
```

## ✅ Testes

Execute os testes de filtros:

```bash
pytest mydata_core/tests/test_filters.py -v
```

Todos os 8 testes devem passar:
- ✅ Filtro simples
- ✅ Filtro de categorias
- ✅ Filtro com valor único
- ✅ Filtro misto (com e sem)
- ✅ Filtro com unique constraint
- ✅ Filtro numérico
- ✅ Lista vazia ignorada
- ✅ Integração completa

## 🎓 Resumo

**Para filtrar dados**:
1. Adicione `allowed_values` em `constraints.extra`
2. Especifique a lista de valores permitidos
3. O gerador escolherá aleatoriamente dessa lista

**Quando usar**:
- ✅ Dados contextualizados (cidade específica)
- ✅ Valores controlados (categorias específicas)
- ✅ Cenários restritos (universidade específica)
- ✅ Testes com dados conhecidos

**Quando NÃO usar**:
- ❌ Quando você quer máxima diversidade
- ❌ Quando não importa os valores exatos
- ❌ Para campos identificadores únicos (IDs, CPF, etc.)

---

Veja os exemplos completos em:
- `examples/campinas_filtered.json` - Schema completo
- `examples/example_filters.py` - Exemplos em Python
- `mydata_core/tests/test_filters.py` - Testes
