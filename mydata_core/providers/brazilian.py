"""
Brazilian-specific Faker providers for CPF, CNPJ, UF, etc.
"""

import random
from faker.providers import BaseProvider


class BrazilianProvider(BaseProvider):
    """Provider for Brazilian-specific data types."""
    
    # Brazilian states (UF)
    STATES = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]
    
    # Brazilian universities
    UNIVERSITIES = [
        "Universidade Estadual de Campinas (UNICAMP)",
        "Universidade de São Paulo (USP)",
        "Universidade Federal do Rio de Janeiro (UFRJ)",
        "Universidade Federal de Minas Gerais (UFMG)",
        "Universidade Federal do Rio Grande do Sul (UFRGS)",
        "Universidade Estadual Paulista (UNESP)",
        "Universidade de Brasília (UnB)",
        "Universidade Federal de São Paulo (UNIFESP)",
        "Universidade Federal de Santa Catarina (UFSC)",
        "Universidade Federal do Paraná (UFPR)",
    ]
    
    # Brazilian courses
    COURSES = [
        "Engenharia da Computação",
        "Ciência da Computação",
        "Sistemas de Informação",
        "Engenharia de Software",
        "Análise e Desenvolvimento de Sistemas",
        "Medicina",
        "Direito",
        "Administração",
        "Psicologia",
        "Engenharia Civil",
        "Arquitetura e Urbanismo",
        "Biomedicina",
        "Economia",
        "Física",
        "Matemática",
    ]
    
    # Business categories
    BUSINESS_CATEGORIES = [
        "Restaurante",
        "Bar",
        "Café",
        "Lanchonete",
        "Pizzaria",
        "Academia",
        "Cinema",
        "Teatro",
        "Livraria",
        "Shopping",
        "Parque",
        "Museu",
    ]
    
    # Preference types
    PREFERENCE_TYPES = [
        "Alimentação",
        "Ambiente",
        "Lazer",
        "Cultura",
        "Esporte",
        "Entretenimento",
    ]
    
    # Preference names by type
    PREFERENCE_NAMES = {
        "Alimentação": ["Comida Italiana", "Comida Japonesa", "Comida Brasileira", "Fast Food", "Vegano"],
        "Ambiente": ["Silencioso", "Animado", "Familiar", "Romântico", "Casual"],
        "Lazer": ["Ao ar livre", "Indoor", "Esportivo", "Relaxante"],
        "Cultura": ["Arte", "Música", "Literatura", "História"],
        "Esporte": ["Futebol", "Vôlei", "Natação", "Corrida"],
        "Entretenimento": ["Filmes", "Shows", "Jogos", "Dança"],
    }

    def cpf(self) -> str:
        """Generate a valid Brazilian CPF number."""
        def calculate_digit(cpf_list, weight_start):
            total = sum(int(cpf_list[i]) * (weight_start - i) for i in range(len(cpf_list)))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Generate first 9 digits
        cpf = [random.randint(0, 9) for _ in range(9)]
        
        # Calculate first verification digit
        cpf.append(calculate_digit(cpf, 10))
        
        # Calculate second verification digit
        cpf.append(calculate_digit(cpf, 11))
        
        # Format as XXX.XXX.XXX-XX
        cpf_str = ''.join(map(str, cpf))
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"

    def cnpj(self) -> str:
        """Generate a valid Brazilian CNPJ number."""
        def calculate_digit(cnpj_list, weights):
            total = sum(int(cnpj_list[i]) * weights[i] for i in range(len(cnpj_list)))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Generate first 12 digits
        cnpj = [random.randint(0, 9) for _ in range(8)]
        cnpj.extend([0, 0, 0, 1])  # Branch code 0001
        
        # First verification digit
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        cnpj.append(calculate_digit(cnpj, weights1))
        
        # Second verification digit
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        cnpj.append(calculate_digit(cnpj, weights2))
        
        # Format as XX.XXX.XXX/XXXX-XX
        cnpj_str = ''.join(map(str, cnpj))
        return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:]}"

    def uf(self) -> str:
        """Generate a Brazilian state abbreviation."""
        return self.random_element(self.STATES)

    def university_name(self) -> str:
        """Generate a Brazilian university name."""
        return self.random_element(self.UNIVERSITIES)

    def course_name(self) -> str:
        """Generate a Brazilian course name."""
        return self.random_element(self.COURSES)

    def business_category(self) -> str:
        """Generate a business category."""
        return self.random_element(self.BUSINESS_CATEGORIES)

    def preference_type(self) -> str:
        """Generate a preference type."""
        return self.random_element(self.PREFERENCE_TYPES)

    def preference_name(self, preference_type: str = None) -> str:
        """Generate a preference name, optionally for a specific type."""
        if preference_type and preference_type in self.PREFERENCE_NAMES:
            return self.random_element(self.PREFERENCE_NAMES[preference_type])
        # Random from any type
        all_names = [name for names in self.PREFERENCE_NAMES.values() for name in names]
        return self.random_element(all_names)

    def opening_hours(self) -> str:
        """Generate opening hours in Brazilian format."""
        days = ["Seg-Sex", "Seg-Sáb", "Todos os dias", "Seg-Dom"]
        start_hour = random.randint(6, 12)
        end_hour = random.randint(18, 23)
        return f"{self.random_element(days)} {start_hour:02d}:00 - {end_hour:02d}:00"

    def password_hash(self) -> str:
        """Generate a mock password hash (bcrypt-like format)."""
        import hashlib
        random_bytes = str(random.randint(100000, 999999)).encode()
        return f"$2b$12${hashlib.sha256(random_bytes).hexdigest()[:53]}"
