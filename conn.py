import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Deletar a tabela Produto antiga, se ela existir
cursor.execute('''
    DROP TABLE IF EXISTS Produto
''')

# Criar a nova tabela Produto com a coluna Status
cursor.execute('''
    CREATE TABLE Produto (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_produto TEXT NOT NULL,
        nome_produto TEXT NOT NULL,
        tipo_produto TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade_estoque INTEGER NOT NULL,
        endereco_estoque TEXT,
        status INTEGER NOT NULL  -- Status (1 = Em Estoque, 2 = Em Falta)
    )
''')

# Confirmar as alterações
conn.commit()

# Fechar a conexão
conn.close()

print("Tabela Produto recriada com sucesso.")
