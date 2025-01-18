import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def criar_label_arredondada(texto, cor_fundo, largura, altura, raio=20):
    imagem = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    draw = ImageDraw.Draw(imagem)
    draw.rounded_rectangle((0, 0, largura, altura), radius=raio, fill=cor_fundo)
    imagem_tk = ImageTk.PhotoImage(imagem)

    label = tk.Label(frame_resumo, text=texto, font=("Helvetica", 12, "bold"), width=15, height=2)
    label.config(image=imagem_tk, compound="center")
    label.image = imagem_tk  # Necessário para manter a referência da imagem
    return label

root = tk.Tk()
root.geometry("960x600")  # Define o tamanho da janela
frame_resumo = tk.Frame(root)
frame_resumo.pack(pady=10)

# Dimensões da imagem de fundo (ajuste conforme necessário)
largura, altura = 150, 60

# Labels com bordas arredondadas
entradas_label = criar_label_arredondada(f"ENTRADAS\nR$ {1234.56:,.2f}", "lime", largura, altura)
entradas_label.grid(row=0, column=0, padx=5, pady=5)

saidas_label = criar_label_arredondada(f"SAÍDAS\nR$ {567.89:,.2f}", "red", largura, altura)
saidas_label.grid(row=0, column=1, padx=5, pady=5)

saldo_label = criar_label_arredondada(f"SALDO\nR$ {666.67:,.2f}", "yellow", largura, altura)
saldo_label.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()
