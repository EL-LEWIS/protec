import tkinter as tk
from tkinter import ttk

# Configuração da janela principal
root = tk.Tk()
root.title("Carregando...")
root.geometry("200x100")

# Texto informativo
label = tk.Label(root, text="Carregando, por favor, aguarde...")
label.pack(pady=10)

# Barra de progresso circular (modo indeterminado)
progress = ttk.Progressbar(root, mode="indeterminate", length=100)
progress.pack(pady=10)

# Inicia o progresso indeterminado
progress.start(10)  # valor em milissegundos entre cada atualização do progresso

# Inicia o loop principal da aplicação
root.mainloop()
