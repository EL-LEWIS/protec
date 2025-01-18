import sqlite3
from faker import Faker
import random

# Inicializando o Faker
fake = Faker()

# Conectando ao banco de dados SQLite (ou criando um novo)
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Criando a tabela Funcionario
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Funcionario (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        CPF TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        telefone TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario REAL NOT NULL,
        id_departamento INTEGER NOT NULL,
        FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
    )
''')

# (Opcional) Criando uma tabela Departamento para referência
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departamento (
        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_departamento TEXT NOT NULL
    )
''')

# Inserindo dados fictícios na tabela Departamento
departamentos = ['RH', 'Vendas', 'TI', 'Financeiro', 'Marketing']
for dep in departamentos:
    cursor.execute('INSERT INTO Departamento (nome_departamento) VALUES (?)', (dep,))

# Inserindo 100 funcionários com dados gerados pelo Faker
for _ in range(100):
    nome = fake.name()
    cpf = fake.ssn()  # Gera um CPF fictício (sem validação)
    email = fake.email()
    senha = fake.password()
    telefone = fake.phone_number()
    cargo = random.choice(['Gerente', 'Analista', 'Assistente', 'Coordenador', 'Estagiário'])
    salario = round(random.uniform(3000, 15000), 2)  # Salário entre 3000 e 15000
    id_departamento = random.randint(1, len(departamentos))  # ID aleatório entre os departamentos

    cursor.execute('''
        INSERT INTO Funcionario (nome, CPF, email, senha, telefone, cargo, salario, id_departamento) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cpf, email, senha, telefone, cargo, salario, id_departamento))

# Commitando as mudanças e fechando a conexão
conn.commit()
conn.close()

print("Banco de dados criado e 100 funcionários inseridos com sucesso!")
