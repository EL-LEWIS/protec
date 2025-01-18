import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import Image, ImageDraw, ImageTk, ImageFont
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import Label, Button, Entry
from datetime import datetime, timedelta
import re
from tkinter import Canvas



#-----------------Validador de CPF & CNPJ -------------------
# Função para validar CPF
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)  # Remove caracteres não numéricos
    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):  # Checa tamanho e repetição
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

# Função para validar CNPJ
def validar_cnpj(CNPJ):
    # Remove caracteres não numéricos (incluindo . e /)
    CNPJ = re.sub(r'[^0-9]', '', CNPJ)
    
    # Verifica se o CNPJ possui 14 dígitos
    if len(CNPJ) != 14:
        return False
    
    # Cálculo do primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(int(CNPJ[i]) * pesos1[i] for i in range(12))
    digito1 = 0 if soma1 % 11 < 2 else 11 - (soma1 % 11)
    
    # Verifica se o primeiro dígito está correto
    if digito1 != int(CNPJ[12]):
        return False
    
    # Cálculo do segundo dígito verificador
    pesos2 = [6] + pesos1  # O primeiro peso do segundo dígito é 6
    soma2 = sum(int(CNPJ[i]) * pesos2[i] for i in range(13))
    digito2 = 0 if soma2 % 11 < 2 else 11 - (soma2 % 11)
    
    # Verifica se o segundo dígito está correto
    if digito2 != int(CNPJ[13]):
        return False
    
    return True

#-----------------Conexão com Banco de Dados-----------------
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()
# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('estoque.db')
c = conn.cursor()

def conectar_banco():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    
    # Criação da tabela Produto, caso ainda não exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produto(
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_produto TEXT NOT NULL,
            nome_produto TEXT NOT NULL,
            tipo_produto TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            endereco_estoque TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def ver_detalhes():
    Mostrar_financas(frame_conteudo)

#funções------------------------------------------
#Meus-Dados
def carregar_imagem(nome_arquivo, tamanho):
    imagem = Image.open(nome_arquivo)
    imagem = imagem.resize(tamanho, Image.LANCZOS)
    return ImageTk.PhotoImage(imagem)

def obter_dados_funcionario():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nome, CPF, email, telefone, cargo
        FROM Funcionario
        WHERE id_funcionario = 1
    ''')
    dados = cursor.fetchone()
    conn.close()
    return dados if dados else ("", "", "", "", "")

def def_mostrar_dados(frame_conteudo):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: HOME --> MEUS DADOS")

    # Sidebar
    sidebar = tk.Frame(frame_conteudo, bg="#f1f1f1", width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    titulo_sidebar = tk.Label(sidebar, text="MINHA AREA", font=("Helvetica", 16, "bold"), fg="blue", bg="#f1f1f1")
    titulo_sidebar.pack(pady=20)

    botoes_sidebar = [("Dados Cadastrados", "#0056b3"), ("Alterar Senha", "blue"), ("Privacidade", "blue")]
    for texto, cor in botoes_sidebar:
        botao = tk.Label(sidebar, text=texto, font=("Helvetica", 12, "bold"), fg=cor, bg="#f1f1f1", cursor="hand2")
        botao.pack(pady=5, anchor="w", padx=15)

    # Conteúdo principal
    conteudo_frame = tk.Frame(frame_conteudo, bg="white")
    conteudo_frame.pack(side="right", fill="both", expand=True)

    # Caminho de navegação e título
    caminho_frame = tk.Frame(conteudo_frame, bg="white")
    caminho_frame.pack(anchor="w", padx=10, pady=5)

    # Ícone de home
    try:
        imagem_home = carregar_imagem("home_1.png", (20, 20))
        label_imagem_home = tk.Label(caminho_frame, image=imagem_home, bg="white")
        label_imagem_home.image = imagem_home
        label_imagem_home.pack(side="left", padx=5)
    except Exception as e:
        print(f"Erro ao carregar a imagem home: {e}")

    caminho_label = tk.Label(caminho_frame, text="Minha área > Dados Cadastrados", font=("Helvetica", 10), bg="white")
    caminho_label.pack(side="left", padx=5)

    titulo_label = tk.Label(conteudo_frame, text="Dados Cadastrados", font=("Arial", 18, "bold"), bg="white")
    titulo_label.pack(pady=(10, 20))

    # Dados do funcionário
    dados = obter_dados_funcionario()

    campos = [
        ("Nome", dados[0]),
        ("CPF", dados[1]),
        ("Data de Nascimento", ""),
        ("Telefone", dados[3]),
        ("Email", dados[2]),
        ("Cargo", dados[4]),
        ("Escala", ""),
        ("Endereço", "")
    ]

    # Organizar os campos em uma grade para melhor alinhamento
    campos_frame = tk.Frame(conteudo_frame, bg="white")
    campos_frame.pack(anchor="w", padx=20, pady=10)

    for i, (campo, valor) in enumerate(campos):
        # Definindo as posições da grade
        row = i // 2
        col = i % 2

        label_campo = tk.Label(campos_frame, text=campo, font=("Helvetica", 12), bg="white")
        label_campo.grid(row=row, column=col*2, padx=5, pady=5, sticky="e")

        entry_valor = tk.Entry(campos_frame, font=("Helvetica", 12), width=25)
        entry_valor.insert(0, valor)
        entry_valor.config(state="readonly")  # Somente leitura
        entry_valor.grid(row=row, column=col*2 + 1, padx=5, pady=5, sticky="w")

    # Para manter a largura das colunas consistente, você pode ajustar a largura dos `Entry`
    campos_frame.grid_columnconfigure(1, weight=1)
    campos_frame.grid_columnconfigure(3, weight=1)

#-------------------------------------------------
#FUNÇÃO DA FRAME HOME
def carregar_imagem(caminho, tamanho):
    try:
        imagem = Image.open(caminho)
        imagem = imagem.convert("RGBA")  # Assegurar transparência
        imagem = imagem.resize(tamanho, Image.ANTIALIAS)  # Redimensiona exatamente para o tamanho desejado
        
        fundo_transparente = Image.new("RGBA", tamanho, (255, 255, 255, 0))  # Fundo transparente
        fundo_transparente.paste(imagem, (0, 0), imagem)
        return ImageTk.PhotoImage(fundo_transparente)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return None

# Função para carregar imagens
def carregar_imagem(caminho, tamanho):
    img = Image.open(caminho)
    img = img.resize(tamanho, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

# Função para criar um fundo arredondado para os botões
def create_rounded_rectangle(width, height, color, corner_radius):
    img = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (width, height)], corner_radius, fill=color
    )
    return ImageTk.PhotoImage(img)

# Função para obter os totais do banco de dados
def obter_totais():
    conn = sqlite3.connect("seu_banco_de_dados.db")
    cursor = conn.cursor()

    # Consultas para cada tipo de transação
    cursor.execute("SELECT SUM(valor) FROM Financas WHERE tipo_transacao = '1'")
    total_receber = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(valor) FROM Financas WHERE tipo_transacao = '2'")
    total_pagar = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(valor) FROM Financas WHERE tipo_transacao = '3'")
    receita_menos_despesas = cursor.fetchone()[0] or 0

    # Calcula a diferença entre "Recebidos - Pagos"
    recebidos_menos_pagos = total_receber - total_pagar

    conn.close()
    return total_receber, total_pagar, receita_menos_despesas, recebidos_menos_pagos

# Função para criar a janela principal
def criar_janela_home(frame_conteudo):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    frame_conteudo.configure(bg="white")
    # Alterar o título da janela
    root.title("PROTEC Admin: HOME")

    # Foto de perfil e nome do administrador
    frame_admin = tk.Frame(frame_conteudo, bg="white")
    frame_admin.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Carregar imagem de perfil (Ajustar caminho da imagem)
    try:
        imagem_perfil = carregar_imagem('perfil.png', (50, 50))  # Redimensiona para 50x50
        label_imagem = tk.Label(frame_admin, image=imagem_perfil, bg="white")
        label_imagem.image = imagem_perfil  # Manter referência
        label_imagem.pack(side="left", padx=10)
    except Exception as e:
        print(f"Erro ao carregar imagem de perfil: {e}")

    # Label com o nome "Administrador"
    label_admin = tk.Label(frame_admin, text="Administrador", font=("Helvetica", 14), bg="white")
    label_admin.pack(side="left", padx=10)

    # Criar a linha preta logo abaixo do administrador
    linha_preta = tk.Frame(frame_conteudo, bg="black", height=2, width=600)  # Ajuste a largura conforme necessário
    linha_preta.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Botão de sair no canto superior direito
    btn_sair = tk.Button(frame_conteudo, image=icone_exit, text=" Sair", compound="left", anchor="w", bg="white", fg="red", bd=0, font=("Helvetica", 12), command=sair)
    btn_sair.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # Título "Visão Geral"
    titulo = tk.Label(frame_conteudo, text="Visao Geral", font=("Arial", 24, "bold"), bg="white")
    titulo.grid(row=2, column=0, padx=20, pady=20, sticky="nw")

    # Criar um frame para exibir os resumos financeiros
    frame_imagens = tk.Frame(frame_conteudo, bg="white")
    frame_imagens.grid(row=3, column=0, padx=20, pady=20, sticky="nw")

    # 4 TELAS AQUI!!!------

    # Obtém os totais do banco de dados
    total_receber, total_pagar, receita_menos_despesas, recebidos_menos_pagos = obter_totais()

    # Parâmetros dos botões de resumo financeiro
    button_params = [
        {"text": f"R$ {total_receber:,.2f}\nTotal de Títulos a Receber(R$)", "bg_color": "#46b747", "button_color": "#1f7031", "text_color": "white"},
        {"text": f"R$ {receita_menos_despesas:,.2f}\nRecebidos - Pagos(R$)", "bg_color": "#6ae06b", "button_color": "#1f7031", "text_color": "white"},
        {"text": f"R$ {recebidos_menos_pagos:,.2f}\nReceita - Despesas(R$)", "bg_color": "#3aa747", "button_color": "#1c6524", "text_color": "white"},
        {"text": f"R$ {total_pagar:,.2f}\nTotal de Títulos a Pagar(R$)", "bg_color": "#e05044", "button_color": "#a43a34", "text_color": "white"},
    ]

    # Dimensões e estilo dos botões de resumo financeiro
    width, height = 250, 150
    corner_radius = 20

    # Criação dos botões de resumo financeiro
    for idx, params in enumerate(button_params):
        # Criar fundo arredondado para o botão
        bg_image = create_rounded_rectangle(width, height, params["bg_color"], corner_radius)
        
        # Frame do botão
        btn_frame = tk.Label(frame_imagens, image=bg_image, bd=0, bg="white")
        btn_frame.image = bg_image  # Manter uma referência da imagem
        
        # Texto do botão
        btn_text = tk.Label(btn_frame, text=params["text"], fg=params["text_color"], font=("Arial", 12, "bold"), bg=params["bg_color"])
        btn_text.place(relx=0.5, rely=0.3, anchor="center")
        
        # Botão de "Ver detalhes" com fundo escuro personalizado
        details_button = tk.Button(btn_frame, text="Ver detalhes", font=("Arial", 10), bg=params["button_color"], fg="white", borderwidth=0, command=ver_detalhes)
        details_button.place(relx=0.25, rely=0.75, anchor="center")
        
        # Setinha no botão
        arrow_label = tk.Label(btn_frame, text="←", fg="black", bg=params["bg_color"], font=("Arial", 12, "bold"))
        arrow_label.place(relx=0.85, rely=0.75, anchor="center")
        
        # Posicionando os botões no frame_imagens
        btn_frame.grid(row=idx // 2, column=idx % 2, padx=20, pady=20, sticky="nw")

    # Frame lateral para botões adicionais
    lateral_frame = tk.Frame(frame_conteudo, bg="white")
    lateral_frame.grid(row=3, column=1, padx=20, pady=20, sticky="n")

    # Botões laterais
    botoes_laterais = [
        ("meusdados.png", "#FFD700", lambda: def_mostrar_dados(frame_conteudo)),
        ("duvidas.png", "#B0C4DE", None),
        ("sistemupdate.png", "#8B4513", None),
        ("configuracoes.png", "#483D8B", None)
    ]

    for i, (icone, cor_fundo, command) in enumerate(botoes_laterais):
        try:
            img_icone = carregar_imagem(icone, (150, 60))
            btn = tk.Button(lateral_frame, image=img_icone, borderwidth=0, highlightthickness=0, bg=cor_fundo, command=command)
            btn.image = img_icone
            btn.grid(row=i, column=0, pady=5, sticky="ew")
        except Exception as e:
            print(f"Erro ao carregar ícone {icone}: {e}")

    # Ajustar a visualização
    lateral_frame.pack_propagate(False)

#-------------------------------------------------
#FUNÇÃO DA FRAME FUNCIONARIOS
def exibir_funcionarios():
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: FUNCIONÁRIOS")

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Função para buscar funcionários por nome
    def buscar_funcionarios():
        filtro_nome = entry_pesquisa.get()
        if filtro_nome.strip() == "":
            query = "SELECT nome, CPF, email, telefone FROM Funcionario"
            cursor.execute(query)
        else:
            query = "SELECT nome, CPF, email, telefone FROM Funcionario WHERE nome LIKE ?"
            cursor.execute(query, ('%' + filtro_nome + '%',))

        funcionarios = cursor.fetchall()
        if not funcionarios:
            messagebox.showinfo("Nenhum resultado", "Nenhum funcionário encontrado com esse nome.")
        else:
            atualizar_tabela(funcionarios)

    # Função para atualizar a tabela
    def atualizar_tabela(funcionarios):
        for row in tree.get_children():
            tree.delete(row)
        for funcionario in funcionarios:
            tree.insert("", "end", values=funcionario)

    # Função para abrir uma janela de edição de funcionários
    def editar_funcionario():
        item_selecionado = tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um funcionário para editar.")
            return

        valores = tree.item(item_selecionado, 'values')
        cpf_selecionado = valores[1]

        # Abrir nova janela para edição
        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar Funcionário")
        janela_edicao.geometry("400x300")
        janela_edicao.configure(bg="#F7F9FB")

        # Estilizar os botões
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), background="#2E3B59", foreground="white")

        # Título da janela de edição
        tk.Label(janela_edicao, text="Editar Funcionário", font=("Helvetica", 14, "bold"), bg="#F7F9FB").pack(pady=10)

        # Frame para os campos de edição
        frame_campos = tk.Frame(janela_edicao, bg="#F7F9FB")
        frame_campos.pack(padx=20, pady=10, fill="both", expand=True)

        # Campos de entrada para editar o funcionário
        ttk.Label(frame_campos, text="Nome").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        entry_nome = ttk.Entry(frame_campos)
        entry_nome.grid(row=0, column=1, padx=10, pady=5)
        entry_nome.insert(0, valores[0])

        ttk.Label(frame_campos, text="CPF").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        entry_cpf = ttk.Entry(frame_campos)
        entry_cpf.grid(row=1, column=1, padx=10, pady=5)
        entry_cpf.insert(0, valores[1])
        entry_cpf.config(state='disabled')  # CPF não editável

        ttk.Label(frame_campos, text="E-mail").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        entry_email = ttk.Entry(frame_campos)
        entry_email.grid(row=2, column=1, padx=10, pady=5)
        entry_email.insert(0, valores[2])

        ttk.Label(frame_campos, text="Telefone").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        entry_telefone = ttk.Entry(frame_campos)
        entry_telefone.grid(row=3, column=1, padx=10, pady=5)
        entry_telefone.insert(0, valores[3])

        # Função para salvar as alterações
        def salvar_alteracoes():
            novo_nome = entry_nome.get()
            novo_email = entry_email.get()
            novo_telefone = entry_telefone.get()

            try:
                conn = sqlite3.connect('seu_banco_de_dados.db')
                cursor = conn.cursor()

                # Atualizar no banco de dados usando o CPF como referência
                cursor.execute("""
                    UPDATE Funcionario
                    SET nome = ?, email = ?, telefone = ?
                    WHERE CPF = ?
                """, (novo_nome, novo_email, novo_telefone, cpf_selecionado))

                conn.commit()  # Confirma as alterações
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")

                # Atualiza a tabela com os novos dados
                buscar_funcionarios()
                atualizar_tabela(funcionarios)

                # Fechar a janela de edição após salvar
                janela_edicao.destroy()

            except Exception as e:
                pass
    
            finally:
                conn.close()

        # Função para deletar o funcionário
        def deletar_funcionario():
            confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este funcionário?")
            if confirmar:
                try:
                    conn = sqlite3.connect('seu_banco_de_dados.db')
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM Funcionario WHERE CPF = ?", (cpf_selecionado,))
                    conn.commit()

                    messagebox.showinfo("Sucesso", "Funcionário deletado com sucesso!")
                    buscar_funcionarios()
                    janela_edicao.destroy()

                except Exception as e:
                    pass
                
                finally:
                    conn.close()

        # Botões de ação
        frame_botoes = tk.Frame(janela_edicao, bg="#F7F9FB")
        frame_botoes.pack(pady=10)

        btn_salvar = ttk.Button(frame_botoes, text="Salvar", command=salvar_alteracoes)
        btn_salvar.grid(row=0, column=0, padx=10)

        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=janela_edicao.destroy)
        btn_cancelar.grid(row=0, column=1, padx=10)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=deletar_funcionario)
        btn_deletar.grid(row=0, column=2, padx=10)

    # Título da página de funcionários
    label_titulo = tk.Label(frame_conteudo, text="Funcionários", font=("Helvetica", 16, "bold"), bg="white")
    label_titulo.pack(pady=10)

    # Frame que vai conter a tabela e outros elementos
    frame_tabela = tk.Frame(frame_conteudo, bg="white", bd=2, relief="solid")
    frame_tabela.pack(padx=20, pady=20, fill="both", expand=True)

    # Barra de pesquisa
    frame_pesquisa = tk.Frame(frame_tabela, bg="white")
    frame_pesquisa.pack(pady=10)

    label_pesquisa = tk.Label(frame_pesquisa, text="Buscar:", bg="white", font=("Helvetica", 12))
    label_pesquisa.pack(side="left", padx=5)

    entry_pesquisa = tk.Entry(frame_pesquisa, font=("Helvetica", 12), width=30)
    entry_pesquisa.pack(side="left", padx=5)

    btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=buscar_funcionarios, bg="#2E3B59", fg="white", font=("Helvetica", 12))
    btn_pesquisar.pack(side="left", padx=5)

    # Tabela de funcionários
    colunas = ("Nome", "CPF", "E-mail", "Telefone")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("E-mail", text="E-mail")
    tree.heading("Telefone", text="Telefone")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Botão de editar
    btn_editar = tk.Button(frame_tabela, text="Editar Funcionário", command=editar_funcionario, bg="#2E3B59", fg="white", font=("Helvetica", 12))
    btn_editar.pack(pady=10)

    # Carregar os funcionários inicialmente
    cursor.execute("SELECT nome, CPF, email, telefone FROM Funcionario")
    funcionarios = cursor.fetchall()
    atualizar_tabela(funcionarios)

    # Fechar a conexão com o banco de dados
    conn.close()

# Conectar ao banco de dados e criar a tabela Funcionario
def criar_tabela():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()
#-------------------------------------------------
#FUNÇÃO DA FRAME CLIENTES
def exibir_clientes(tipo_cliente):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: CLIENTES")

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Definir o tipo de cliente e query de acordo com a seleção
    if tipo_cliente == 'fisico':
        tabela_cliente = 'Cliente_Fisico'
        query = "SELECT nome, CPF, endereco, telefone, email_cliente FROM " + tabela_cliente
        colunas = ("Nome", "CPF", "Endereço", "Telefone", "E-mail")
    else:
        tabela_cliente = 'Cliente_Juridico'
        query = "SELECT nome_empresa, CNPJ, nome_representante, telefone_empresa, email_empresa FROM " + tabela_cliente
        colunas = ("Empresa", "CNPJ", "Representante", "Telefone", "E-mail")

    # Função para buscar clientes por nome
    def buscar_clientes():
        filtro_nome = entry_pesquisa.get()
        if tipo_cliente == 'fisico':
            query = "SELECT nome, CPF, endereco, telefone, email_cliente FROM " + tabela_cliente + " WHERE nome LIKE ?"
        else:
            query = "SELECT nome_empresa, CNPJ, nome_representante, telefone_empresa, email_empresa FROM " + tabela_cliente + " WHERE nome_empresa LIKE ?"
        cursor.execute(query, ('%' + filtro_nome + '%',))
        clientes = cursor.fetchall()
        atualizar_tabela(clientes)
        
    def atualizar():
        # Limpa a tabela atual
        for row in tree.get_children():
            tree.delete(row)

        # Conecta ao banco de dados e recupera os clientes
        conn = sqlite3.connect('seu_banco_de_dados.db')
        cursor = conn.cursor()

        try:
            if tipo_cliente == 'fisico':
                cursor.execute("SELECT nome, CPF, endereco, telefone, email_cliente FROM " + tabela_cliente)
            else:
                cursor.execute("SELECT nome_empresa, CNPJ, nome_representante, telefone_empresa, email_empresa FROM " + tabela_cliente)

            # Adiciona os novos dados ao Treeview
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar clientes: {e}")

        finally:
            conn.close()

    # Função para atualizar a tabela
    def atualizar_tabela(clientes):
        for row in tree.get_children():
            tree.delete(row)
        for cliente in clientes:
            tree.insert("", "end", values=cliente)

    # Função para editar as informações de um cliente selecionado
    def editar_cliente():
        item_selecionado = tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um cliente para editar.")
            return

        valores = tree.item(item_selecionado, 'values')
        nome_original = valores[0]

        # Abrir uma nova janela para editar as informações do cliente
        janela_editar_cliente = tk.Toplevel()
        janela_editar_cliente.title(f"Editar Cliente: {nome_original}")

        # Labels e Entrys para editar informações
        tk.Label(janela_editar_cliente, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = tk.Entry(janela_editar_cliente)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, valores[0])

        tk.Label(janela_editar_cliente, text=colunas[1] + ":").grid(row=1, column=0, padx=5, pady=5)
        entry_campo2 = tk.Entry(janela_editar_cliente)
        entry_campo2.grid(row=1, column=1, padx=5, pady=5)
        entry_campo2.insert(0, valores[1])

        tk.Label(janela_editar_cliente, text=colunas[2] + ":").grid(row=2, column=0, padx=5, pady=5)
        entry_campo3 = tk.Entry(janela_editar_cliente)
        entry_campo3.grid(row=2, column=1, padx=5, pady=5)
        entry_campo3.insert(0, valores[2])

        tk.Label(janela_editar_cliente, text=colunas[3] + ":").grid(row=3, column=0, padx=5, pady=5)
        entry_campo4 = tk.Entry(janela_editar_cliente)
        entry_campo4.grid(row=3, column=1, padx=5, pady=5)
        entry_campo4.insert(0, valores[3])

        tk.Label(janela_editar_cliente, text=colunas[4] + ":").grid(row=4, column=0, padx=5, pady=5)
        entry_campo5 = tk.Entry(janela_editar_cliente)
        entry_campo5.grid(row=4, column=1, padx=5, pady=5)
        entry_campo5.insert(0, valores[4])

        # Função para salvar as alterações
    def editar_cliente():
        item_selecionado = tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um cliente para editar.")
            return

        valores = tree.item(item_selecionado, 'values')
        nome_original = valores[0]

        # Abrir uma nova janela para editar as informações do cliente
        janela_editar_cliente = tk.Toplevel()
        janela_editar_cliente.title(f"Editar Cliente: {nome_original}")
        janela_editar_cliente.configure(bg="#4B0082")  # fundo da janela roxo

        # Labels e Entrys para editar informações
        tk.Label(janela_editar_cliente, text="Nome:", bg="#4B0082", fg="white").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = tk.Entry(janela_editar_cliente)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, valores[0])

        tk.Label(janela_editar_cliente, text=colunas[1] + ":", bg="#4B0082", fg="white").grid(row=1, column=0, padx=5, pady=5)
        entry_campo2 = tk.Entry(janela_editar_cliente, state='disabled')  # desativar edição de CPF
        entry_campo2.grid(row=1, column=1, padx=5, pady=5)
        entry_campo2.insert(0, valores[1])

        tk.Label(janela_editar_cliente, text=colunas[2] + ":", bg="#4B0082", fg="white").grid(row=2, column=0, padx=5, pady=5)
        entry_campo3 = tk.Entry(janela_editar_cliente)
        entry_campo3.grid(row=2, column=1, padx=5, pady=5)
        entry_campo3.insert(0, valores[2])

        tk.Label(janela_editar_cliente, text=colunas[3] + ":", bg="#4B0082", fg="white").grid(row=3, column=0, padx=5, pady=5)
        entry_campo4 = tk.Entry(janela_editar_cliente)
        entry_campo4.grid(row=3, column=1, padx=5, pady=5)
        entry_campo4.insert(0, valores[3])

        tk.Label(janela_editar_cliente, text=colunas[4] + ":", bg="#4B0082", fg="white").grid(row=4, column=0, padx=5, pady=5)
        entry_campo5 = tk.Entry(janela_editar_cliente)
        entry_campo5.grid(row=4, column=1, padx=5, pady=5)
        entry_campo5.insert(0, valores[4])

        # Função para salvar as alterações
        def salvar_alteracoes():
            # Abrir a conexão com o banco de dados
            conn = sqlite3.connect('seu_banco_de_dados.db')
            cursor = conn.cursor()

            # Obter os valores dos campos de entrada
            novo_nome = entry_nome.get()
            novo_campo3 = entry_campo3.get()
            novo_campo4 = entry_campo4.get()
            novo_campo5 = entry_campo5.get()

            try:
                if tipo_cliente == 'fisico':
                    cursor.execute("""
                        UPDATE Cliente_Fisico
                        SET nome = ?, endereco = ?, telefone = ?, email_cliente = ?
                        WHERE nome = ?
                    """, (novo_nome, novo_campo3, novo_campo4, novo_campo5, nome_original))
                else:
                    cursor.execute("""
                        UPDATE Cliente_Juridico
                        SET nome_empresa = ?, nome_representante = ?, telefone_empresa = ?, email_empresa = ?
                        WHERE nome_empresa = ?
                    """, (novo_nome, novo_campo3, novo_campo4, novo_campo5, nome_original))

                conn.commit()
                messagebox.showinfo("Sucesso", "As alterações foram salvas com sucesso.")
                buscar_clientes()
            

            except sqlite3.Error as e:
                atualizar()

            finally:
                conn.close()
                janela_editar_cliente.destroy()

        # Função para deletar o cliente
        def deletar_cliente():
            resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este cliente?")
            if resposta:
                try:
                    conn = sqlite3.connect('seu_banco_de_dados.db')
                    cursor = conn.cursor()

                    if tipo_cliente == 'fisico':
                        cursor.execute("DELETE FROM Cliente_Fisico WHERE nome = ?", (nome_original,))
                    else:
                        cursor.execute("DELETE FROM Cliente_Juridico WHERE nome_empresa = ?", (nome_original,))

                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente deletado com sucesso.")
                    buscar_clientes()

                except sqlite3.Error as e:
                    atualizar()

                finally:
                    conn.close()
                    janela_editar_cliente.destroy()

        # Botões de salvar e deletar com design arredondado e cores
        btn_salvar = tk.Button(janela_editar_cliente, text="Salvar Alterações", command=salvar_alteracoes, bg="#6A0DAD", fg="white", font=("Helvetica", 12), relief="flat")
        btn_salvar.grid(row=5, column=0, pady=10, padx=10)

        btn_deletar = tk.Button(janela_editar_cliente, text="Deletar Cliente", command=deletar_cliente, bg="#8A2BE2", fg="white", font=("Helvetica", 12), relief="flat")
        btn_deletar.grid(row=5, column=1, pady=10, padx=10)

    # Adicionar botões para selecionar o tipo de cliente
    frame_tipo_cliente = tk.Frame(frame_conteudo, bg="white")
    frame_tipo_cliente.pack(pady=10)

    btn_fisico = tk.Button(frame_tipo_cliente, text="FÍSICA", command=lambda: exibir_clientes('fisico'), bg="#B0BEC5", fg="black", font=("Helvetica", 12))
    btn_fisico.pack(side="left", padx=10)

    btn_juridico = tk.Button(frame_tipo_cliente, text="JURÍDICA", command=lambda: exibir_clientes('juridico'), bg="#3E50B4", fg="white", font=("Helvetica", 12))
    btn_juridico.pack(side="left", padx=10)

    # Barra de pesquisa
    frame_pesquisa = tk.Frame(frame_conteudo, bg="white")
    frame_pesquisa.pack(pady=10)

    label_pesquisa = tk.Label(frame_pesquisa, text="Buscar:", bg="white", font=("Helvetica", 12))
    label_pesquisa.pack(side="left", padx=5)

    entry_pesquisa = tk.Entry(frame_pesquisa, font=("Helvetica", 12), width=30)
    entry_pesquisa.pack(side="left", padx=5)

    btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=buscar_clientes, bg="#2E3B59", fg="white", font=("Helvetica", 12))
    btn_pesquisar.pack(side="left", padx=5)

    # Frame que vai conter a tabela e adicionar borda
    frame_tabela = tk.Frame(frame_conteudo, bg="white", bd=2, relief="solid")
    frame_tabela.pack(pady=10, padx=10, fill="both", expand=True)

    # Tabela de clientes
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        
    scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    
    tree.pack(fill="both", expand=True)
    scrollbar_x.pack(fill="x")


    # Botão de editar
    btn_editar = tk.Button(frame_conteudo, text="Editar Cliente", command=editar_cliente, bg="#2E3B59", fg="white", font=("Helvetica", 12))
    btn_editar.pack(pady=10)

    # Carregar os clientes inicialmente
    cursor.execute(query)
    clientes = cursor.fetchall()
    atualizar_tabela(clientes)

    # Fechar a conexão com o banco de dados
    conn.close()
#-------------------------------------------------
#FUNÇÕES DA FRAME CADASTROS:

#Função para exibir Cadastros
def cadastrar_funcionario(frame_conteudo):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    frame_conteudo.configure(bg="white")
    root.title("PROTEC Admin: CADASTRO --> FUNCIONÁRIOS")

    # Função para salvar os dados no banco de dados
    def salvar_dados():
        # Conectar ao banco de dados
        conn = sqlite3.connect('seu_banco_de_dados.db')
        cursor = conn.cursor()

        # Criar a tabela Funcionario se ela não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                CPF TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                telefone TEXT NOT NULL,
                cargo TEXT NOT NULL,
                salario REAL NOT NULL,
                data_admissao TEXT NOT NULL,
                id_departamento INTEGER NOT NULL
            )
        ''')

        # Capturar os dados dos campos
        nome = entry_nome.get()
        CPF = entry_CPF.get()
        email = entry_email.get()
        senha = entry_senha.get()
        telefone = entry_telefone.get()
        cargo = combo_cargo.get()
        salario = entry_salario.get()
        data_admissao = entry_data_admissao.get()
        id_departamento = combo_departamento.get()  # Novo campo para id_departamento

        # Verificar se todos os campos obrigatórios estão preenchidos
        if nome and CPF and email and senha and telefone and cargo != "Selecione" and salario and data_admissao and id_departamento != "Selecione":
            try:
                # Inserir os dados no banco de dados
                cursor.execute('''
                    INSERT INTO Funcionario (nome, CPF, email, senha, telefone, cargo, salario, data_admissao, id_departamento) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (nome, CPF, email, senha, telefone, cargo, float(salario), data_admissao, int(id_departamento))
                )
                conn.commit()  # Salvar as mudanças no banco de dados
                messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            except sqlite3.Error as e:
                # Mostrar mensagem de erro detalhada se algo der errado
                messagebox.showerror("Erro", f"Erro ao cadastrar no banco de dados: {e}")
            finally:
                conn.close()  # Fechar a conexão apenas após todas as operações serem concluídas
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")

    # Função para criar placeholders
    def create_placeholder(entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg='black')

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
                entry.config(fg='grey')

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Layout da tela ajustado
    frame_conteudo.configure(bg="white")

    # Título "Funcionários"
    label_titulo = tk.Label(frame_conteudo, text="FUNCIONÁRIOS", font=("Arial", 20, "bold"), bg="white")
    label_titulo.grid(row=0, column=0, columnspan=4, pady=(20, 10), sticky="n")

    # Subtítulo "Inserir Registro"
    label_subtitulo = tk.Label(frame_conteudo, text="Inserir Registro", font=("Arial", 12, "bold"), bg="white")
    label_subtitulo.grid(row=1, column=0, columnspan=4, pady=10, sticky="w", padx=20)

    # Labels e Campos de Entrada
    labels = ["Nome", "CPF", "Data de Admissão", "E-Mail", "Telefone", "Cargo", "Salário", "Senha", "Departamento"]

    for i, label_text in enumerate(labels):
        label = tk.Label(frame_conteudo, text=label_text, font=("Arial", 10), bg="white")
        label.grid(row=2 + i // 3, column=i % 3, padx=20, pady=5, sticky="w")

    # Entradas
    entry_nome = tk.Entry(frame_conteudo, font=("Arial", 10), width=25)
    entry_CPF = tk.Entry(frame_conteudo, font=("Arial", 10), width=25)
    entry_data_admissao = tk.Entry(frame_conteudo, font=("Arial", 10), width=25)
    entry_email = tk.Entry(frame_conteudo, font=("Arial", 10), width=25)
    entry_telefone = tk.Entry(frame_conteudo, font=("Arial", 10), width=25)
    entry_salario = tk.Entry(frame_conteudo, font=("Arial", 10), width=25)
    entry_senha = tk.Entry(frame_conteudo, font=("Arial", 10), width=25, show="*")

    # Adicionando os placeholders
    create_placeholder(entry_nome, "Seu Nome")
    create_placeholder(entry_CPF, "000.000.000-00")
    create_placeholder(entry_data_admissao, "DD/MM/AAAA")
    create_placeholder(entry_email, "Seu E-mail")
    create_placeholder(entry_telefone, "(00) 00000-0000")
    create_placeholder(entry_salario, "0000")
    create_placeholder(entry_senha, "Sua Senha")

    # Combobox para Cargo (RH, Gerente, Funcionário)
    combo_cargo = ttk.Combobox(frame_conteudo, values=["Selecione", "RH", "Gerente", "Funcionário"], font=("Arial", 10), width=23)
    combo_cargo.current(0)  # Definir valor padrão como "Selecione"

    # Combobox para Departamento
    combo_departamento = ttk.Combobox(frame_conteudo, values=["Selecione", "1", "2", "3"], font=("Arial", 10), width=23)
    combo_departamento.current(0)  # Definir valor padrão como "Selecione"

    # Posicionando as entradas na grid
    entry_nome.grid(row=3, column=0, padx=20, pady=5)
    entry_CPF.grid(row=3, column=1, padx=20, pady=5)
    entry_data_admissao.grid(row=3, column=2, padx=20, pady=5)

    entry_email.grid(row=4, column=0, padx=20, pady=5)
    entry_telefone.grid(row=4, column=1, padx=20, pady=5)
    combo_cargo.grid(row=4, column=2, padx=20, pady=5)

    entry_salario.grid(row=5, column=0, padx=20, pady=5)
    entry_senha.grid(row=5, column=1, padx=20, pady=5)
    combo_departamento.grid(row=5, column=2, padx=20, pady=5)  # Campo de departamento na grid

    # Botão "Salvar"
    btn_salvar = tk.Button(frame_conteudo, text="SALVAR", font=("Arial", 12, "bold"), bg="#4A90E2", fg="white", width=10, command=salvar_dados)
    btn_salvar.grid(row=6, column=2, padx=20, pady=20, sticky="e")

#função da janela de cadastro de clientes
def cadastrar_cliente(frame_conteudo):
     # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    frame_conteudo.configure(bg="white")
    root.title("PROTEC Admin: CADASTRO --> CLIENTES")
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Criar tabelas se não existirem
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente_Fisico (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            CPF TEXT NOT NULL,
            endereco TEXT NOT NULL,
            telefone TEXT,
            email_cliente TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente_Juridico (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            CNPJ TEXT NOT NULL,
            nome_empresa TEXT NOT NULL,
            nome_representante TEXT NOT NULL,
            email_empresa TEXT NOT NULL,
            telefone_empresa TEXT,
            telefone_representante TEXT,
            email_representante TEXT
        )
    ''')

    # Função para salvar os dados no banco de dados
    def salvar_cliente():
        tipo_cliente = combo_tipo_cliente.get()

        if tipo_cliente == "Físico":
            nome = entry_nome.get()
            CPF = entry_CPF.get()
            endereco = entry_endereco.get()
            telefone = entry_telefone.get()
            email_cliente = entry_email.get()
            senha = entry_senha.get()
            frame_conteudo.configure(bg="white")

            # Validar CPF antes de prosseguir
            if not validar_cpf(CPF):
                messagebox.showwarning("Aviso", "CPF inválido. Por favor, insira um CPF válido.")
                return

            if nome and CPF and endereco and email_cliente and senha:
                try:
                    # Inserir os dados no banco de dados
                    cursor.execute('''
                        INSERT INTO Cliente_Fisico (nome, CPF, endereco, telefone, email_cliente, senha) 
                        VALUES (?, ?, ?, ?, ?, ?)''', 
                        (nome, CPF, endereco, telefone, email_cliente, senha)
                    )
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente Físico cadastrado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar: {e}")
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")

        elif tipo_cliente == "Jurídico":
            CNPJ = entry_CNPJ.get()
            nome_empresa = entry_nome_empresa.get()
            nome_representante = entry_nome_representante.get()
            email_empresa = entry_email_empresa.get()
            telefone_empresa = entry_telefone_empresa.get()
            telefone_representante = entry_telefone_representante.get()
            email_representante = entry_email_representante.get()
            frame_conteudo.configure(bg="white")

            # Validar CNPJ antes de prosseguir
            if not validar_cnpj(CNPJ):
                messagebox.showwarning("Aviso", "CNPJ inválido. Por favor, insira um CNPJ válido.")
                return

            if CNPJ and nome_empresa and nome_representante and email_empresa:
                try:
                    # Inserir os dados no banco de dados
                    cursor.execute('''
                        INSERT INTO Cliente_Juridico (CNPJ, nome_empresa, nome_representante, email_empresa, telefone_empresa, telefone_representante, email_representante) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (CNPJ, nome_empresa, nome_representante, email_empresa, telefone_empresa, telefone_representante, email_representante)
                    )
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente Jurídico cadastrado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar: {e}")
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")

    # Função para criar placeholders
    def create_placeholder(entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg='black')

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
                entry.config(fg='grey')

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Função para atualizar os campos conforme o tipo de cliente
    def atualizar_campos(event):
        tipo_cliente = combo_tipo_cliente.get()
        
        # Limpando os widgets anteriores
        for widget in frame_form.winfo_children():
            widget.destroy()
        frame_conteudo.configure(bg="white")

        # Variáveis globais para armazenar as entradas
        global entry_nome, entry_CPF, entry_endereco, entry_telefone, entry_email, entry_senha
        global entry_CNPJ, entry_nome_empresa, entry_nome_representante, entry_email_empresa, entry_telefone_empresa, entry_telefone_representante, entry_email_representante
        
        if tipo_cliente == "Físico":
            # Campos para Cliente Físico
            labels_fisico = ["Nome", "CPF", "Endereço", "Telefone", "E-mail", "Senha"]
            entries_fisico = [None]*6  # Lista para armazenar as entradas
            placeholders_fisico = ["Seu Nome", "000.000.000-00", "Seu Endereço", "(00) 00000-0000", "Seu E-mail", "Sua Senha"]

            for i, label_text in enumerate(labels_fisico):
                label = tk.Label(frame_form, text=label_text, font=("Arial", 10), bg="white")
                label.grid(row=i, column=0, padx=20, pady=5, sticky="w")
                
                entries_fisico[i] = tk.Entry(frame_form, font=("Arial", 10), width=30)
                create_placeholder(entries_fisico[i], placeholders_fisico[i])
                entries_fisico[i].grid(row=i, column=1, padx=20, pady=5)

            # Atribuindo as entradas às variáveis globais
            entry_nome, entry_CPF, entry_endereco, entry_telefone, entry_email, entry_senha = entries_fisico

        elif tipo_cliente == "Jurídico":
            # Campos para Cliente Jurídico
            labels_juridico = ["CNPJ", "Nome da Empresa", "Nome do Representante", "E-mail da Empresa", "Telefone da Empresa", "Telefone do Representante", "E-mail do Representante"]
            entries_juridico = [None]*7  # Lista para armazenar as entradas
            placeholders_juridico = ["00.000.000/0000-00", "Nome da Empresa", "Nome do Representante", "E-mail da Empresa", "(00) 00000-0000", "(00) 00000-0000", "E-mail do Representante"]

            for i, label_text in enumerate(labels_juridico):
                label = tk.Label(frame_form, text=label_text, font=("Arial", 10), bg="white")
                label.grid(row=i, column=0, padx=20, pady=5, sticky="w")

                entries_juridico[i] = tk.Entry(frame_form, font=("Arial", 10), width=30)
                create_placeholder(entries_juridico[i], placeholders_juridico[i])
                entries_juridico[i].grid(row=i, column=1, padx=20, pady=5)

            # Atribuindo as entradas às variáveis globais
            entry_CNPJ, entry_nome_empresa, entry_nome_representante, entry_email_empresa, entry_telefone_empresa, entry_telefone_representante, entry_email_representante = entries_juridico

    # Layout da tela ajustado
    frame_conteudo.configure(bg="white")

    # Título "Clientes"
    label_titulo = tk.Label(frame_conteudo, text="CLIENTES", font=("Arial", 20, "bold"), bg="#F7F9FB")
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

    # Subtítulo "Inserir Registro"
    label_subtitulo = tk.Label(frame_conteudo, text="Inserir Registro", font=("Arial", 12, "bold"), bg="#F7F9FB")
    label_subtitulo.grid(row=1, column=0, columnspan=2, pady=10, sticky="w", padx=20)

    # Combobox para selecionar tipo de cliente (Físico ou Jurídico)
    label_tipo_cliente = tk.Label(frame_conteudo, text="Tipo de Cliente", font=("Arial", 10), bg="#F7F9FB")
    label_tipo_cliente.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    
    combo_tipo_cliente = ttk.Combobox(frame_conteudo, values=["Selecione", "Físico", "Jurídico"], font=("Arial", 10), width=27)
    combo_tipo_cliente.current(0)
    combo_tipo_cliente.grid(row=2, column=1, padx=20, pady=5)
    combo_tipo_cliente.bind("<<ComboboxSelected>>", atualizar_campos)

    # Frame para os campos dinâmicos
    frame_form = tk.Frame(frame_conteudo, bg="#F7F9FB")
    frame_form.grid(row=3, column=0, columnspan=2, pady=10)

    # Botão para salvar
    button_salvar = tk.Button(frame_conteudo, text="Salvar", font=("Arial", 12), bg="#A5D6A7", command=salvar_cliente)
    button_salvar.grid(row=4, column=0, columnspan=2, pady=(10, 20))


#------------------------------------------------

#------------------------------------------------


# Função da janela cadastro de produtos
def cadastrar_produto(frame_conteudo):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    frame_conteudo.configure(bg="white")
    root.title("PROTEC Admin: CADASTRO --> PRODUTOS")

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Título "PRODUTOS"
    titulo = tk.Label(frame_conteudo, text="PRODUTOS", font=("Arial", 24, "bold"), bg="white")
    titulo.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="n")

    # Subtítulo "Inserir Registro"
    subtitulo = tk.Label(frame_conteudo, text="Inserir Registro", font=("Arial", 14), bg="white")
    subtitulo.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="n")

    # Função para criar os placeholders
    def create_placeholder(entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.bind("<FocusIn>", lambda event: on_focus_in(event, placeholder_text))
        entry.bind("<FocusOut>", lambda event: on_focus_out(event, placeholder_text))

    def on_focus_in(event, placeholder_text):
        if event.widget.get() == placeholder_text:
            event.widget.delete(0, "end")
            event.widget.config(fg='black')

    def on_focus_out(event, placeholder_text):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder_text)
            event.widget.config(fg='grey')

    # Labels e Entrys com placeholders
    fields = [
        ("Codigo do Produto", "Digite o código", 2, 0),
        ("Nome do Produto", "Nome", 2, 2),
        ("Quantidade", "0", 3, 0),
        ("Categoria do Produto", "Categoria", 3, 2),
        ("Preço do Produto", "R$ 0,00", 4, 0),
        ("Peso do Produto", "0KG", 4, 2),
        ("Descrição", "Descrição", 5, 0)
    ]

    entry_vars = {}
    
    for field, placeholder, linha, coluna in fields:
        label = tk.Label(frame_conteudo, text=field, font=("Arial", 12), bg="white")
        label.grid(row=linha, column=coluna, padx=10, pady=10, sticky="w")
        
        entry_var = tk.StringVar()
        entry = tk.Entry(frame_conteudo, textvariable=entry_var, width=30, fg='grey')
        entry.grid(row=linha, column=coluna+1, padx=10, pady=10)
        
        # Adiciona placeholder
        create_placeholder(entry, placeholder)
        
        entry_vars[field] = entry_var

    # Função para salvar os dados no banco de dados
    def salvar_produto():
        try:
            # Capturar os valores dos campos, removendo o placeholder
            codigo_produto = entry_vars["Codigo do Produto"].get()
            nome_produto = entry_vars["Nome do Produto"].get()
            quantidade = int(entry_vars["Quantidade"].get()) if entry_vars["Quantidade"].get() != "0" else 0
            categoria = entry_vars["Categoria do Produto"].get()
            preco = float(entry_vars["Preço do Produto"].get().replace("R$ ", "").replace(",", ".")) if entry_vars["Preço do Produto"].get() != "R$ 0,00" else 0.0
            peso = entry_vars["Peso do Produto"].get()
            descricao = entry_vars["Descrição"].get()

            # Verificar se os campos obrigatórios foram preenchidos
            if codigo_produto == "Digite o código" or nome_produto == "Nome":
                messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
                return

            # Inserir os dados no banco de dados
            cursor.execute('''
                INSERT INTO Produto (codigo_produto, nome_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque, status)
                VALUES (?, ?, ?, ?, ?, ?, 1)  -- Status padrão "Em Estoque"
            ''', (codigo_produto, nome_produto, categoria, preco, quantidade, descricao))
            
            conn.commit()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar o produto: {e}")

    # Função para criar uma imagem de botão arredondada

    # Função para criar uma imagem arredondada com texto para o botão
    def create_rounded_button_image(width, height, color, corner_radius, text):
        img = Image.new("RGBA", (width, height), (255, 0, 0, 0))  # Fundo transparente
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([(0, 0), (width, height)], corner_radius, fill=color)

        # Adiciona o texto centralizado
        font = ImageFont.truetype("arial.ttf", 14)  # Define a fonte e o tamanho do texto
        # Usa textbbox para obter as dimensões do texto
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((width - text_width) / 2, (height - text_height) / 2)
        draw.text(text_position, text, fill="white", font=font)

        return ImageTk.PhotoImage(img)

    # Dimensões e estilo do botão "SALVAR"
    width, height = 150, 50
    corner_radius = 25
    button_color = "#0066ff"  # Cor padrão do botão
    hover_color = "#0052cc"  # Cor ao passar o mouse
    click_color = "#0041a3"  # Cor ao clicar

    # Criar as imagens de fundo arredondadas com texto para as diferentes cores do botão
    default_image = create_rounded_button_image(width, height, button_color, corner_radius, "SALVAR")
    hover_image = create_rounded_button_image(width, height, hover_color, corner_radius, "SALVAR")
    click_image = create_rounded_button_image(width, height, click_color, corner_radius, "SALVAR")

    # Frame do botão para exibir a imagem de fundo arredondada
    btn_frame = tk.Label(frame_conteudo, image=default_image, bg="white", borderwidth=0)
    btn_frame.image = default_image  # Manter referência da imagem padrão
    btn_frame.grid(row=10, column=2, pady=20, sticky="e")  # Posicionando abaixo do formulário, alinhado à direita

    # Função para alterar a imagem do botão ao passar o mouse e ao clicar
    def on_enter(event):
        btn_frame.config(image=hover_image)

    def on_leave(event):
        btn_frame.config(image=default_image)

    def on_click(event):
        btn_frame.config(image=click_image)
        salvar_produto()  # Chamar a função de salvar

    # Bind dos eventos de hover e clique
    btn_frame.bind("<Enter>", on_enter)
    btn_frame.bind("<Leave>", on_leave)
    btn_frame.bind("<Button-1>", on_click)


#função da janela cadastro de vendas/pedidos
def cadastrar_vendas(frame_conteudo):
    # Limpar o frame anterior
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: CADASTRO --> VENDAS")
    frame_conteudo.configure(bg="white")

    # Conectar ao banco de dados
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Criar a tabela se não existir
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
    conn.commit()

    # Função para adicionar e remover placeholders
    def on_entry_click(event, entry, placeholder):
        """ Remove o texto placeholder quando o usuário clica no campo """
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focusout(event, entry, placeholder):
        """ Adiciona o texto placeholder se o campo estiver vazio """
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    # Título "PEDIDOS"
    label_titulo = tk.Label(frame_conteudo, text="PEDIDOS", font=("Helvetica", 16, "bold"), bg="white")
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Subtítulo "Inserir Registro"
    label_subtitulo = tk.Label(frame_conteudo, text="Inserir Registro", font=("Helvetica", 12, "bold"), bg="white")
    label_subtitulo.grid(row=1, column=0, columnspan=2, pady=(0, 20), padx=10, sticky="w")

    # Campo Código do Pedido
    label_codigo_pedido = tk.Label(frame_conteudo, text="Código do Pedido", font=("Helvetica", 10), bg="white")
    label_codigo_pedido.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_codigo_pedido = tk.Entry(frame_conteudo, width=30, fg='grey')
    entry_codigo_pedido.insert(0, "Digite o Código")
    entry_codigo_pedido.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_codigo_pedido.bind('<FocusIn>', lambda event: on_entry_click(event, entry_codigo_pedido, "Digite o Código"))
    entry_codigo_pedido.bind('<FocusOut>', lambda event: on_focusout(event, entry_codigo_pedido, "Digite o Código"))

    # Campo Data de Admissão
    label_data_admissao = tk.Label(frame_conteudo, text="Data de Admissão", font=("Helvetica", 10), bg="white")
    label_data_admissao.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_data_admissao = tk.Entry(frame_conteudo, width=30, fg='grey')
    entry_data_admissao.insert(0, "AAAA-MM-DD")
    entry_data_admissao.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    entry_data_admissao.bind('<FocusIn>', lambda event: on_entry_click(event, entry_data_admissao, "AAAA-MM-DD"))
    entry_data_admissao.bind('<FocusOut>', lambda event: on_focusout(event, entry_data_admissao, "AAAA-MM-DD"))

    # Campo Forma de Pagamento
    label_forma_pagamento = tk.Label(frame_conteudo, text="Forma de Pagamento", font=("Helvetica", 10), bg="white")
    label_forma_pagamento.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    combo_pagamento = ttk.Combobox(frame_conteudo, values=["Selecione", "Cartão de crédito", "Pix", "Dinheiro"], state="readonly", width=28)
    combo_pagamento.current(0)
    combo_pagamento.grid(row=5, column=0, padx=10, pady=5, sticky="w")

    # Campo Status de Pagamento
    label_status_pagamento = tk.Label(frame_conteudo, text="Status de Pagamento", font=("Helvetica", 10), bg="white")
    label_status_pagamento.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    combo_status_pagamento = ttk.Combobox(frame_conteudo, values=["Em Andamento", "Pago", "Cancelado"], state="readonly", width=28)
    combo_status_pagamento.current(0)
    combo_status_pagamento.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Campo Tipo de Transação com Combobox
    label_tipo_transacao = tk.Label(frame_conteudo, text="Tipo de Transação", font=("Helvetica", 10), bg="white")
    label_tipo_transacao.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    combo_tipo_transacao = ttk.Combobox(frame_conteudo, values=["A Receber", "Saída", "Entrada"], state="readonly", width=28)
    combo_tipo_transacao.current(0)
    combo_tipo_transacao.grid(row=7, column=0, padx=10, pady=5, sticky="w")

    # Campo Status do Pedido
    label_status_pedido = tk.Label(frame_conteudo, text="Status do Pedido", font=("Helvetica", 10), bg="white")
    label_status_pedido.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    entry_status_pedido = tk.Entry(frame_conteudo, width=30, fg='grey')
    entry_status_pedido.insert(0, "Processando...")
    entry_status_pedido.grid(row=9, column=0, padx=10, pady=5, sticky="w")
    entry_status_pedido.bind('<FocusIn>', lambda event: on_entry_click(event, entry_status_pedido, "Processando..."))
    entry_status_pedido.bind('<FocusOut>', lambda event: on_focusout(event, entry_status_pedido, "Processando..."))

    # Campo Quantidade
    label_quantidade = tk.Label(frame_conteudo, text="Quantidade", font=("Helvetica", 10), bg="white")
    label_quantidade.grid(row=8, column=1, padx=10, pady=5, sticky="w")
    entry_quantidade = tk.Entry(frame_conteudo, width=30, fg='grey')
    entry_quantidade.insert(0, "0")
    entry_quantidade.grid(row=9, column=1, padx=10, pady=5, sticky="w")
    entry_quantidade.bind('<FocusIn>', lambda event: on_entry_click(event, entry_quantidade, "0"))
    entry_quantidade.bind('<FocusOut>', lambda event: on_focusout(event, entry_quantidade, "0"))

    # Campo Valor Total
    label_valor_total = tk.Label(frame_conteudo, text="Valor Total", font=("Helvetica", 10), bg="white")
    label_valor_total.grid(row=10, column=0, padx=10, pady=5, sticky="w")
    entry_valor_total = tk.Entry(frame_conteudo, width=30, fg='grey')
    entry_valor_total.insert(0, "R$ 0,00")
    entry_valor_total.grid(row=11, column=0, padx=10, pady=5, sticky="w")
    entry_valor_total.bind('<FocusIn>', lambda event: on_entry_click(event, entry_valor_total, "R$ 0,00"))
    entry_valor_total.bind('<FocusOut>', lambda event: on_focusout(event, entry_valor_total, "R$ 0,00"))

    # Função para salvar os dados no banco
    def salvar_dados():
        codigo_pedido = entry_codigo_pedido.get()
        data_admissao = entry_data_admissao.get()
        forma_pagamento = combo_pagamento.get()
        status_pagamento = combo_status_pagamento.get()
        tipo_transacao = combo_tipo_transacao.get()
        status_pedido = entry_status_pedido.get()
        quantidade = entry_quantidade.get()
        valor_total = entry_valor_total.get()

        # Mapear os tipos de transação para números
        tipo_transacao_valor = {"A Receber": 1, "Saída": 2, "Entrada": 3}.get(tipo_transacao, 0)

        # Inserir os dados no banco
        cursor.execute('''
            INSERT INTO Financas (tipo_transacao, descricao, valor, data_transacao, categoria, id_funcionario)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (tipo_transacao_valor, status_pedido, valor_total, data_admissao, forma_pagamento, 1))  # Ajuste conforme necessário
        conn.commit()

    # Botão de Salvar
    button_salvar = tk.Button(frame_conteudo, text="Salvar", command=salvar_dados, font=("Helvetica", 10, "bold"), bg="#4CAF50", fg="white")
    button_salvar.grid(row=12, column=0, columnspan=2, pady=20)

# Fechar conexão ao banco de dados ao encerrar a aplicação
conn.close()


# Desconectar do banco de dados ao fechar
def fechar_conexao():
    conn.close()

# Função principal da janela de cadastros
def criar_janela_cadastros(frame_conteudo):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: CADASTRO")

    # Definir paleta de cores e fontes
    cor_fundo = "#F7F9FB"
    cor_titulo = "#2E3B55"
    cor_subtitulo = "#4C5A6E"
    cor_botao = "#4A90E2"
    cor_botao_selecao = "#D9E4EC"

    fonte_titulo = ("Arial", 24, "bold")
    fonte_subtitulo = ("Arial", 14)
    fonte_botoes = ("Arial", 12, "bold")
    fonte_versao = ("Arial", 8)

    frame_conteudo.config(bg=cor_fundo)

    # Carregar as imagens para as seleções
    circle_img = Image.open("circle.png").resize((20, 20))
    tick_img = Image.open("GreenTickCheck.png").resize((20, 20))
    circle_img = ImageTk.PhotoImage(circle_img)
    tick_img = ImageTk.PhotoImage(tick_img)

    # Título "Cadastros"
    titulo = tk.Label(frame_conteudo, text="CADASTROS", font=fonte_titulo, fg=cor_titulo, bg=cor_fundo)
    titulo.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=3, sticky="n")

    # Linha abaixo do título "Cadastros"
    linha1 = ttk.Separator(frame_conteudo, orient="horizontal")
    linha1.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

    # Subtítulo "Escolha uma opção"
    subtitulo = tk.Label(frame_conteudo, text="Escolha uma opção", font=fonte_subtitulo, fg=cor_subtitulo, bg=cor_fundo)
    subtitulo.grid(row=2, column=0, padx=20, pady=10, columnspan=3, sticky="n")

    # Linha abaixo do subtítulo "Escolha uma opção"
    linha2 = ttk.Separator(frame_conteudo, orient="horizontal")
    linha2.grid(row=3, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

    # Definir botões de cadastro com as opções
    opcoes = [
        ("FUNCIONÁRIOS", cadastrar_funcionario), 
        ("CLIENTES", cadastrar_cliente), 
        ("VENDAS", cadastrar_vendas), 
        ("FORNECEDORES", None),
        ("PRODUTOS", cadastrar_produto), 
        ("ESTOQUE", None)
    ]

    variavel_selecao = tk.StringVar(value="")  # Variável para capturar a seleção
    imagens_selecionadas = {}  # Dicionário para armazenar as imagens selecionadas

    def atualizar_selecao(nome_opcao, img_label):
        # Atualizar visualmente a seleção
        variavel_selecao.set(nome_opcao)
        for opcao, img in imagens_selecionadas.items():
            if opcao == nome_opcao:
                img.config(image=tick_img)
            else:
                img.config(image=circle_img)

    # Colocar os botões e as imagens com mais espaçamento
    for i, (opcao, funcao) in enumerate(opcoes):
        linha = 4 + i // 2  # Organizar duas colunas
        coluna = (i % 2) * 2  # Para alternar as colunas 0 e 2

        # Botão de ação
        btn = tk.Button(frame_conteudo, text=opcao, font=fonte_botoes, width=15, height=2, 
                        bg=cor_botao_selecao, fg="black", relief="solid", bd=0, cursor="hand2")
        btn.grid(row=linha, column=coluna, padx=50, pady=20, sticky="e")

        # Imagem (substituindo o Radiobutton)
        img_label = tk.Label(frame_conteudo, image=circle_img, bg=cor_fundo, cursor="hand2")
        img_label.grid(row=linha, column=coluna+1, padx=10, pady=20, sticky="w")

        # Armazenar a referência para controlar depois
        imagens_selecionadas[opcao] = img_label

        # Associa o clique para atualizar a seleção
        img_label.bind("<Button-1>", lambda event, opcao=opcao, img_label=img_label: atualizar_selecao(opcao, img_label))

    # Função para lidar com o botão "Cadastrar"
    def cadastrar():
        opcao_escolhida = variavel_selecao.get()
        for texto, funcao in opcoes:
            if opcao_escolhida == texto and funcao:
                funcao(frame_conteudo)  # Chama a função correspondente
                break

    # Botão "Cadastrar"
    btn_cadastrar = tk.Button(frame_conteudo, text="CADASTRAR", font=fonte_botoes, width=15, height=2, 
                              bg=cor_botao, fg="white", relief="flat", cursor="hand2", command=cadastrar)
    btn_cadastrar.grid(row=8, column=2, padx=50, pady=30, sticky="e")
#-------------------------------------------------
#FUNÇÃO DE PRODUTOS
# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    
    # Criar tabela com a nova coluna Status, se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produto(
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_produto TEXT NOT NULL,
            nome_produto TEXT NOT NULL,
            tipo_produto TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            endereco_estoque TEXT,
            status INTEGER NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

# Função para buscar produtos no banco de dados com base no filtro de status
def buscar_produto(status=None):
    termo_busca = buscar_entry.get()

    # Limpar a tabela antes de preencher
    for row in tabela.get_children():
        tabela.delete(row)

    # Conectar ao banco de dados para realizar a busca
    conn, cursor = conectar_banco()

    # Se houver termo de busca, filtra os produtos pelo nome
    if termo_busca:
        query = "SELECT nome_produto, codigo_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque FROM Produto WHERE nome_produto LIKE ?"
        params = ('%' + termo_busca + '%',)
        if status:  # Adiciona o filtro de status se necessário
            query += " AND status = ?"
            params += (status,)
        cursor.execute(query, params)
    else:
        # Filtros de status
        if status:
            cursor.execute("SELECT nome_produto, codigo_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque FROM Produto WHERE status = ?", (status,))
        else:
            # Caso status seja None, traz todos os produtos
            cursor.execute("SELECT nome_produto, codigo_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque FROM Produto")

    produtos = cursor.fetchall()

    # Verificar se a consulta retornou dados
    if not produtos:
        print("Nenhum produto encontrado.")
    
    # Preencher a tabela com os resultados da busca
    for row in produtos:
        tabela.insert('', 'end', values=row)

    conn.close()

# Função para exibir todos os produtos
def exibir_todos():
    buscar_produto()  # Chamar sem filtro para mostrar todos

# Função para exibir produtos em falta
def exibir_em_falta():
    buscar_produto(status=2)  # Filtro para "em falta"

# Função para exibir produtos em estoque
def exibir_em_estoque():
    buscar_produto(status=1)  # Filtro para "em estoque"

def abrir_janela_editar(produto_selecionado):
    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Produto")
    janela_editar.geometry("400x400")
    janela_editar.configure(bg="#EDE7F6")  # Cor de fundo suave

    estilo = ttk.Style()
    estilo.configure("TLabel", font=("Arial", 12), background="#EDE7F6")
    estilo.configure("TButton", font=("Arial", 10), padding=6)
    estilo.configure("TEntry", font=("Arial", 12), padding=5)

    # Labels e entradas para editar os dados do produto
    ttk.Label(janela_editar, text="Nome:", background="#EDE7F6").grid(row=0, column=0, padx=10, pady=5, sticky="W")
    nome_entry = ttk.Entry(janela_editar, width=30)  # Aumentar largura
    nome_entry.grid(row=0, column=1, padx=10, pady=5)
    nome_entry.insert(0, produto_selecionado[0])

    ttk.Label(janela_editar, text="Código:", background="#EDE7F6").grid(row=1, column=0, padx=10, pady=5, sticky="W")
    codigo_entry = ttk.Entry(janela_editar, width=30)  # Aumentar largura
    codigo_entry.grid(row=1, column=1, padx=10, pady=5)
    codigo_entry.insert(0, produto_selecionado[1])

    ttk.Label(janela_editar, text="Categoria:", background="#EDE7F6").grid(row=2, column=0, padx=10, pady=5, sticky="W")
    categoria_entry = ttk.Entry(janela_editar, width=30)  # Aumentar largura
    categoria_entry.grid(row=2, column=1, padx=10, pady=5)
    categoria_entry.insert(0, produto_selecionado[2])

    ttk.Label(janela_editar, text="Valor:", background="#EDE7F6").grid(row=3, column=0, padx=10, pady=5, sticky="W")
    valor_entry = ttk.Entry(janela_editar, width=30)  # Aumentar largura
    valor_entry.grid(row=3, column=1, padx=10, pady=5)
    valor_entry.insert(0, produto_selecionado[3])

    ttk.Label(janela_editar, text="Quantidade:", background="#EDE7F6").grid(row=4, column=0, padx=10, pady=5, sticky="W")
    quantidade_entry = ttk.Entry(janela_editar, width=30)  # Aumentar largura
    quantidade_entry.grid(row=4, column=1, padx=10, pady=5)
    quantidade_entry.insert(0, produto_selecionado[4])

    ttk.Label(janela_editar, text="Endereço:", background="#EDE7F6").grid(row=5, column=0, padx=10, pady=5, sticky="W")
    endereco_entry = ttk.Entry(janela_editar, width=30)  # Aumentar largura
    endereco_entry.grid(row=5, column=1, padx=10, pady=5)
    endereco_entry.insert(0, produto_selecionado[5])

    def atualizar_produto():
        # Atualizar no banco de dados
        try:
            conn = sqlite3.connect('seu_banco_de_dados.db')
            cursor = conn.cursor()

            # Recuperando os valores dos campos
            nome = nome_entry.get()
            codigo = codigo_entry.get()
            categoria = categoria_entry.get()
            valor = valor_entry.get()
            quantidade = quantidade_entry.get()
            endereco = endereco_entry.get()

            cursor.execute('''
                UPDATE Produto SET nome_produto=?, codigo_produto=?, tipo_produto=?, preco=?, quantidade_estoque=?, endereco_estoque=?
                WHERE codigo_produto=?
            ''', (nome, codigo, categoria, float(valor), int(quantidade), endereco, produto_selecionado[1]))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            janela_editar.destroy()
            exibir_todos()  # Atualiza a tabela principal
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")

    def deletar_produto():
        # Deletar produto no banco de dados
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este produto?")
        if resposta:
            try:
                conn = sqlite3.connect('seu_banco_de_dados.db')
                cursor = conn.cursor()

                cursor.execute('DELETE FROM Produto WHERE codigo_produto=?', (produto_selecionado[1],))

                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
                janela_editar.destroy()
                exibir_todos()  # Atualiza a tabela principal
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar produto: {e}")

    # Botões de ação
    btn_atualizar = ttk.Button(janela_editar, text="Atualizar", command=atualizar_produto)
    btn_atualizar.grid(row=6, column=0, padx=10, pady=20, sticky="E")

    btn_deletar = ttk.Button(janela_editar, text="Deletar", command=deletar_produto)
    btn_deletar.grid(row=6, column=1, padx=10, pady=20, sticky="W")

    # Estilização das cores dos botões
    btn_atualizar.configure(style="TButton")
    btn_deletar.configure(style="TButton")

    # Cores dos botões
    btn_atualizar['style'] = 'TButton'
    btn_deletar['style'] = 'TButton'
    estilo.map("TButton",
               background=[("active", "#6A5ACD"), ("!active", "#836FFF")],  # Cor ativa e inativa
               foreground=[("active", "white"), ("!active", "black")])  # Cor do texto

def editar_produto():
    try:
        produto_selecionado = tabela.item(tabela.selection())['values']
        if produto_selecionado:
            abrir_janela_editar(produto_selecionado)
        else:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione um produto para editar!")

def exibir_todos():
    # Limpa a tabela
    for item in tabela.get_children():
        tabela.delete(item)

    # Conectar ao banco de dados e buscar os produtos
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nome_produto, codigo_produto, tipo_produto, preco, quantidade_estoque, endereco_estoque FROM Produto')
    produtos = cursor.fetchall()

    # Inserir os produtos na tabela
    for produto in produtos:
        tabela.insert('', tk.END, values=produto)

    conn.close()

def Mostrar_Produtos(parent_frame):
    # Limpar o conteúdo anterior do frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: PRODUTOS")

    # Frame para área de conteúdo principal
    content_frame = tk.Frame(parent_frame)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Botões de filtro
    filtro_frame = tk.Frame(content_frame)
    filtro_frame.pack(fill=tk.X, pady=10)

    # Botão para mostrar todos os produtos
    btn_todos = tk.Button(filtro_frame, text="TODOS", bg="#D9E4E8", font=("Arial", 12), command=exibir_todos)
    btn_todos.pack(side=tk.LEFT, padx=10)

    # Botão para mostrar produtos em falta
    btn_em_falta = tk.Button(filtro_frame, text="EM FALTA", bg="#CC444B", fg="white", font=("Arial", 12), command=exibir_em_falta)
    btn_em_falta.pack(side=tk.LEFT, padx=10)

    # Botão para mostrar produtos em estoque
    btn_estoque = tk.Button(filtro_frame, text="ESTOQUE", bg="#FFC857", font=("Arial", 12), command=exibir_em_estoque)
    btn_estoque.pack(side=tk.LEFT, padx=10)

    global buscar_entry
    buscar_entry = tk.Entry(filtro_frame, width=20, font=("Arial", 12))
    buscar_entry.pack(side=tk.RIGHT, padx=5)

    # Botão para acionar a busca
    buscar_button = tk.Button(filtro_frame, text="Buscar", command=buscar_produto, font=("Arial", 12))
    buscar_button.pack(side=tk.RIGHT, padx=5)

    # Frame para tabela e barra de rolagem
    tabela_frame = tk.Frame(content_frame)
    tabela_frame.pack(fill=tk.BOTH, expand=True)

    # Adicionar barra de rolagem
    scrollbar = tk.Scrollbar(tabela_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Tabela de produtos
    columns = ("Nome", "Codigo", "Categoria", "Valor", "Quantidade", "Endereço")
    global tabela
    tabela = ttk.Treeview(tabela_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

    # Definir cabeçalhos da tabela
    for col in columns:
        tabela.heading(col, text=col)
        tabela.column(col, width=100, anchor="center")

    tabela.pack(fill=tk.BOTH, expand=True)

    # Configurar barra de rolagem
    scrollbar.config(command=tabela.yview)

    # Carregar todos os produtos ao iniciar a exibição
    exibir_todos()

    # Botão Editar
    btn_editar = tk.Button(content_frame, text="Editar Produto", bg="#58C4DD", font=("Arial", 12), command=editar_produto)
    btn_editar.pack(side=tk.LEFT, padx=10, pady=10)
    
#-------------------------------------------------
#FUNÇÃO DE FINANÇAS E CALULAR SALDO, ENTRADAS E SAÍDAS!!
def Mostrar_financas(frame_conteudo):
    # Limpar conteúdo existente no frame_conteudo
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: FINANÇAS")

    # Conexão com o banco de dados
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Criar a tabela Financas caso não exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Financas (
            id_financa INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_transacao TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data_transacao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            id_funcionario INTEGER,
            FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
        )
    ''')
    conn.commit()

    # Função para carregar dados na tabela com base no filtro
    def carregar_dados(filtro):
        # Conexão com o banco de dados
        conn = sqlite3.connect('seu_banco_de_dados.db')
        cursor = conn.cursor()

        # Limpar a tabela existente
        for item in tabela.get_children():
            tabela.delete(item)

        # Calcular o intervalo de datas com base no filtro
        hoje = datetime.now()
        if filtro == "Este Mês":
            data_inicial = hoje.replace(day=1)
        elif filtro == "Últimos 3 Meses":
            data_inicial = hoje - timedelta(days=90)
        elif filtro == "Este Ano":
            data_inicial = hoje.replace(month=1, day=1)
        elif filtro == "Ano Passado":
            data_inicial = hoje.replace(year=hoje.year - 1, month=1, day=1)
            data_final = hoje.replace(year=hoje.year - 1, month=12, day=31)
        else:  # Sem filtro
            data_inicial = None

        # Carregar dados com o filtro de data
        if data_inicial:
            if filtro == "Ano Passado":
                cursor.execute("""
                    SELECT id_financa, descricao, valor, data_transacao, categoria 
                    FROM Financas 
                    WHERE data_transacao BETWEEN ? AND ?""", 
                    (data_inicial.strftime("%Y-%m-%d"), data_final.strftime("%Y-%m-%d")))
            else:
                cursor.execute("""
                    SELECT id_financa, descricao, valor, data_transacao, categoria 
                    FROM Financas 
                    WHERE data_transacao >= ?""", 
                    (data_inicial.strftime("%Y-%m-%d"),))
        else:
            cursor.execute("SELECT id_financa, descricao, valor, data_transacao, categoria FROM Financas")
        
        # Buscar e inserir registros
        registros = cursor.fetchall()
        for registro in registros:
            tabela.insert("", "end", values=registro)

    # Frame principal
    frame_principal = tk.Frame(frame_conteudo, bg="white", bd=2, relief="solid")
    frame_principal.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Título
    label_titulo = tk.Label(frame_principal, text="FINANCEIRO", font=("Helvetica", 16, "bold"), bg="white")
    label_titulo.grid(row=0, column=0, columnspan=4, pady=10)
    
    # Calcular valores para Entradas, Saídas e Saldo
    cursor.execute("SELECT tipo_transacao, SUM(valor) FROM Financas GROUP BY tipo_transacao")
    resultados = cursor.fetchall()
    
    entradas_total = sum(valor for tipo, valor in resultados if tipo == '1')
    saidas_total = sum(valor for tipo, valor in resultados if tipo == '2')
    saldo_total = sum(valor for tipo, valor in resultados if tipo == '3')

    # Resumo das finanças
    frame_resumo = tk.Frame(frame_principal, bg="white")
    frame_resumo.grid(row=1, column=0, columnspan=4, sticky="ew", padx=20, pady=10)

    entradas_label = tk.Label(frame_resumo, text=f"CRÉDITOS\nR$ {entradas_total:,.2f}", bg="lime", font=("Helvetica", 12, "bold"), width=15, height=2)
    entradas_label.grid(row=0, column=0, padx=5, pady=5)

    saidas_label = tk.Label(frame_resumo, text=f"DÉBITOS\nR$ {saidas_total:,.2f}", bg="red", font=("Helvetica", 12, "bold"), width=15, height=2)
    saidas_label.grid(row=0, column=1, padx=5, pady=5)

    saldo_label = tk.Label(frame_resumo, text=f"SALDO\nR$ {saldo_total:,.2f}", bg="yellow", font=("Helvetica", 12, "bold"), width=15, height=2)
    saldo_label.grid(row=0, column=2, padx=5, pady=5)

    # Menu suspenso para filtro de data
    filtro_opcoes = ["Sem Filtro","Sem Filtro", "Este Mês", "Últimos 3 Meses", "Este Ano", "Ano Passado"]
    filtro_selecionado = tk.StringVar(value="Sem Filtro")
    
    filtro_menu = ttk.OptionMenu(frame_resumo, filtro_selecionado, *filtro_opcoes, command=carregar_dados)
    filtro_menu.grid(row=0, column=3, padx=10)

    # Frame da tabela com barra de rolagem
    frame_tabela = tk.Frame(frame_principal)
    frame_tabela.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=20, pady=10)

    # Barra de rolagem
    scrollbar_y = tk.Scrollbar(frame_tabela, orient="vertical")
    scrollbar_x = tk.Scrollbar(frame_tabela, orient="horizontal")

    # Tabela
    tabela = ttk.Treeview(frame_tabela, columns=("ID", "Descricao", "Valor", "Data de Transação", "Categoria"),
                          yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, show="headings")
    tabela.heading("ID", text="ID")
    tabela.heading("Descricao", text="Descrição")
    tabela.heading("Valor", text="Valor")
    tabela.heading("Data de Transação", text="Data de Transação")
    tabela.heading("Categoria", text="Categoria")

    tabela.column("ID", width=25)
    tabela.column("Descricao", width=350)
    tabela.column("Valor", width=100)
    tabela.column("Data de Transação", width=120)
    tabela.column("Categoria", width=120)

    tabela.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.config(command=tabela.yview)
    scrollbar_x.config(command=tabela.xview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # Carregar dados inicialmente sem filtro
    carregar_dados("Sem Filtro")
    
    #Atualizar valores---
    def atualizar_resumo():
        # Conectar ao banco de dados
        conn = sqlite3.connect("seu_banco_de_dados.db")
        cursor = conn.cursor()

        # Recalcular valores para Entradas, Saídas e Saldo
        cursor.execute("SELECT tipo_transacao, SUM(valor) FROM Financas GROUP BY tipo_transacao")
        resultados = cursor.fetchall()
        
        entradas_total = sum(valor for tipo, valor in resultados if tipo == '1')
        saidas_total = sum(valor for tipo, valor in resultados if tipo == '2')
        #saldo_total = sum(valor for tipo, valor in resultados if tipo == '3')
        saldo_total = entradas_total - saidas_total  # saldo_total ajustado para o cálculo correto

        # Atualizar os rótulos
        entradas_label.config(text=f"CRÉDITOS\nR$ {entradas_total:,.2f}")
        saidas_label.config(text=f"DÉBITOS\nR$ {saidas_total:,.2f}")
        saldo_label.config(text=f"SALDO\nR$ {saldo_total:,.2f}")

        # Fechar a conexão
        conn.close()

        # Configurar para repetir a cada 5 segundos (5000 milissegundos)
        frame_resumo.after(5000, atualizar_resumo)
    #--------------------
    atualizar_resumo()

    # Botão de editar
    def editar_selecionado():
        try:
            item_selecionado = tabela.selection()[0]
            valores = tabela.item(item_selecionado, "values")

            # Criar uma nova janela para edição
            janela_editar = tk.Toplevel()
            janela_editar.title("Editar Transação")
            janela_editar.configure(bg="#2C2F33")  # Cor de fundo preto

            # Abrir nova conexão para a edição
            conn_editar = sqlite3.connect('seu_banco_de_dados.db')
            cursor_editar = conn_editar.cursor()

            # Campos para edição
            campos = ["Descrição", "Valor", "Data de Transação", "Categoria"]
            entradas = {}
            for i, campo in enumerate(campos):
                label = tk.Label(janela_editar, text=campo, bg="#2C2F33", fg="white", font=("Helvetica", 10, "bold"))
                label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                entrada = tk.Entry(janela_editar, bg="#99AAB5", fg="black", font=("Helvetica", 10))
                entrada.insert(0, valores[i+1])  # Ignora o ID (posição 0)
                entrada.grid(row=i, column=1, padx=10, pady=5)
                entradas[campo] = entrada

            def salvar_edicao():
                novos_valores = {campo: entrada.get() for campo, entrada in entradas.items()}
                cursor_editar.execute('''UPDATE Financas SET 
                                            descricao = ?, valor = ?, 
                                            data_transacao = ?, categoria = ? 
                                          WHERE id_financa = ?''',
                                      (novos_valores["Descrição"], float(novos_valores["Valor"]), 
                                       novos_valores["Data de Transação"], novos_valores["Categoria"], valores[0]))
                conn_editar.commit()
                tabela.item(item_selecionado, values=(valores[0], *novos_valores.values()))
                messagebox.showinfo("Sucesso", "Transação atualizada com sucesso!")
                atualizar_resumo()
                

            def deletar_transacao():
                resposta = messagebox.askyesno("Confirmação", "Deseja realmente excluir esta transação?")
                if resposta:
                    cursor_editar.execute("DELETE FROM Financas WHERE id_financa = ?", (valores[0],))
                    conn_editar.commit()
                    tabela.delete(item_selecionado)
                    janela_editar.destroy()
                    messagebox.showinfo("Sucesso", "Transação excluída com sucesso!")
                    atualizar_resumo()

            # Botões Salvar e Excluir estilizados
            btn_salvar = ttk.Button(janela_editar, text="Salvar", command=salvar_edicao, style="TButton")
            btn_salvar.grid(row=len(campos), column=0, padx=10, pady=20)

            btn_excluir = ttk.Button(janela_editar, text="Excluir", command=deletar_transacao, style="TButton")
            btn_excluir.grid(row=len(campos), column=1, padx=10, pady=20)

            # Fechar conexão ao fechar a janela
            def fechar_janela_editar():
                conn_editar.close()
                janela_editar.destroy()

            janela_editar.protocol("WM_DELETE_WINDOW", fechar_janela_editar)

        except IndexError:
            messagebox.showwarning("Seleção necessária", "Selecione uma transação para editar.")

    btn_editar = ttk.Button(frame_principal, text="Editar", command=editar_selecionado)
    btn_editar.grid(row=3, column=0, columnspan=4, pady=10)

    # Fechar conexão com o banco de dados ao terminar
    conn.close()

#-------------------------------------------------
#FUNÇÃO SERVIÇOS
def criar_janela_servicos(frame_conteudo):
    # Limpar o frame antes de adicionar novos widgets
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: SERVIÇOS")

    # Conexão com o banco de dados
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Foto de perfil e nome do administrador
    frame_admin = tk.Frame(frame_conteudo, bg="white")
    frame_admin.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Carregar imagem de perfil (Ajuste o caminho para o ícone correto)
    try:
        imagem_perfil = carregar_imagem('perfil.png', (50, 50))  # Redimensiona para 50x50
        label_imagem = tk.Label(frame_admin, image=imagem_perfil, bg="white")
        label_imagem.image = imagem_perfil  # Manter referência para evitar que a imagem seja "apagada"
        label_imagem.pack(side="left", padx=10)
    except Exception as e:
        print(f"Erro ao carregar imagem de perfil: {e}")

    # Label com o nome "Administrador"
    label_admin = tk.Label(frame_admin, text="Administrador", font=("Helvetica", 14), bg="white")
    label_admin.pack(side="left", padx=10)

    # Criar a linha preta logo abaixo do administrador
    linha_preta = tk.Frame(frame_conteudo, bg="black", height=2, width=600)  # Ajuste a largura conforme necessário
    linha_preta.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    # Botão "+ SERVIÇO" (azul)
    btn_servico = tk.Button(frame_conteudo, text="+ SERVIÇO", font=("Arial", 12, "bold"), bg="#0066ff", fg="white", width=15, height=2)
    btn_servico.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # Botão "RELATÓRIO" (verde)
    btn_relatorio = tk.Button(frame_conteudo, text="RELATORIO", font=("Arial", 12, "bold"), bg="#00cc66", fg="white", width=15, height=2)
    btn_relatorio.grid(row=0, column=3, padx=10, pady=10, sticky="e")

    # Mostrar quantos registros
    lbl_mostrar = tk.Label(frame_conteudo, text="Mostrar", font=("Arial", 12))
    lbl_mostrar.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    combo_mostrar = ttk.Combobox(frame_conteudo, values=[5, 10, 15], width=5)
    combo_mostrar.set(5)
    combo_mostrar.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Campo de busca
    lbl_buscar = tk.Label(frame_conteudo, text="Buscar:", font=("Arial", 12))
    lbl_buscar.grid(row=2, column=2, padx=10, pady=10, sticky="e")
    entry_buscar = tk.Entry(frame_conteudo, width=20)
    entry_buscar.grid(row=2, column=3, padx=10, pady=10, sticky="e")

    # Definir a tabela
    columns = ("Nome", "Valor", "Data", "Comissao", "Acoes")

    tree = ttk.Treeview(frame_conteudo, columns=columns, show="headings", height=5)
    tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    # Definir os cabeçalhos
    tree.heading("Nome", text="Nome")
    tree.heading("Valor", text="Valor")
    tree.heading("Data", text="Data")
    tree.heading("Comissao", text="Comissão %")
    tree.heading("Acoes", text="Ações")

    # Ajustar largura das colunas
    tree.column("Nome", width=200)
    tree.column("Valor", width=100)
    tree.column("Data", width=100)
    tree.column("Comissao", width=100)
    tree.column("Acoes", width=100)

    # Função para carregar os dados da tabela
    def carregar_dados():
        # Limpar a tabela antes de inserir novos dados
        for item in tree.get_children():
            tree.delete(item)

        # Selecionar os dados da tabela 'Pedido'
        cursor.execute('''SELECT id_pedido, forma_pagamento, valor_total, data_pedido, status_envio_produto 
                          FROM Pedido LIMIT 5''')
        rows = cursor.fetchall()

        for row in rows:
            # Inserir dados na Treeview
            tree.insert('', 'end', values=(row[1], f"R${row[2]:.2f}", row[3], "10%", "Editar | Excluir"))

    # Chamar a função para carregar os dados
    carregar_dados()

    # Informações de rodapé com a paginação
    lbl_rodape = tk.Label(frame_conteudo, text="Listando 05/100 registros", font=("Arial", 10))
    lbl_rodape.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # Botões de navegação da página
    btn_anterior = tk.Button(frame_conteudo, text="Anterior", font=("Arial", 10), width=10)
    btn_anterior.grid(row=4, column=2, padx=10, pady=10, sticky="e")

    lbl_pagina = tk.Label(frame_conteudo, text="1", font=("Arial", 10))
    lbl_pagina.grid(row=4, column=3, padx=5, pady=10, sticky="e")

    btn_proximo = tk.Button(frame_conteudo, text="Próximo", font=("Arial", 10), width=10)
    btn_proximo.grid(row=4, column=3, padx=40, pady=10, sticky="e")

    # Fechar conexão com o banco de dados ao finalizar
    conn.close()
#-------------------------------------------------------------------------------------------------------

# Função para redimensionar e carregar imagens
def carregar_imagem(caminho, tamanho):
    imagem = Image.open(caminho)
    imagem = imagem.resize(tamanho, Image.LANCZOS)
    return ImageTk.PhotoImage(imagem)

#TESTE--------------------------------------------------------
def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Função para criar a interface principal
def create_main_interface():
    # Limpar o frame principal antes de adicionar novos widgets
    for widget in frame_menu.winfo_children():
        widget.destroy()
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    root.title("PROTEC Admin: HOME --> CONFIGURAÇÕES")

    # Configuração para que o main_frame se expanda com a janela
    frame_menu.grid_rowconfigure(0, weight=1)
    frame_menu.grid_columnconfigure(1, weight=1)

    # Definir os textos dos botões antes de configurar o sidebar
    button_texts = [
        "Verificação de Atualizações",
        "Agendamento",
        "Status da Atualização",
        "Opções de atualização",
        "Backup de dados",
        "Atualizações anteriores",
        "Erro ou alertas",
        "VOLTAR HOME"
    ]

    # Adicionar botões de opções
    for texto in button_texts:
        button = tk.Button(frame_conteudo, text=texto, command=lambda t=texto: acao_botao(t))
        button.pack(pady=5)

    def acao_botao(texto):
        if texto == "VOLTAR HOME":
            criar_janela_home(frame_conteudo)
        else:
            print(f"Ação para o botão: {texto}")

    # Lado esquerdo com botões
    sidebar = tk.Frame(frame_menu, bg="white")
    sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 20))
    sidebar.grid_rowconfigure(len(button_texts), weight=1)  # Para expandir a coluna de botões

    # Adicionar os botões laterais
    for idx, text in enumerate(button_texts):
        btn = ttk.Button(sidebar, text=text, width=25)
        btn.grid(row=idx, column=0, padx=5, pady=5, sticky="ew")  # Expansão horizontal

    # Ícone de download, ajustando o tamanho da imagem para expandir conforme a tela
    download_icon = load_image("Down_Icon.png", (60, 60))
    download_label = tk.Label(sidebar, image=download_icon, bg="white")
    download_label.grid(row=len(button_texts), column=0, pady=10)

    # Área principal com notas e informações
    content_frame = tk.Frame(frame_menu, bg="#3D4D5B")
    content_frame.grid(row=0, column=1, sticky="nsew")

    # Configuração para que content_frame se expanda
    content_frame.grid_rowconfigure(1, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # Texto de boas-vindas
    welcome_label = tk.Label(content_frame, text="Bem-vindo ao System Update da Protect!", font=("Arial", 14, "bold"), bg="#3D4D5B", fg="white")
    welcome_label.pack(pady=10)

    # Texto de descrição
    description_label = tk.Label(content_frame, text="Estamos constantemente trabalhando para melhorar nossos serviços e garantir\nque você tenha a melhor experiência possível.", font=("Arial", 12), bg="#3D4D5B", fg="white")
    description_label.pack(pady=5)

    # Notas de atualização e versão com imagens, configurando para expandir
    notes_frame = tk.Frame(content_frame, bg="#3D4D5B")
    notes_frame.pack(pady=20, fill="both", expand=True)

    # Carregar imagens Notas_(1) e Notas_(2) e ajustar o tamanho para expandir proporcionalmente
    info_image = load_image("Notas_(1).png", (330, 220))
    version_image = load_image("Notas_(2).png", (330, 220))

    # Label para Informação sobre a atualização
    info_label = tk.Label(notes_frame, image=info_image, bg="#3D4D5B")
    info_label.grid(row=0, column=0, padx=10, sticky="nsew")

    # Label para Notas da versão
    version_label = tk.Label(notes_frame, image=version_image, bg="#3D4D5B")
    version_label.grid(row=0, column=1, padx=10, sticky="nsew")

    # Expansão das imagens para preencher o espaço disponível
    notes_frame.grid_rowconfigure(0, weight=1)
    notes_frame.grid_columnconfigure(0, weight=1)
    notes_frame.grid_columnconfigure(1, weight=1)

    # Ícone de logout
    logout_icon = load_image("logout.png", (50, 50))
    logout_label = tk.Label(content_frame, image=logout_icon, bg="#3D4D5B")
    logout_label.pack(pady=10)
#-------------------------------------------------------------

# Inicializando janela principal
root = tk.Tk()
root.title("PROTEC Admin: Sistema Intuitivo de Gerenciamento")
root.geometry("960x600")  # Define o tamanho da janela

# Frame esquerdo para o menu de navegação
frame_menu = tk.Frame(root, bg="#2E3B59", width=200, height=600)
frame_menu.pack(side="left", fill="y")

# Frame principal para o conteúdo
frame_conteudo = tk.Frame(root, bg="white")
frame_conteudo.pack(side="right", expand=True, fill="both")

# Carregar imagens (atualize os caminhos conforme necessário)
icone_home = carregar_imagem('home.png', (30, 30))
icone_clientes = carregar_imagem('clientes_funcionarios.png', (30, 30))  # Mesma imagem para clientes e funcionários
icone_cadastros = carregar_imagem('cadastros.png', (30, 30))
icone_produto = carregar_imagem('produtos.png', (30, 30))
icone_financeiro = carregar_imagem('financeiro.png', (30, 30))
icone_servicos = carregar_imagem('servicos.png', (30, 30))
icone_exit = carregar_imagem('exit.png', (30, 30))
icone_funcionarios = carregar_imagem('funcionarios.png', (25, 30))

# Frame para o título "PROTEC" dividido em "PRO" e "TEC"
frame_titulo = tk.Frame(frame_menu, bg="#2E3B59")
frame_titulo.pack(pady=10)

# "PRO" (normal) e "TEC" (negrito)
titulo_pro = tk.Label(frame_titulo, text="PRO", fg="white", bg="#2E3B59", font=("Helvetica", 20, "normal"))
titulo_pro.pack(side="left")

titulo_tec = tk.Label(frame_titulo, text="TEC", fg="white", bg="#2E3B59", font=("Helvetica", 20, "bold"))
titulo_tec.pack(side="left")

# Label para "MENU INICIAL" com fundo cinza claro
menu_inicial = tk.Label(frame_menu, text="MENU INICIAL", fg="white", bg="#1F2A44", font=("Helvetica", 12))
menu_inicial.pack(fill="x")

# Criar botões com ícones no menu
btn_home = tk.Button(frame_menu, image=icone_home, text=" Home", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=lambda: criar_janela_home(frame_conteudo))
btn_home.pack(fill="x", pady=10)

# botão Clientes
btn_clientes = tk.Button(frame_menu, image=icone_clientes, text=" Clientes", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=lambda: exibir_clientes('fisico'))
btn_clientes.pack(fill="x", pady=10)

# botão Funcionários
btn_funcionarios = tk.Button(frame_menu, image=icone_funcionarios, text=" Funcionários", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=exibir_funcionarios)
btn_funcionarios.pack(fill="x", pady=10)

# botão Cadastros
btn_cadastros = tk.Button(frame_menu, image=icone_cadastros, text=" Cadastros", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=lambda: criar_janela_cadastros(frame_conteudo))
btn_cadastros.pack(fill="x", pady=10)

# botão Produto
btn_produto = tk.Button(frame_menu, image=icone_produto, text=" Produto", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=lambda: Mostrar_Produtos(frame_conteudo))
btn_produto.pack(fill="x", pady=10)

# botão Financeiro
btn_financeiro = tk.Button(frame_menu, image=icone_financeiro, text=" Financeiro", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0,command=lambda: Mostrar_financas(frame_conteudo))
btn_financeiro.pack(fill="x", pady=10)

# botão Serviços
btn_servicos = tk.Button(frame_menu, image=icone_servicos, text=" Serviços", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=lambda: criar_janela_servicos(frame_conteudo))
btn_servicos.pack(fill="x", pady=10)

# Rodapé no menu
rodape = tk.Label(frame_menu, text="VERSÃO 1.0", fg="white", bg="#2E3B59", font=("Helvetica", 10))
rodape.pack(side="bottom", pady=10)

# Foto de perfil e nome do administrador
frame_admin = tk.Frame(frame_conteudo, bg="white")
frame_admin.pack(anchor="nw", padx=10, pady=10)

# Carregar imagem de perfil (Ajustar caminho da imagem)
imagem_perfil = carregar_imagem('perfil.png', (50, 50))  # Redimensiona para 50x50

label_imagem = tk.Label(frame_admin, image=imagem_perfil, bg="white")
label_imagem.pack(side="left", padx=10)

# Label com o nome "Administrador"
label_admin = tk.Label(frame_admin, text="Administrador", font=("Helvetica", 14), bg="white")
label_admin.pack(side="left", padx=10)
    
#exit function
def sair():
    # Janela de encerramento
    janela_saida = tk.Toplevel(root)
    janela_saida.title("Saindo...")
    janela_saida.geometry("200x100")
    janela_saida.grab_set()  # Bloqueia interações com a janela principal
    
    # Mensagem de saída
    label_saida = tk.Label(janela_saida, text="Encerrando, por favor, aguarde...")
    label_saida.pack(pady=10)

    # Barra de progresso circular
    progress_saida = ttk.Progressbar(janela_saida, mode="indeterminate", length=100)
    progress_saida.pack(pady=10)
    progress_saida.start(10)
    
    # Função para fechar a aplicação após alguns segundos
    root.after(2000, root.quit)  # Espera 2 segundos antes de fechar a aplicação
    
# Botão de sair no canto superior direito
btn_sair = tk.Button(frame_conteudo, image=icone_exit, text=" Sair", compound="left", anchor="w", bg="white", fg="red", bd=0, font=("Helvetica", 12), command=sair)
btn_sair.pack(anchor="ne", padx=10, pady=10)

criar_janela_home(frame_conteudo)

#-----------------Testes para passar o tempo-----------------

# Carregar a imagem PNG como ícone
icone = ImageTk.PhotoImage(file="icone.png")
root.iconphoto(True, icone)

#função para interceptar o fechamento da janela
def disable_event():
    # Intercepta o fechamento da janela e desativa a ação
    pass
#função para desativar tela-cheia
def disable_fullscreen(event=None):
    # Sai do modo de tela cheia, se ativado
    root.attributes("-fullscreen", False)


# Desabilita o botão de fechar
root.protocol("WM_DELETE_WINDOW", disable_event)

# Desabilita o redimensionamento da janela (impede maximização e redimensionamento manual)
root.resizable(False, False)

# Bloqueia o modo de tela cheia ao apertar F11 ou Alt+Enter
root.bind("<F11>", disable_fullscreen)
root.bind("<Alt-Return>", disable_fullscreen)

#------------------------------------------------------------

# Executar a janela
root.mainloop()