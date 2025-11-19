# Decisão de Arquitetura: lib vs API vs script

## Resumo da Decisão

**Resposta**: **TODOS OS TRÊS!** 🎉

O sistema foi implementado com uma arquitetura em camadas que fornece três modos de uso:

1. ✅ **Biblioteca Python (Core)** - Camada obrigatória e fundamental
2. ✅ **API REST (FastAPI)** - Interface HTTP opcional
3. ✅ **Script CLI (Typer)** - Interface de linha de comando opcional

## Justificativa

### Por que todos os três?

Esta arquitetura oferece **máxima flexibilidade** sem duplicação de código:

```
┌─────────────────────────────────────┐
│         API (FastAPI)              │  ← Interface HTTP
│         CLI (Typer)                │  ← Interface Linha de Comando
├─────────────────────────────────────┤
│    Core Library (mydata_core)      │  ← Lógica de negócio
│  • Data Generation Engine          │
│  • Brazilian Providers             │
│  • Database Adapters               │
└─────────────────────────────────────┘
```

## Vantagens de Cada Camada

### 1. Core Library (Obrigatório)

**Uso:**
```python
from mydata_core import GenerationRequest, generate_and_insert

request = GenerationRequest(...)
response = generate_and_insert(request)
```

**Vantagens:**
- ✅ Reutilizável em qualquer código Python
- ✅ Testável isoladamente
- ✅ Sem overhead de rede
- ✅ Máximo controle e flexibilidade
- ✅ Pode ser usado em notebooks, scripts, testes

**Casos de uso:**
- Testes automatizados que precisam de dados sintéticos
- Pipelines de CI/CD
- Scripts de população de bancos de desenvolvimento
- Integração em aplicações maiores

### 2. API REST (Opcional)

**Uso:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @schema.json
```

**Vantagens:**
- ✅ Acesso via HTTP de qualquer linguagem
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Deploy independente (Docker, Kubernetes)
- ✅ Escalável horizontalmente
- ✅ Controle de acesso e autenticação possível

**Casos de uso:**
- Equipes diferentes precisam gerar dados
- Integração com ferramentas externas
- Serviço centralizado para toda a organização
- Frontend web precisa gerar dados

### 3. Script CLI (Opcional)

**Uso:**
```bash
mydata-gen --schema schema.json
mydata-gen validate --schema schema.json
```

**Vantagens:**
- ✅ Fácil de usar para desenvolvedores
- ✅ Integração com shell scripts
- ✅ Validação de schemas sem execução
- ✅ Output formatado e colorido (Rich)
- ✅ Perfeito para automação local

**Casos de uso:**
- Desenvolvedores populando bancos locais
- Scripts de setup de ambiente
- Makefiles e scripts de automação
- Testes manuais rápidos

## Como as Camadas se Relacionam

### Sem Duplicação

```python
# API (mydata_core/api/main.py)
@app.post("/generate")
async def generate_data(request: GenerationRequest):
    return generate_and_insert(request)  # ← Usa a lib

# CLI (mydata_core/cli/main.py)
def generate(schema_file: Path):
    request = GenerationRequest(**schema_data)
    response = generate_and_insert(request)  # ← Usa a lib
```

**Todo o código de geração de dados está na lib!** API e CLI são apenas "cascas" finas.

## Comparação com Alternativas

### Opção 1: Apenas Biblioteca ❌
- ❌ Difícil integração externa
- ❌ Toda equipe precisa saber Python
- ❌ Sem isolamento de execução

### Opção 2: Apenas API ❌
- ❌ Overhead de rede para uso local
- ❌ Requer servidor rodando sempre
- ❌ Não reutilizável em código Python

### Opção 3: Apenas Script ❌
- ❌ Só linha de comando
- ❌ Difícil automação programática
- ❌ Sem integração HTTP

### Opção 4: LIB + API + CLI ✅ (Implementado)
- ✅ Máxima flexibilidade
- ✅ Todos os casos de uso cobertos
- ✅ Sem duplicação de código
- ✅ Manutenção centralizada

## Exemplos de Uso Real

### Cenário 1: Desenvolvedor Local
```bash
# Usa CLI para popular banco local rapidamente
mydata-gen --schema dev_schema.json
```

### Cenário 2: Teste Automatizado
```python
# Usa biblioteca direto no código de teste
def test_user_creation():
    data = generate_all_data(request)
    assert len(data['users']) == 100
```

### Cenário 3: Frontend Web
```javascript
// Usa API REST via fetch
const response = await fetch('http://api.example.com/generate', {
  method: 'POST',
  body: JSON.stringify(schema)
});
```

### Cenário 4: Pipeline CI/CD
```yaml
# Usa CLI em script de CI
- name: Populate test database
  run: mydata-gen --schema test_data.json
```

## Conclusão

A arquitetura implementada oferece:

1. **Core sólido** (biblioteca) com toda a lógica
2. **Interfaces flexíveis** (API e CLI) para diferentes casos de uso
3. **Zero duplicação** de código
4. **Manutenção simples** (tudo em um lugar)
5. **Extensível** (fácil adicionar novas interfaces)

Esta é a melhor solução para atender **todos os usuários possíveis** mantendo o código **limpo, testável e manutenível**.

---

## Resposta Final

**lib vs API vs script?**

**Resposta**: Implementamos os **três**, com a **biblioteca como núcleo** e **API/CLI como interfaces opcionais**. Esta arquitetura maximiza flexibilidade sem sacrificar qualidade ou aumentar complexidade. 🚀
