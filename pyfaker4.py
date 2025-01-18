import sqlite3
from faker import Faker
import random

# Conectar ao banco de dados
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Inicializar o Faker
faker = Faker('pt_BR')  # Usando o Faker em Português

# Categorias de produtos
categorias = ['Periférico', 'Hardware', 'Software']

# Gerar e inserir dados fictícios
for _ in range(20):  # Gerar 20 produtos fictícios
    nome_produto = faker.word().capitalize() + ' ' + random.choice(['Mouse', 'Teclado', 'Monitor', 'Placa-mãe', 'SSD', 'Antivírus', 'Sistema Operacional'])
    codigo_produto = faker.unique.ean(length=8)  # Gera um código único
    tipo_produto = random.choice(categorias)
    preco = round(random.uniform(100.0, 2000.0), 2)  # Preço entre 100 e 2000 reais
    quantidade_estoque = random.randint(0, 50)  # Quantidade entre 0 e 50
    endereco_estoque = faker.street_address()
    
    # Definir o status do produto (1 = Em Estoque, 2 = Em Falta)
    status = 1 if quantidade_estoque > 0 else 2
    
    # Inserir o produto no banco de dados
    cursor.execute('''
        INSERT INTO Produto (codigo_produto, nome_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (codigo_produto, nome_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque, status))

# Confirmar as alterações no banco de dados
conn.commit()

# Fechar a conexão
conn.close()

print("Dados falsos inseridos com sucesso.")
