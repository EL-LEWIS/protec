import sqlite3

# Conecte-se ao banco de dados (substitua 'seu_banco.db' pelo nome do seu banco de dados)
conexao = sqlite3.connect('seu_banco_de_dados.db')
cursor = conexao.cursor()

# Deletar a tabela Funcionario, se existir
cursor.execute('DROP TABLE IF EXISTS Funcionario')

# Criar a tabela Funcionario com a nova estrutura
cursor.execute('''
    CREATE TABLE Funcionario (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        CPF TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        telefone TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario REAL NOT NULL,
        id_departamento INTEGER NOT NULL,
        data_admissao TEXT,  -- Adicionando a coluna data_admissao
        FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
    )
''')

# Confirma as alterações
conexao.commit()

# Fecha a conexão
conexao.close()

print("Tabela Funcionario recriada com sucesso!")