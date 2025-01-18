import sqlite3
import random

# Conecta ao banco de dados
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Remove a tabela Departamento se ela já existir para evitar erros
cursor.execute('DROP TABLE IF EXISTS Departamento')

# Criação da tabela Departamento
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departamento (
    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')
print("Tabela Departamento criada.")

# Insere um departamento exemplo (Marketing Digital)
cursor.execute("INSERT INTO Departamento (nome) VALUES ('Marketing Digital')")
conn.commit()

# Criação da tabela Funcionario
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
print("Tabela Funcionario criada.")

# Função para gerar dados aleatórios
def gerar_dados(cargo):
    cpf = ''.join([str(random.randint(0, 9)) for _ in range(11)])
    email = f"{cargo.lower().replace(' ', '')}@empresa.com"
    senha = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    telefone = f"({random.randint(10, 99)}) {random.randint(90000, 99999)}-{random.randint(1000, 9999)}"
    salario = round(random.uniform(3000, 7000), 2)
    return cpf, email, senha, telefone, salario

# Lista de funcionários
funcionarios = [
    "Débora Rafaelle",
    "Alysson Rodrigo",
    "Pedro Lucas",
    "Kayo Fernandes",
    "Pedro Leon",
    "Lucas André"
]

# Insere os funcionários na tabela
for nome in funcionarios:
    cpf, email, senha, telefone, salario = gerar_dados(nome)
    cursor.execute('''
        INSERT INTO Funcionario (nome, CPF, email, senha, telefone, cargo, salario, id_departamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cpf, email, senha, telefone, "Marketing Digital", salario, 1))

conn.commit()
print("Funcionários inseridos com sucesso.")

# Fecha a conexão
conn.close()
