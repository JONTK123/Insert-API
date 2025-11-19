"""
Exemplo: Gerar dados para o Sistema de Recomendação LightFM

Este exemplo mostra como gerar dados sintéticos que correspondem
EXATAMENTE aos seus modelos SQLAlchemy.
"""

from mydata_core import (
    generate_all_data,
    generate_and_insert,
    export_to_sql,
    export_to_csv,
    export_all,
    GenerationRequest,
)
import json


def generate_for_lightfm_project():
    """
    Gera dados para o projeto de recomendação com LightFM.
    Mapeia EXATAMENTE para seus models do SQLAlchemy.
    """
    
    print("\n" + "="*70)
    print("Gerando Dados para Sistema de Recomendação LightFM")
    print("="*70 + "\n")
    
    # Carregar o schema
    with open('/home/runner/work/Insert-API/Insert-API/examples/recommendation_system_lightfm.json', 'r') as f:
        schema = json.load(f)
    
    # Criar request
    request = GenerationRequest(**schema)
    
    # Mostrar resumo
    print("📊 Resumo do Schema:")
    print(f"  Database: {request.database_type}")
    print(f"  Entities: {len(request.entities)}")
    print()
    
    total_records = 0
    for entity in request.entities:
        print(f"  • {entity.name:40} {entity.records:5} registros")
        total_records += entity.records
    
    print(f"\n  Total de registros a gerar: {total_records}")
    print()
    
    # Gerar dados
    print("⏳ Gerando dados...")
    data = generate_all_data(request)
    print("✅ Dados gerados com sucesso!")
    print()
    
    # Mostrar resumo dos dados gerados
    print("📈 Dados Gerados:")
    print("-" * 70)
    
    # Universidades
    print("\n🎓 Universidades:")
    for uni in data['universidades'][:3]:
        print(f"  - {uni['nome']}")
        print(f"    Localização: {uni['cidade']}/{uni['estado']}")
    print(f"  ... e mais {len(data['universidades']) - 3} universidades")
    
    # Usuários
    print("\n👤 Usuários (amostras):")
    for user in data['usuarios'][:3]:
        uni_id = user['id_universidade']
        uni_nome = next((u['nome'] for u in data['universidades'] if u['id_universidade'] == uni_id), "N/A")
        print(f"  - {user['nome']} ({user['idade']} anos)")
        print(f"    Email: {user['email']}")
        print(f"    Curso: {user['curso']}")
        print(f"    Universidade: {uni_nome}")
    print(f"  ... e mais {len(data['usuarios']) - 3} usuários")
    
    # Estabelecimentos
    print("\n🏪 Estabelecimentos (amostras):")
    for est in data['estabelecimentos'][:3]:
        cat_id = est['id_categoria']
        cat_nome = next((c['nome_categoria'] for c in data['categorias_estabelecimentos'] if c['id_categoria'] == cat_id), "N/A")
        print(f"  - Categoria: {cat_nome}")
        print(f"    Cidade: {est['cidade']}")
        print(f"    Horário: {est['horario_funcionamento']}")
    print(f"  ... e mais {len(data['estabelecimentos']) - 3} estabelecimentos")
    
    # Preferências
    print(f"\n⭐ Preferências: {len(data['preferencias'])} preferências cadastradas")
    pref_types = {}
    for pref in data['preferencias']:
        tipo = pref['tipo_preferencia']
        pref_types[tipo] = pref_types.get(tipo, 0) + 1
    for tipo, count in pref_types.items():
        print(f"  - {tipo}: {count} preferências")
    
    # Interações
    print(f"\n🔗 Relacionamentos:")
    print(f"  - Usuário-Preferência: {len(data['usuario_preferencia'])} conexões")
    print(f"  - Estabelecimento-Preferência: {len(data['estabelecimento_preferencia'])} conexões")
    print(f"  - Recomendação Estabelecimento: {len(data['recomendacao_estabelecimento'])} interações")
    print(f"  - Recomendação Usuário: {len(data['recomendacao_usuario'])} similaridades")
    
    return data


def export_data(data):
    """Exporta os dados gerados em múltiplos formatos."""
    
    print("\n" + "="*70)
    print("Exportando Dados")
    print("="*70 + "\n")
    
    output_dir = "/tmp/lightfm_data_export"
    
    print(f"📁 Diretório de saída: {output_dir}")
    print()
    
    # Exportar para todos os formatos
    results = export_all(data, output_dir=output_dir)
    
    print("✅ Exportação concluída!")
    print()
    print("Arquivos gerados:")
    print("-" * 70)
    
    # SQL
    print(f"\n📄 SQL Commands:")
    print(f"  {results['sql']}")
    with open(results['sql'], 'r') as f:
        lines = len(f.readlines())
    print(f"  ({lines} linhas)")
    
    # CSV
    print(f"\n📊 CSV Files:")
    for entity, path in results['csv'].items():
        print(f"  - {entity}.csv: {path}")
    
    # JSON
    print(f"\n📋 JSON Files:")
    for entity, path in results['json'].items():
        print(f"  - {entity}.json: {path}")
    
    print()
    
    # Mostrar preview do SQL
    print("Preview dos comandos SQL (primeiras 30 linhas):")
    print("-" * 70)
    with open(results['sql'], 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 30:
                print("  ...")
                break
            print(f"  {line.rstrip()}")
    
    return results


def usage_instructions():
    """Mostra instruções de uso."""
    
    print("\n" + "="*70)
    print("Como Usar os Dados Gerados")
    print("="*70 + "\n")
    
    print("1️⃣  Usar comandos SQL diretamente:")
    print("    psql -U seu_usuario -d seu_banco -f /tmp/lightfm_data_export/insert_commands.sql")
    print()
    
    print("2️⃣  Importar CSV via Python/pandas:")
    print("    import pandas as pd")
    print("    df = pd.read_csv('/tmp/lightfm_data_export/usuarios.csv')")
    print()
    
    print("3️⃣  Usar JSON em análises:")
    print("    import json")
    print("    with open('/tmp/lightfm_data_export/usuarios.json') as f:")
    print("        usuarios = json.load(f)")
    print()
    
    print("4️⃣  Inserir via biblioteca (requer conexão com BD):")
    print("    from mydata_core import generate_and_insert, GenerationRequest")
    print("    response = generate_and_insert(request)")
    print()
    
    print("5️⃣  Via CLI (mais rápido):")
    print("    mydata-gen generate --schema recommendation_system_lightfm.json")
    print()


def show_filters_example():
    """Mostra exemplo com filtros."""
    
    print("\n" + "="*70)
    print("Exemplo: Gerar apenas dados de Campinas")
    print("="*70 + "\n")
    
    print("Você pode filtrar para gerar apenas estabelecimentos de Campinas:")
    print()
    print("No seu schema JSON, adicione:")
    print("""
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
    """)
    print()
    print("Veja: examples/campinas_filtered.json para exemplo completo!")
    print()


if __name__ == "__main__":
    # Gerar dados
    data = generate_for_lightfm_project()
    
    # Exportar dados
    results = export_data(data)
    
    # Mostrar instruções
    usage_instructions()
    
    # Exemplo de filtros
    show_filters_example()
    
    print("="*70)
    print("✅ PRONTO! Dados gerados e exportados com sucesso!")
    print("="*70)
    print()
    print("Próximos passos:")
    print("  1. Revise os arquivos SQL em: /tmp/lightfm_data_export/")
    print("  2. Execute o SQL no seu banco PostgreSQL")
    print("  3. Use os dados para treinar seu modelo LightFM!")
    print()
    print("💡 Dica: Use filtros para gerar dados apenas de cidades específicas!")
    print("   Exemplo: examples/campinas_filtered.json")
    print()
