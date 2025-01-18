import sqlite3
from faker import Faker
import random

# Conectar ao banco de dados
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Função para gerar produtos fictícios
def gerar_produtos_ficticios(qtd):
    faker = Faker('pt_BR')
    categorias = ['Hardware', 'Software', 'Acessório', 'Periférico', 'Dispositivo', 'Sistema Operacional']
    
    for _ in range(qtd):
        nome_produto = faker.company() + " " + random.choice(['Pro', 'Lite', 'X', 'V2', 'Max'])
        codigo_produto = faker.bothify(text='???-#####')
        tipo_produto = random.choice(categorias)
        preco = round(random.uniform(50, 5000), 2)  # Gera preços entre R$ 50 e R$ 5000
        quantidade_estoque = random.randint(0, 200)  # Gera quantidade de 0 a 200
        endereco_estoque = faker.street_address()

        # Inserir produto no banco de dados
        cursor.execute('''
            INSERT INTO Produto (codigo_produto, nome_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (codigo_produto, nome_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque))

    conn.commit()

# Gerar 50 produtos fictícios
gerar_produtos_ficticios(50)

# Fechar a conexão
conn.close()
