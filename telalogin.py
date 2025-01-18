import tkinter as tk
import threading
import subprocess
import sys
import time
import sqlite3

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.create_login_screen()
        self.db_connection = sqlite3.connect('seu_banco_de_dados.db')
        self.cursor = self.db_connection.cursor()

    def create_login_screen(self):
        # Frame principal de login
        self.login_frame = tk.Frame(self.root, bg="#2c3455")
        self.login_frame.pack(fill="both", expand=True)

        label_title = tk.Label(self.login_frame, text="PROTEC", font=("Helvetica", 18, "bold"), bg="#2c3455", fg="white")
        label_title.pack(pady=20)

        email_label = tk.Label(self.login_frame, text="Email", font=("Helvetica", 12), bg="#2c3455", fg="white")
        email_label.pack()
        self.email_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=30)
        self.email_entry.pack(pady=5)

        senha_label = tk.Label(self.login_frame, text="Senha", font=("Helvetica", 12), bg="#2c3455", fg="white")
        senha_label.pack()
        self.senha_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=30, show="*")
        self.senha_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="LOGIN", font=("Helvetica", 12), bg="#6C4EBF", fg="white", width=20, height=2, command=self.verificar_login)
        login_button.pack(pady=20)

    def verificar_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        # Consulta para verificar email e senha no banco de dados
        self.cursor.execute('SELECT nome, cargo FROM Funcionario WHERE email = ? AND senha = ?', (email, senha))
        result = self.cursor.fetchone()

        if result:
            self.nome_usuario, self.cargo_usuario = result
            self.mostrar_bem_vindo()
        else:
            tk.messagebox.showerror("Erro", "Email ou senha incorretos. Tente novamente.")

    def mostrar_bem_vindo(self):
        # Esconde o frame de login
        self.login_frame.pack_forget()

        # Cria o frame de "Bem-vindo" com efeito fade in/out
        self.welcome_frame = tk.Frame(self.root, bg="#2c3455")
        self.welcome_frame.pack(fill="both", expand=True)

        # Exibe o nome e cargo do usuário
        mensagem_bem_vindo = f"Bem-vindo {self.nome_usuario} ({self.cargo_usuario})"
        self.label_welcome = tk.Label(self.welcome_frame, text=mensagem_bem_vindo, font=("Helvetica", 16, "bold"), fg="white", bg="#2c3455")
        self.label_welcome.place(relx=0.5, rely=0.5, anchor="center")

        self.fade_in_out_text(self.label_welcome, 1.0)  # Inicia o efeito fade in/out
        self.root.after(5000, self.mostrar_entrada)  # Após 3 segundos, mostra o círculo giratório

    def fade_in_out_text(self, label, opacity):
        # Efeito fade in/out para o texto "Bem-vindo"
        label.config(fg=f"#{int(255 * opacity):02x}{int(255 * opacity):02x}{int(255 * opacity):02x}")
        if opacity > 0:
            self.root.after(80, self.fade_in_out_text, label, opacity - 0.05)

    def mostrar_entrada(self):
        # Esconde o frame de "Bem-vindo"
        self.welcome_frame.pack_forget()

        # Cria o frame de carregamento centralizado
        self.loading_frame = tk.Frame(self.root, bg="#2c3455")
        self.loading_frame.pack(fill="both", expand=True)

        # Centralizando o texto "Entrando..." e o círculo
        label_text = tk.Label(self.loading_frame, text="Entrando...", font=("Helvetica", 14), bg="#2c3455", fg="white")
        label_text.place(relx=0.5, rely=0.4, anchor="center")

        self.label_loading = tk.Label(self.loading_frame, text="◐", font=("Helvetica", 24), fg="white", bg="#2c3455")
        self.label_loading.place(relx=0.5, rely=0.5, anchor="center")

        # Inicia a animação de carregamento em uma nova thread
        threading.Thread(target=self.animate_loading).start()

    def animate_loading(self):
        chars = "◐◓◑◒"  # Círculo giratório com caracteres
        start_time = time.time()
        while time.time() - start_time < 10:
            for char in chars:
                # Atualiza o texto do círculo giratório
                self.label_loading.config(text=char)
                time.sleep(0.25)  # Intervalo entre as mudanças de caractere
                self.label_loading.update_idletasks()  # Atualiza a interface

        # Após 10 segundos, executa o próximo script e fecha a janela atual
        self.on_login_success()

    def on_login_success(self):
        # Executa o script 'baseinterface.py'
        subprocess.run([sys.executable, 'baseinterface.py'])
        print("Login bem-sucedido! Executando baseinterface.py")
        
        # Fecha a janela principal
        self.root.destroy()

    def __del__(self):
        # Fecha a conexão com o banco de dados ao finalizar
        self.db_connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PROTEC")
    root.configure(bg="#2c3455")
    root.geometry("400x300")
    app = LoginScreen(root)
    root.mainloop()
