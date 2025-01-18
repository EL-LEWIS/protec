import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

# Conectando ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servicos(
        ID_servico INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_cliente INTEGER NOT NULL,
        ID_funcionario INTEGER NOT NULL,
        tipo VARCHAR(60),
        valor FLOAT,
        data_solicitacao DATE,
        data_finalizacao DATE,
        status_servico INTEGER,
        descricao VARCHAR(300),
        FOREIGN KEY(ID_cliente) REFERENCES cliente_fisico(ID_cliente),
        FOREIGN KEY(ID_funcionario) REFERENCES funcionario(ID_funcionario)
    )
    ''')
    conn.commit()
    return conn

# Função para carregar dados na tabela
def carregar_dados():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, valor, data_solicitacao, '10%', 'Ações' FROM servicos")
    rows = cursor.fetchall()
    for row in rows:
        tabela.insert('', 'end', values=row)
    conn.close()

# Criando a janela principal
root = tk.Tk()
root.geometry("960x600")
root.title("Serviços")

# Cabeçalho
frame_header = tk.Frame(root, bg="white")
frame_header.pack(fill="x")

btn_servico = tk.Button(frame_header, text=" SERVIÇO ", bg="blue", fg="white", font=("Arial", 12, "bold"))
btn_servico.pack(side="left", padx=20, pady=10)

btn_relatorio = tk.Button(frame_header, text=" RELATORIO ", bg="green", fg="white", font=("Arial", 12, "bold"))
btn_relatorio.pack(side="right", padx=20, pady=10)

# Frame para Tabela
frame_tabela = tk.Frame(root)
frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

# Criando a tabela
colunas = ("Nome", "Valor", "Data", "Comissão %", "Ações")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
for coluna in colunas:
    tabela.heading(coluna, text=coluna)

# Definindo o layout da tabela
tabela.column("Nome", anchor="center", width=150)
tabela.column("Valor", anchor="center", width=100)
tabela.column("Data", anchor="center", width=100)
tabela.column("Comissão %", anchor="center", width=100)
tabela.column("Ações", anchor="center", width=100)
tabela.pack(fill="both", expand=True)

# Botões de ações
def criar_botao_acao(imagem_path):
    imagem = Image.open(imagem_path).resize((20, 20))
    imagem_tk = ImageTk.PhotoImage(imagem)
    botao = tk.Button(root, image=imagem_tk, bd=0, highlightthickness=0)
    botao.image = imagem_tk
    return botao

# Botões arredondados nas ações da tabela
frame_acoes = tk.Frame(frame_tabela)
editar_btn = criar_botao_acao("editar.png")  # Substitua com o caminho correto da imagem
excluir_btn = criar_botao_acao("excluir.png")
editar_btn.pack(side="left", padx=5)
excluir_btn.pack(side="left", padx=5)

# Configuração de barra de rolagem
scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
tabela.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Carregar dados do banco de dados na tabela
carregar_dados()

root.mainloop()
