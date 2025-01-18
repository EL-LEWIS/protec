import tkinter as tk
from PIL import Image, ImageTk

# Função para carregar imagem redimensionada
def carregar_imagem(caminho, tamanho):
    imagem = Image.open(caminho)
    imagem = imagem.resize(tamanho, Image.ANTIALIAS)
    return ImageTk.PhotoImage(imagem)

# Função para criar uma imagem de retângulo arredondado
def create_rounded_rectangle(width, height, color, radius):
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=color)
    return ImageTk.PhotoImage(image)

# Função principal para exibir dados no frame
def def_mostrar_dados(frame_conteudo):
    # Limpar o conteúdo atual do frame
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    # Foto de perfil e nome do administrador
    frame_admin = tk.Frame(frame_conteudo, bg="white")
    frame_admin.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Carregar imagem de perfil
    try:
        imagem_perfil = carregar_imagem('perfil.png', (50, 50))
        label_imagem = tk.Label(frame_admin, image=imagem_perfil, bg="white")
        label_imagem.image = imagem_perfil
        label_imagem.pack(side="left", padx=10)
    except Exception as e:
        print(f"Erro ao carregar imagem de perfil: {e}")

    # Nome do Administrador
    label_admin = tk.Label(frame_admin, text="Administrador", font=("Helvetica", 14), bg="white")
    label_admin.pack(side="left", padx=10)

    # Linha separadora
    linha_preta = tk.Frame(frame_conteudo, bg="black", height=2, width=600)
    linha_preta.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Botão de sair
    btn_sair = tk.Button(frame_conteudo, text=" Sair", bg="white", fg="red", bd=0, font=("Helvetica", 12), command=sair)
    btn_sair.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # Título "Visão Geral"
    titulo = tk.Label(frame_conteudo, text="Visão Geral", font=("Arial", 24, "bold"))
    titulo.grid(row=2, column=0, padx=20, pady=20, sticky="nw")

    # Frame para resumos financeiros
    frame_imagens = tk.Frame(frame_conteudo, bg="white")
    frame_imagens.grid(row=3, column=0, padx=20, pady=20, sticky="nw")

    # Valores do banco de dados
    total_receber, total_pagar, receita_menos_despesas, recebidos_menos_pagos = obter_totais()

    # Configuração dos botões de resumo
    button_params = [
        {"text": f"R$ {total_receber:,.2f}\nTotal de Títulos a Receber(R$)", "bg_color": "#46b747", "button_color": "#1f7031", "text_color": "white"},
        {"text": f"R$ {recebidos_menos_pagos:,.2f}\nRecebidos - Pagos(R$)", "bg_color": "#6ae06b", "button_color": "#1f7031", "text_color": "white"},
        {"text": f"R$ {receita_menos_despesas:,.2f}\nReceita - Despesas(R$)", "bg_color": "#3aa747", "button_color": "#1c6524", "text_color": "white"},
        {"text": f"R$ {total_pagar:,.2f}\nTotal de Títulos a Pagar(R$)", "bg_color": "#e05044", "button_color": "#a43a34", "text_color": "white"},
    ]

    # Dimensões dos botões
    width, height = 250, 150
    corner_radius = 20

    # Criar botões de resumo financeiro
    for idx, params in enumerate(button_params):
        bg_image = create_rounded_rectangle(width, height, params["bg_color"], corner_radius)
        
        btn_frame = tk.Label(frame_imagens, image=bg_image, bd=0)
        btn_frame.image = bg_image
        
        btn_text = tk.Label(btn_frame, text=params["text"], fg=params["text_color"], font=("Arial", 12, "bold"), bg=params["bg_color"])
        btn_text.place(relx=0.5, rely=0.3, anchor="center")
        
        details_button = tk.Button(btn_frame, text="Ver detalhes", font=("Arial", 10), bg=params["button_color"], fg="white", borderwidth=0, command=ver_detalhes)
        details_button.place(relx=0.25, rely=0.75, anchor="center")
        
        arrow_label = tk.Label(btn_frame, text="←", fg="black", bg=params["bg_color"], font=("Arial", 12, "bold"))
        arrow_label.place(relx=0.85, rely=0.75, anchor="center")
        
        btn_frame.grid(row=idx // 2, column=idx % 2, padx=20, pady=20, sticky="nw")

    # Frame lateral para botões adicionais
    lateral_frame = tk.Frame(frame_conteudo, bg="#FFFFFF")
    lateral_frame.grid(row=3, column=1, padx=20, pady=20, sticky="n")

    botoes_laterais = [
        ("meusdados.png", "#FFD700"),
        ("duvidas.png", "#B0C4DE"),
        ("sistemupdate.png", "#8B4513"),
        ("configuracoes.png", "#483D8B")
    ]

    for i, (icone, cor_fundo) in enumerate(botoes_laterais):
        try:
            img_icone = carregar_imagem(icone, (150, 60))
            btn = tk.Button(lateral_frame, image=img_icone, borderwidth=0, highlightthickness=0, bg=None)
            btn.image = img_icone
            btn.grid(row=i, column=0, pady=5, sticky="ew")
        except Exception as e:
            print(f"Erro ao carregar ícone {icone}: {e}")

    lateral_frame.pack_propagate(False)


def_mostrar_dados()