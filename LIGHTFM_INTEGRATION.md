# 🎉 Sistema Completo para Seu Projeto LightFM

## ✅ Resposta às Suas Perguntas

### 1. "quero q vc me gere comandos sql ou mongo de adicionar nas tabelas"

**SIM! Totalmente implementado!**

```python
from mydata_core import generate_all_data, export_to_sql, export_to_mongodb

# Gerar dados
data = generate_all_data(request)

# Exportar para SQL
sql_commands = export_to_sql(data)
# Agora você tem comandos INSERT prontos para copiar!

# Ou MongoDB
mongo_commands = export_to_mongodb(data)
```

### 2. "ou vc vai me dar um csv algo do tipo?"

**SIM! CSV, JSON, e mais!**

```python
from mydata_core import export_to_csv, export_to_json, export_all

# Exportar para CSV (um arquivo por tabela)
csv_files = export_to_csv(data, output_dir="/tmp/export")

# Exportar para JSON
json_files = export_to_json(data, output_dir="/tmp/export")

# Ou exportar TUDO de uma vez!
results = export_all(data, output_dir="/tmp/export")
# Cria: SQL, MongoDB, CSV e JSON
```

### 3. "poderei aplicar filtros e gerar dados para essa base de dados do meu projeto atual?"

**SIM! Schema pronto para seus models!**

Veja: `examples/recommendation_system_lightfm.json`

Este schema mapeia **EXATAMENTE** para seus models SQLAlchemy:
- ✅ `universidades` com nomes corretos: `id_universidade`, `nome`, `cidade`, `estado`
- ✅ `usuarios` com nomes corretos: `id_usuario`, `nome`, `email`, `senha_hash`, etc.
- ✅ `estabelecimentos` com nomes corretos: `id_estabelecimento`, `descricao`, `endereco`, etc.
- ✅ Todos os relacionamentos com FK corretas!

---

## 🚀 Como Usar com Seu Projeto

### Opção 1: Gerar e Exportar SQL (Mais Simples)

```bash
# Executar o exemplo
cd /home/runner/work/Insert-API/Insert-API
python examples/example_lightfm.py

# Isso cria:
# - /tmp/lightfm_data_export/insert_commands.sql (6000+ linhas!)
# - CSVs de todas as tabelas
# - JSONs de todas as tabelas
```

Depois, execute no seu PostgreSQL:

```bash
psql -U seu_usuario -d sua_base -f /tmp/lightfm_data_export/insert_commands.sql
```

Pronto! 5.262 registros inseridos! 🎉

### Opção 2: Inserir Direto no Banco

```python
from mydata_core import generate_and_insert, GenerationRequest
import json

# Carregar schema
with open('examples/recommendation_system_lightfm.json') as f:
    schema = json.load(f)

# Atualizar connection_uri para seu banco
schema['connection_uri'] = 'postgresql://user:pass@localhost/seu_banco'

request = GenerationRequest(**schema)

# Gerar E inserir direto no banco!
response = generate_and_insert(request)

print(response.message)
# "Successfully generated and inserted 5262 records across 9 entities."
```

### Opção 3: Via CLI (Mais Rápido)

```bash
# Validar schema
mydata-gen validate --schema examples/recommendation_system_lightfm.json

# Gerar dados
mydata-gen generate --schema examples/recommendation_system_lightfm.json

# Com export
mydata-gen generate --schema examples/recommendation_system_lightfm.json --export sql,csv,json
```

---

## 🎯 Com Filtros (Apenas Campinas, por exemplo)

Edite o schema JSON e adicione filtros:

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

Ou use o schema já pronto: `examples/campinas_filtered.json`

---

## 📊 O Que Foi Gerado

### Dados para Seu Sistema de Recomendação

- **10 Universidades** (UNICAMP, USP, UNESP, etc.)
- **12 Categorias** de estabelecimentos
- **200 Usuários** com:
  - Nome, email, senha_hash (formato bcrypt!)
  - Curso, idade, descrição
  - Universidade associada
  - Data de cadastro
- **300 Estabelecimentos** com:
  - Descrição, endereço, cidade
  - Horário de funcionamento
  - Dono (nome e email)
  - Categoria
- **40 Preferências** por tipo:
  - Alimentação, Ambiente, Lazer, Cultura, Esporte, Entretenimento
- **800 Conexões** Usuário-Preferência (user features para LightFM)
- **900 Conexões** Estabelecimento-Preferência (item features para LightFM)
- **2000 Interações** Usuário-Estabelecimento (matriz de interações!)
- **1000 Similaridades** Usuário-Usuário (collaborative filtering!)

**Total: 5.262 registros prontos para LightFM!** 🚀

---

## 📁 Formatos de Export

### 1. SQL Commands (PostgreSQL)

```sql
-- /tmp/lightfm_data_export/insert_commands.sql
INSERT INTO usuarios (id_usuario, nome, email, senha_hash, curso, idade, descricao, id_universidade, data_cadastro) VALUES
(1, 'Ana Sophia Aragão', 'svieira@example.net', '$2b$12$c991a8...', 'Engenharia Civil', 44, '...', 1, '2025-11-03'),
(2, 'Laura Silveira', 'aragao@example.com', '$2b$12$7d719f...', 'Arquitetura', 47, NULL, 1, '2025-03-12');
-- ... mais 198 usuários
```

### 2. CSV Files

```csv
# /tmp/lightfm_data_export/usuarios.csv
id_usuario,nome,email,senha_hash,curso,idade,descricao,id_universidade,data_cadastro
1,"Ana Sophia Aragão","svieira@example.net","$2b$12$c991a8...","Engenharia Civil",44,"...",1,"2025-11-03"
```

### 3. JSON Files

```json
// /tmp/lightfm_data_export/usuarios.json
[
  {
    "id_usuario": 1,
    "nome": "Ana Sophia Aragão",
    "email": "svieira@example.net",
    "senha_hash": "$2b$12$c991a8...",
    "curso": "Engenharia Civil",
    "idade": 44,
    "descricao": "...",
    "id_universidade": 1,
    "data_cadastro": "2025-11-03"
  }
]
```

### 4. MongoDB Commands

```javascript
// /tmp/lightfm_data_export/insert_commands.js
db.usuarios.insertMany([
  {
    "id_usuario": 1,
    "nome": "Ana Sophia Aragão",
    "email": "svieira@example.net",
    // ...
  }
]);
```

---

## 🎓 Exemplos Prontos

### 1. `examples/example_lightfm.py`
Gera dados para SEU projeto e exporta em todos os formatos!

```bash
python examples/example_lightfm.py
```

### 2. `examples/recommendation_system_lightfm.json`
Schema JSON mapeando EXATAMENTE seus models SQLAlchemy.

### 3. `examples/example_export.py`
Demonstra todas as opções de export (SQL, MongoDB, CSV, JSON).

### 4. `examples/campinas_filtered.json`
Exemplo com filtros para gerar apenas dados de Campinas.

### 5. `examples/example_filters.py`
4 exemplos de como usar filtros.

---

## 💡 Dicas

### Para Treinar LightFM

1. **User Features**: Use `usuario_preferencia` (800 conexões)
2. **Item Features**: Use `estabelecimento_preferencia` (900 conexões)
3. **Interactions Matrix**: Use `recomendacao_estabelecimento` (2000 interações)
4. **User Similarity**: Use `recomendacao_usuario` (1000 similaridades)

### Para Testar Localmente

```python
# Gerar apenas para Campinas
# Edite o JSON e adicione filtros:
"cidade": {
  "extra": {"allowed_values": ["Campinas"]}
}
```

### Para Importar CSV no Pandas

```python
import pandas as pd

usuarios = pd.read_csv('/tmp/lightfm_data_export/usuarios.csv')
estabelecimentos = pd.read_csv('/tmp/lightfm_data_export/estabelecimentos.csv')
interacoes = pd.read_csv('/tmp/lightfm_data_export/recomendacao_estabelecimento.csv')

# Pronto para análise ou treinar LightFM!
```

---

## 📚 Documentação

- **README.md** - Guia geral do sistema
- **FILTERS_GUIDE.md** - Guia completo de filtros (300+ linhas!)
- **QUICKSTART.md** - Como começar em 5 minutos
- **ARCHITECTURE_DECISION.md** - Por que lib + API + CLI

---

## ✅ Checklist Final

- [x] Gerar dados sintéticos ✅
- [x] Mapear seus models SQLAlchemy ✅
- [x] Exportar comandos SQL ✅
- [x] Exportar comandos MongoDB ✅
- [x] Exportar CSV ✅
- [x] Exportar JSON ✅
- [x] Aplicar filtros (cidade, categoria, etc.) ✅
- [x] Manter relacionamentos (FK) ✅
- [x] Gerar senhas hash (bcrypt format) ✅
- [x] 5.262 registros prontos! ✅

---

## 🚀 Próximos Passos

1. **Execute o exemplo:**
   ```bash
   python examples/example_lightfm.py
   ```

2. **Revise os arquivos gerados:**
   ```bash
   ls -lh /tmp/lightfm_data_export/
   ```

3. **Execute o SQL no seu banco:**
   ```bash
   psql -U user -d database -f /tmp/lightfm_data_export/insert_commands.sql
   ```

4. **Treine seu modelo LightFM!** 🎉

---

**Está tudo pronto para você usar no seu projeto! 🎊**

Qualquer dúvida, veja os exemplos em `examples/` ou a documentação completa!
