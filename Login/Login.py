from tkinter import Tk, Label, Entry, Button, PhotoImage, Toplevel
import time
import threading

# Função para verificar login
def check_login(email, password, window):
    if email == "admin@admin.com" and password == "admin":
        window.destroy()  # Fecha a janela atual
        show_loading_screen()

# Função para mostrar a tela de carregamento
def show_loading_screen():
    loading_window = Toplevel()
    loading_window.title("PROTEC")
    loading_window.geometry("960x600")
    loading_window.config(bg="#2E3957")

    # Texto de carregamento
    loading_label = Label(loading_window, text="Logando em sua conta", fg="white", bg="#2E3957", font=("Arial", 16))
    loading_label.pack(pady=200)

    # Imagem de círculo que vai girar
    circle_img = PhotoImage(file="mnt/data/circle.png")
    circle_label = Label(loading_window, image=circle_img, bg="#2E3957")
    circle_label.pack()

    # Função para simular o tempo de carregamento
    def simulate_loading():
        time.sleep(33)  # Simula 33 segundos de carregamento
        loading_window.destroy()  # Fecha a janela de carregamento
        # Aqui você pode chamar a próxima tela (outro arquivo Python)

    # Inicia a simulação de carregamento em uma thread separada
    threading.Thread(target=simulate_loading).start()

    loading_window.mainloop()

# Função para criar a tela de login
def create_login_screen():
    root = Tk()
    root.title("PROTEC")
    root.geometry("960x600")
    root.config(bg="#2E3957")

    # Centralizar todos os widgets
    center_x = 480  # Metade da largura da tela (960/2)
    logo_y = 50
    entry_height = 40
    button_height = 60

    # Logo
    logo_label = Label(root, text="PROTEC", fg="white", bg="#2E3957", font=("Arial", 36, "bold"))
    logo_label.place(x=center_x - 100, y=logo_y)

    # Entrada de Email com ícone de usuário
    user_icon = PhotoImage(file="mnt/data/vector.png")
    user_label = Label(root, image=user_icon, bg="#2E3957")
    user_label.place(x=center_x - 150, y=logo_y + 100)

    email_entry = Entry(root, width=25, font=("Arial", 16), bg="#E3E3E3")
    email_entry.insert(0, "Email")
    email_entry.place(x=center_x - 100, y=logo_y + 100, height=entry_height)

    # Entrada de Senha com ícone de cadeado
    lock_icon = PhotoImage(file="mnt/data/vector2.png")
    lock_label = Label(root, image=lock_icon, bg="#2E3957")
    lock_label.place(x=center_x - 150, y=logo_y + 180)

    password_entry = Entry(root, width=25, font=("Arial", 16), show="*", bg="#E3E3E3")
    password_entry.insert(0, "Senha")
    password_entry.place(x=center_x - 100, y=logo_y + 180, height=entry_height)

    # Botão de Login
    login_button_img = PhotoImage(file="mnt/data/Button.png")
    login_button = Button(root, image=login_button_img, command=lambda: check_login(email_entry.get(), password_entry.get(), root), borderwidth=0)
    login_button.place(x=center_x - 125, y=logo_y + 280, width=250, height=button_height)

    # Texto sobre o botão
    login_text = Label(root, text="LOGIN", fg="white", bg="#6C47E1", font=("Arial", 18, "bold"))
    login_text.place(x=center_x - 35, y=logo_y + 295)

    root.mainloop()

# Cria a tela de login
create_login_screen()
