import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Criar a tabela Financas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Financas (
        id_financa INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_transacao INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data_transacao TEXT NOT NULL,
        categoria TEXT NOT NULL,
        id_funcionario INTEGER,
        FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
    )
''')

# Limpar dados existentes
cursor.execute('DELETE FROM Financas')

# Novos dados a serem inseridos
transacoes = [
    # Tipo de transação, Descrição, Valor, Data, Categoria
    # SALDO
    (3, "Saldo Inicial", 25450.00, "01/01/2024", "saldo"),  # SALDO
    
    # A RECEBER
    (1, "Pagamento de contrato - Cliente João Silva", 5000.00, "10/01/2024", "a receber"),
    (1, "Serviço de manutenção - Cliente Maria Oliveira", 10000.00, "15/01/2024", "a receber"),
    (1, "Desenvolvimento de software - Cliente Carlos Mendes", 5000.00, "20/01/2024", "a receber"),
    (1, "Venda de equipamento - Cliente Ana Santos", 5000.00, "25/01/2024", "a receber"),
    (1, "Serviço de consultoria - Cliente Lucas Pereira", 2450.00, "30/01/2024", "a receber"),  # Totaliza 25.450,00
    
    # DEVENDO
    (2, "Pagamento fornecedor de software - Fornecedor TechCorp", 10000.00, "05/01/2024", "devendo"),
    (2, "Compra de peças - Fornecedor Peças Rápidas", 5000.00, "10/01/2024", "devendo"),
    (2, "Serviço de hospedagem - Fornecedor HostingPro", 5000.00, "15/01/2024", "devendo"),
    (2, "Licenciamento de software - Fornecedor Licenças Ltda", 5000.00, "20/01/2024", "devendo"),
    (2, "Consultoria de TI - Fornecedor Consultoria XYZ", 2450.00, "25/01/2024", "devendo"),  # Totaliza 25.450,00
]

# Inserir os novos dados
for transacao in transacoes:
    tipo_transacao = transacao[0]  # Obter o tipo de transação
    descricao = transacao[1]
    valor = transacao[2]  # Valor já está em formato float
    data_transacao = transacao[3]
    
    # Inserir na tabela
    cursor.execute('''
        INSERT INTO Financas (tipo_transacao, descricao, valor, data_transacao, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (tipo_transacao, descricao, valor, data_transacao, "geral"))

# Salvar (commit) as mudanças e fechar a conexão
conn.commit()
conn.close()

print("Novos dados inseridos com sucesso!")
