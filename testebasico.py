import tkinter as tk
from PIL import Image, ImageTk  # Necessário instalar a biblioteca Pillow para carregar o ícone


# Criação da janela principal
root = tk.Tk()
root.overrideredirect(True)  # Remove a barra de título padrão
root.geometry("600x400")  # Define o tamanho da janela


root.mainloop()
