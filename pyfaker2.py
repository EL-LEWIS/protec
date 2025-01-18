import sqlite3
from faker import Faker

# Inicializar o Faker
fake = Faker('pt_BR')  # pt_BR para dados no formato brasileiro

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Função para gerar e adicionar clientes físicos aleatórios
def adicionar_cliente_fisico(quantidade):
    for _ in range(quantidade):
        nome = fake.name()
        cpf = fake.cpf()
        endereco = fake.address()
        telefone = fake.phone_number()
        email_cliente = fake.email()
        senha = fake.password()

        cursor.execute('''
            INSERT INTO Cliente_Fisico (nome, CPF, endereco, telefone, email_cliente, senha)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, cpf, endereco, telefone, email_cliente, senha))
    
    conn.commit()
    print(f'{quantidade} clientes físicos adicionados.')

# Função para gerar e adicionar clientes jurídicos aleatórios
def adicionar_cliente_juridico(quantidade):
    for _ in range(quantidade):
        cnpj = fake.cnpj()
        nome_empresa = fake.company()
        nome_representante = fake.name()
        email_empresa = fake.company_email()
        telefone_empresa = fake.phone_number()
        telefone_representante = fake.phone_number()
        email_representante = fake.email()

        cursor.execute('''
            INSERT INTO Cliente_Juridico (CNPJ, nome_empresa, nome_representante, email_empresa, telefone_empresa, telefone_representante, email_representante)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cnpj, nome_empresa, nome_representante, email_empresa, telefone_empresa, telefone_representante, email_representante))
    
    conn.commit()
    print(f'{quantidade} clientes jurídicos adicionados.')

# Exemplo de uso: Adicionar 10 clientes físicos e 5 clientes jurídicos
adicionar_cliente_fisico(10)
adicionar_cliente_juridico(5)

# Fechar a conexão com o banco de dados
conn.close()
