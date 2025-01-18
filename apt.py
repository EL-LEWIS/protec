import sqlite3

# Apenas execute uma vez para corrigir o formato das datas existentes
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Supondo que as datas estejam no formato '%d/%m/%Y'
cursor.execute("""
    UPDATE Financas 
    SET data_transacao = strftime('%Y-%m-%d', substr(data_transacao, 7, 4) || '-' || substr(data_transacao, 4, 2) || '-' || substr(data_transacao, 1, 2))
    WHERE data_transacao LIKE '__/__/____'
""")

conn.commit()
conn.close()
