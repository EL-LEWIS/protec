import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3





#funções------------------------------------------
#função HOME
def criar_janela_home(frame_conteudo):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

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

    # Botão de sair no canto superior direito
    btn_sair = tk.Button(frame_conteudo, image=icone_exit, text=" Sair", compound="left", anchor="w", bg="white", fg="red", bd=0, font=("Helvetica", 12))
    btn_sair.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # Título "Visão Geral"
    titulo = tk.Label(frame_conteudo, text="Visao Geral", font=("Arial", 24, "bold"))
    titulo.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

    # Carregar imagem das 4 telas
    try:
        imagem_4telas = carregar_imagem("4Telas.png", (600, 300))  # Carregar e redimensionar imagem
        img_label = tk.Label(frame_conteudo, image=imagem_4telas)
        img_label.image = imagem_4telas  # Manter a referência para evitar o descarte pelo garbage collector
        img_label.grid(row=2, column=0, padx=20, pady=20, sticky="nw")  # Manter a imagem na grade
    except Exception as e:
        print(f"Erro ao carregar imagem das 4 telas: {e}")

    # Frame lateral para botões
    lateral_frame = tk.Frame(frame_conteudo, bg="#FFFFFF")
    lateral_frame.grid(row=2, column=1, padx=20, pady=20, sticky="n")  # Usar grid para posicionar ao lado

    # Carregar e exibir botões laterais
    botoes_laterais = [
        ("meusdados.png", "#FFD700"),
        ("duvidas.png", "#B0C4DE"),
        ("sistemupdate.png", "#8B4513"),
        ("configuracoes.png", "#483D8B")
    ]

    for i, (icone, cor_fundo) in enumerate(botoes_laterais):
        try:
            img_icone = carregar_imagem(icone, (150, 60))  # Redimensionar o ícone
            btn = tk.Button(lateral_frame, image=img_icone, borderwidth=0, highlightthickness=0, bg=None)
            btn.image = img_icone  # Manter a referência da imagem
            btn.grid(row=i, column=0, pady=5, sticky="ew")  # Usar grid e ajustar padding
        except Exception as e:
            print(f"Erro ao carregar ícone {icone}: {e}")

    # Ajustar a visualização
    lateral_frame.pack_propagate(False)  # Evitar que o frame diminua

#-------------------------------------------------
# Função para exibir a tabela de funcionários
def exibir_funcionarios():
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Função para buscar funcionários por nome
    def buscar_funcionarios():
        filtro_nome = entry_pesquisa.get()

        # Debug para verificar se a função está sendo chamada
        print("Botão de busca pressionado. Filtro: ", filtro_nome)

        # Se o campo de busca estiver vazio, exibe todos os funcionários
        if filtro_nome.strip() == "":
            query = "SELECT nome, CPF, email, telefone FROM Funcionario"
            cursor.execute(query)
        else:
            # Buscar apenas se houver algo no campo de pesquisa
            query = "SELECT nome, CPF, email, telefone FROM Funcionario WHERE nome LIKE ?"
            cursor.execute(query, ('%' + filtro_nome + '%',))

        funcionarios = cursor.fetchall()

        # Debug para verificar se há resultados da consulta
        print("Funcionários encontrados: ", funcionarios)

        # Se nenhum funcionário for encontrado, exibir uma mensagem
        if not funcionarios:
            messagebox.showinfo("Nenhum resultado", "Nenhum funcionário encontrado com esse nome.")
        else:
            atualizar_tabela(funcionarios)

    # Função para atualizar a tabela
    def atualizar_tabela(funcionarios):
        # Limpar a tabela antes de inserir novos dados
        for row in tree.get_children():
            tree.delete(row)
        # Inserir os funcionários encontrados
        for funcionario in funcionarios:
            tree.insert("", "end", values=funcionario)

    # Função para abrir uma janela de edição de funcionários
    def editar_funcionario():
        item_selecionado = tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um funcionário para editar.")
            return

        valores = tree.item(item_selecionado, 'values')
        nome_selecionado = valores[0]

        # Abrir nova janela para edição
        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar Funcionário")

        # Campos de entrada para editar o funcionário
        tk.Label(janela_edicao, text="Nome").grid(row=0, column=0)
        entry_nome = tk.Entry(janela_edicao)
        entry_nome.grid(row=0, column=1)
        entry_nome.insert(0, valores[0])  # Preenche o campo com o nome atual

        tk.Label(janela_edicao, text="CPF").grid(row=1, column=0)
        entry_cpf = tk.Entry(janela_edicao)
        entry_cpf.grid(row=1, column=1)
        entry_cpf.insert(0, valores[1])  # Preenche o campo com o CPF atual

        tk.Label(janela_edicao, text="E-mail").grid(row=2, column=0)
        entry_email = tk.Entry(janela_edicao)
        entry_email.grid(row=2, column=1)
        entry_email.insert(0, valores[2])  # Preenche o campo com o e-mail atual

        tk.Label(janela_edicao, text="Telefone").grid(row=3, column=0)
        entry_telefone = tk.Entry(janela_edicao)
        entry_telefone.grid(row=3, column=1)
        entry_telefone.insert(0, valores[3])  # Preenche o campo com o telefone atual

        # Função para salvar as alterações
        def salvar_alteracoes():
            novo_nome = entry_nome.get()
            novo_cpf = entry_cpf.get()
            novo_email = entry_email.get()
            novo_telefone = entry_telefone.get()

            # Atualizar no banco de dados
            cursor.execute("""
                UPDATE Funcionario
                SET nome = ?, CPF = ?, email = ?, telefone = ?
                WHERE nome = ?
            """, (novo_nome, novo_cpf, novo_email, novo_telefone, nome_selecionado))
            conn.commit()

            # Atualiza a tabela com os novos dados
            buscar_funcionarios()
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            janela_edicao.destroy()

        # Botão para salvar as alterações
        btn_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_alteracoes)
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    # Título da página de funcionários
    label_titulo = tk.Label(frame_conteudo, text="Funcionários", font=("Helvetica", 16, "bold"), bg="white")
    label_titulo.pack(pady=10)

    # Barra de pesquisa
    frame_pesquisa = tk.Frame(frame_conteudo, bg="white")
    frame_pesquisa.pack(pady=10)

    label_pesquisa = tk.Label(frame_pesquisa, text="Buscar:", bg="white", font=("Helvetica", 12))
    label_pesquisa.pack(side="left", padx=5)

    entry_pesquisa = tk.Entry(frame_pesquisa, font=("Helvetica", 12), width=30)
    entry_pesquisa.pack(side="left", padx=5)

    btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=buscar_funcionarios, bg="#2E3B59", fg="white", font=("Helvetica", 12))
    btn_pesquisar.pack(side="left", padx=5)

    # Tabela de funcionários
    colunas = ("Nome", "CPF", "E-mail", "Telefone")
    tree = ttk.Treeview(frame_conteudo, columns=colunas, show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("E-mail", text="E-mail")
    tree.heading("Telefone", text="Telefone")
    tree.pack(fill="both", expand=True)

    # Botão de editar
    btn_editar = tk.Button(frame_conteudo, text="Editar Funcionário", command=editar_funcionario, bg="#2E3B59", fg="white", font=("Helvetica", 12))
    btn_editar.pack(pady=10)

    # Carregar os funcionários inicialmente
    cursor.execute("SELECT nome, CPF, email, telefone FROM Funcionario")
    funcionarios = cursor.fetchall()
    atualizar_tabela(funcionarios)

    # Fechar a conexão com o banco de dados
    conn.close()
#-------------------------------------------------
# Função para exibir clientes físicos ou jurídicos
def exibir_clientes(tipo_cliente):
    # Limpar o conteúdo atual do frame principal
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

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
        nome_selecionado = valores[0]
        
        # Implementar a lógica para abrir uma nova janela ou seção que permite editar as informações
        messagebox.showinfo("Editar", f"Editar informações de {nome_selecionado}")
        # Aqui você pode abrir uma nova janela com os detalhes completos do cliente para edição

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

    # Tabela de clientes
    tree = ttk.Treeview(frame_conteudo, columns=colunas, show="headings")
    for coluna in colunas:
        tree.heading(coluna, text=coluna)
    tree.pack(fill="both", expand=True)

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

#-------------------------------------------------------------------------------------------------------




# Função para redimensionar e carregar imagens
def carregar_imagem(caminho, tamanho):
    imagem = Image.open(caminho)
    imagem = imagem.resize(tamanho, Image.LANCZOS)
    return ImageTk.PhotoImage(imagem)

# Inicializando janela principal
root = tk.Tk()
root.title("PROTEC - Interface Base")
root.geometry("800x600")  # Define o tamanho da janela

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

btn_clientes = tk.Button(frame_menu, image=icone_clientes, text=" Clientes", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=lambda: exibir_clientes('fisico'))
btn_clientes.pack(fill="x", pady=10)

# Novo botão Funcionários
btn_funcionarios = tk.Button(frame_menu, image=icone_clientes, text=" Funcionários", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0, command=exibir_funcionarios)
btn_funcionarios.pack(fill="x", pady=10)

btn_cadastros = tk.Button(frame_menu, image=icone_cadastros, text=" Cadastros", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0)
btn_cadastros.pack(fill="x", pady=10)

btn_produto = tk.Button(frame_menu, image=icone_produto, text=" Produto", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0)
btn_produto.pack(fill="x", pady=10)

btn_financeiro = tk.Button(frame_menu, image=icone_financeiro, text=" Financeiro", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0)
btn_financeiro.pack(fill="x", pady=10)

btn_servicos = tk.Button(frame_menu, image=icone_servicos, text=" Serviços", compound="left", anchor="w", bg="#2E3B59", fg="white", font=("Helvetica", 12), bd=0)
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

# Botão de sair no canto superior direito
btn_sair = tk.Button(frame_conteudo, image=icone_exit, text=" Sair", compound="left", anchor="w", bg="white", fg="red", bd=0, font=("Helvetica", 12))
btn_sair.pack(anchor="ne", padx=10, pady=10)


# Executar a janela
root.mainloop()