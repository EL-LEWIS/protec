import sqlite3
import re
from datetime import datetime

def verificar_existencia(cpf=None, email=None):
    conn = conectar_banco()
    cursor = conn.cursor()

    if cpf:
        cursor.execute("SELECT COUNT(*) FROM Funcionario WHERE CPF = ?", (cpf,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True  # CPF já existe

    if email:
        cursor.execute("SELECT COUNT(*) FROM Funcionario WHERE email = ?", (email,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True  # Email já existe


    conn.close()
    return False  # Nenhum duplicado encontrado

def verificar_existencia_ClienteFisico(cpf=None, email=None):
    conn = conectar_banco()
    cursor = conn.cursor()

    if cpf:
        cursor.execute("SELECT COUNT(*) FROM Cliente_Fisico WHERE CPF = ?", (cpf,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True  # CPF já existe

    if email:
        cursor.execute("SELECT COUNT(*) FROM Cliente_Fisico WHERE email_cliente = ?", (email,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True  # Email já existe
        
def verificar_existencia_ClienteJuridico(cnpj=None, email=None):
    conn = conectar_banco()
    cursor = conn.cursor()

    if cnpj:
        cursor.execute("SELECT COUNT(*) FROM Cliente_Juridico WHERE CNPJ = ?", (cnpj,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True  # CNPJ já existe

    if email:
        cursor.execute("SELECT COUNT(*) FROM Cliente_Juridico WHERE email_empresa = ?", (email,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True  # Email já existe


    conn.close()
    return False  # Nenhum duplicado encontrado

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None


# Validador de cpf
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf, multiplicadores):
        soma = sum([int(cpf[i]) * multiplicadores[i] for i in range(len(multiplicadores))])
        digito = (soma * 10) % 11
        return digito if digito < 10 else 0

    multiplicadores_1 = list(range(10, 1, -1))
    multiplicadores_2 = list(range(11, 2, -1))

    digito_1 = calcular_digito(cpf, multiplicadores_1)
    digito_2 = calcular_digito(cpf, multiplicadores_2 + [digito_1])

    return cpf[-2:] == f"{digito_1}{digito_2}"

# Validador de CNPJ
def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, multiplicadores):
        soma = sum([int(cnpj[i]) * multiplicadores[i % len(multiplicadores)] for i in range(len(multiplicadores))])
        digito = (soma % 11)
        return 0 if digito < 2 else 11 - digito

    multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    digito_1 = calcular_digito(cnpj, multiplicadores_1)
    digito_2 = calcular_digito(cnpj, multiplicadores_2)

    return cnpj[-2:] == f"{digito_1}{digito_2}"

def conectar_banco():
    return sqlite3.connect('protec_db.db')

# Função de login
def login(setor):
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    conn = conectar_banco()
    cursor = conn.cursor()

    if setor == "Funcionário":
        cursor.execute("SELECT nome FROM Funcionario WHERE email = ? AND senha = ?", (email, senha))
    elif setor == "Gerente":
        cursor.execute("SELECT nome FROM Funcionario WHERE email = ? AND senha = ? AND cargo = 'Gerente'", (email, senha))
    elif setor == "RH":
        cursor.execute("SELECT nome FROM Funcionario WHERE email = ? AND senha = ? AND cargo = 'RH'", (email, senha))
    elif setor == "Admin":
        cursor.execute("SELECT nome FROM Admin WHERE email = ? AND senha = ?", (email, senha))

    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

# Funções para o menu Funcionário -------------------------------------------------------------------------------------------------------------------------<
def cadastrar_cliente_fisico():
    nome = input("Digite o nome do cliente físico: ")
    cpf = input("Digite o CPF: ")
    
    if not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        return
    
    endereco = input("Digite o endereço: ")
    telefone = input("Digite o telefone: ")
    email_cliente = input("Digite o email do cliente: ")
    
    if not validar_email(email_cliente):
        print("EMAIL inválido. Tente novamente.")
        return
    
    
    # Verifica se o CPF ou o e-mail já existem
    if verificar_existencia_ClienteFisico(cpf=cpf, email=email_cliente):
        print("Erro: CPF ou e-mail já estão cadastrados no sistema!")
        return
    
    senha = input("Digite a senha: ")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Cliente_Fisico (nome, CPF, endereco, telefone, email_cliente, senha) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (nome, cpf, endereco, telefone, email_cliente, senha))
    conn.commit()
    conn.close()
    print("Cliente físico cadastrado com sucesso!")

def inserir_cliente_juridico():
    cnpj = input("Digite o CNPJ: ")
    
        # Verifica se o CNPJ já existe
    if verificar_existencia_ClienteJuridico(cnpj=cnpj):
        print("Erro: CNPJ já cadastrado!")
        return
    
    nome_empresa = input("Digite o nome da empresa: ")
    nome_representante = input("Digite o nome do representante: ")
    email_empresa = input("Digite o email da empresa: ")
    
       # Verifica se o EMAIL já existe
    if verificar_existencia_ClienteJuridico(email=email_empresa):
        print("Erro: E-mail já cadastrado!")
        return

    telefone_empresa = input("Digite o telefone da empresa: ")
    telefone_representante = input("Digite o telefone do representante: ")
    email_representante = input("Digite o email do representante: ")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Cliente_Juridico (CNPJ, nome_empresa, nome_representante, email_empresa, 
                      telefone_empresa, telefone_representante, email_representante) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (cnpj, nome_empresa, nome_representante, email_empresa, telefone_empresa, telefone_representante, email_representante))
    conn.commit()
    conn.close()
    print("Cliente jurídico cadastrado com sucesso!")

def editar_ou_excluir_pedido():
    id_pedido = input("Digite o ID do pedido que deseja editar ou excluir: ")
    
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedido WHERE id_pedido = ?", (id_pedido,))
    pedido = cursor.fetchone()
    
    if pedido:
        print("Pedido encontrado:", pedido)
        acao = input("Digite 'e' para editar ou 'd' para excluir: ")
        
        if acao == 'e':
            quantidade = input("Nova quantidade: ")
            forma_pagamento = input("Nova forma de pagamento: ")
            status_envio_produto = input("Novo status de envio: ")
            valor_total = input("Novo valor total: ")
            status_pagamento = input("Novo status de pagamento: ")

            cursor.execute('''UPDATE Pedido SET quantidade = ?, forma_pagamento = ?, 
                              status_envio_produto = ?, valor_total = ?, 
                              status_pagamento_pedido = ? WHERE id_pedido = ?''',
                           (quantidade, forma_pagamento, status_envio_produto, valor_total, status_pagamento, id_pedido))
            conn.commit()
            print("Pedido editado com sucesso!")
        
        elif acao == 'd':
            cursor.execute("DELETE FROM Pedido WHERE id_pedido = ?", (id_pedido,))
            conn.commit()
            print("Pedido excluído com sucesso!")
    else:
        print("Pedido não encontrado.")
    
    conn.close()

def mostrar_produto():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Produto")
    produtos = cursor.fetchall()
    conn.close()

    if produtos:
        print("Produtos disponíveis:")
        for produto in produtos:
            print(produto)
    else:
        print("Nenhum produto encontrado.")

def visualizar_ou_cadastrar_servicos():
    acao = input("Digite 'v' para visualizar ou 'c' para cadastrar: ")

    if acao == 'c':
        nome_servico = input("Digite o nome do serviço: ")
        preco_servico = input("Digite o preço do serviço: ")

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Servicos (nome_servico, preco_servico) VALUES (?, ?)''',
                       (nome_servico, preco_servico))
        conn.commit()
        conn.close()
        print("Serviço cadastrado com sucesso!")
    
    elif acao == 'v':
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Servicos")
        servicos = cursor.fetchall()
        conn.close()

        if servicos:
            print("Serviços disponíveis:")
            for servico in servicos:
                print(servico)
        else:
            print("Nenhum serviço encontrado.")

def visualizar_ou_editar_estoque():
    acao = input("Digite 'v' para visualizar ou 'e' para editar: ")

    if acao == 'e':
        cod_estoque = input("Digite o código do estoque que deseja editar: ")
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Estoque WHERE cod_estoque = ?", (cod_estoque,))
        estoque = cursor.fetchone()

        if estoque:
            print("Estoque encontrado:", estoque)
            nome_produto = input("Novo nome do produto: ")
            quantidade = input("Nova quantidade: ")
            endereco = input("Novo endereço: ")

            cursor.execute('''UPDATE Estoque SET nome_produto = ?, quantidade = ?, endereco = ? 
                              WHERE cod_estoque = ?''',
                           (nome_produto, quantidade, endereco, cod_estoque))
            conn.commit()
            print("Estoque editado com sucesso!")
        else:
            print("Estoque não encontrado.")
        
        conn.close()
    elif acao == 'v':
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Estoque")
        estoques = cursor.fetchall()
        conn.close()

        if estoques:
            print("Estoque disponível:")
            for estoque in estoques:
                print(estoque)
        else:
            print("Nenhum estoque encontrado.")

def cadastrar_pedido():  
    conn = sqlite3.connect('protec_db.db')
    cursor = conn.cursor()  

    # Coletando dados do usuário  
    id_cliente = int(input("Digite o ID do cliente: "))  
    quantidade = int(input("Digite a quantidade: "))  
    data_pedido = datetime.now().strftime('%Y-%m-%d')  # Obtendo a data atual no formato YYYY-MM-DD  
    forma_pagamento = input("Digite a forma de pagamento: ")  
    status_envio_produto = input("Digite o status de envio do produto: ")  
    valor_total = float(input("Digite o valor total: "))  
    status_pagamento_pedido = input("Digite o status de pagamento do pedido: ")  

    # Inserindo os dados na tabela Pedido  
    try:  
        cursor.execute('''  
            INSERT INTO Pedido (id_cliente, quantidade, data_pedido, forma_pagamento,   
                                status_envio_produto, valor_total, status_pagamento_pedido)   
            VALUES (?, ?, ?, ?, ?, ?, ?)  
        ''', (id_cliente, quantidade, data_pedido, forma_pagamento,   
              status_envio_produto, valor_total, status_pagamento_pedido))  

        conn.commit()  
        print("Pedido cadastrado com sucesso!")  
    
    except sqlite3.Error as e:  
        print(f"Um erro ocorreu: {e}")  
    
    finally:  
        # Fechando a conexão  
        conn.close()



# Funções para o menu Gerente

def visualizar_estoque():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Estoque")
    produtos = cursor.fetchall()

    print("Produtos em Estoque:")
    for produto in produtos:
        print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Preço: {produto[3]}")

    conn.close()

def editar_estoque():
    visualizar_estoque()
    id_produto = int(input("Digite o ID do produto que deseja editar: "))
    nova_quantidade = int(input("Digite a nova quantidade: "))
    novo_preco = float(input("Digite o novo preço: "))

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''UPDATE Estoque
                      SET quantidade = ?, preco = ?
                      WHERE id_produto = ?''',
                   (nova_quantidade, novo_preco, id_produto))

    conn.commit()
    conn.close()
    print("Estoque atualizado com sucesso!")

#Funções sem TABELA aplicada(FORNECEDORES, SERVIÇOS, VENDAS)!!!!!
def cadastrar_fornecedor():
    nome = input("Digite o nome do fornecedor: ")
    cnpj = input("Digite o CNPJ do fornecedor: ")

    # Verifica se o CNPJ já existe
    if verificar_existencia(cnpj=cnpj):
        print("Erro: CNPJ já cadastrado!")
        return

    telefone = input("Digite o telefone do fornecedor: ")
    email = input("Digite o email do fornecedor: ")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Fornecedor (nome, CNPJ, telefone, email)
                      VALUES (?, ?, ?, ?)''',
                   (nome, cnpj, telefone, email))

    conn.commit()
    conn.close()
    print("Fornecedor cadastrado com sucesso!")

def ver_status_servicos():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Servicos")
    servicos = cursor.fetchall()

    print("Status dos Serviços:")
    for servico in servicos:
        print(f"ID: {servico[0]}, Nome: {servico[1]}, Status: {servico[2]}")

    conn.close()
    
def relatorio_vendas():  
    conn = conectar_banco()  
    cursor = conn.cursor()  
    
    # Seleciona apenas as colunas desejadas  
    cursor.execute("SELECT id_pedido, data_pedido, status_envio_produto, status_pagamento_pedido, valor_total FROM Pedido")  
    vendas = cursor.fetchall()  

    print("Relatório de Vendas:")  
    for venda in vendas:  
        print(f"ID: {venda[0]}, Data: {venda[1]}, Status de Envio: {venda[2]}, Status de Pagamento: {venda[3]}, Valor Total: {venda[4]}")  

    conn.close()  
    
    
def cadastrar_fornecedor():
    nome_fornecedor = input("Digite o nome do fornecedor: ")
    contato = input("Digite o contato do fornecedor: ")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Fornecedor (nome_fornecedor, contato) VALUES (?, ?)''',
                   (nome_fornecedor, contato))
    conn.commit()
    conn.close()
    print("Fornecedor cadastrado com sucesso!")

#--------------------------------------------------------------------------------

def ver_status_financas():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Financas")
    financas = cursor.fetchall()
    conn.close()

    if financas:
        print("Status das Finanças:")
        for financa in financas:
            print(financa)
    else:
        print("Nenhuma informação financeira encontrada.")






# Funções para o menu RH
def administrar_salario_funcionarios():
    conn = conectar_banco()
    cursor = conn.cursor()

    cpf = input("Digite o CPF do funcionário cujo salário deseja alterar: ")
    novo_salario = float(input("Digite o novo salário: "))

    cursor.execute('''UPDATE Funcionario SET salario = ? WHERE CPF = ?''', (novo_salario, cpf))

    conn.commit()
    conn.close()
    print("Salário do funcionário atualizado com sucesso!")
    
def cadastrar_gerente():
    conn = conectar_banco()
    cursor = conn.cursor()

    cpf = input("Digite o CPF do funcionário a ser promovido ou demitido: ")
    acao = input("Digite 'promover' para promover ou 'demitir' para demitir: ").strip().lower()

    if acao == "promover":
        novo_cargo = input("Digite o novo cargo: ")
        cursor.execute('''UPDATE Funcionario SET cargo = ? WHERE CPF = ?''', (novo_cargo, cpf))
        print("Funcionário promovido com sucesso!")
    elif acao == "demitir":
        cursor.execute('''DELETE FROM Funcionario WHERE CPF = ?''', (cpf,))
        print("Funcionário demitido com sucesso!")
    else:
        print("Ação inválida!")

    conn.commit()
    conn.close()


def gerenciar_ferias():
    # Implementar gerenciamento de férias
    pass

def exibir_funcionarios():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''SELECT nome, CPF, cargo, telefone FROM Funcionario''')
    funcionarios = cursor.fetchall()

    print("Funcionários:")
    print("Nome | CPF | Cargo | Telefone")
    for funcionario in funcionarios:
        print(f"{funcionario[0]} | {funcionario[1]} | {funcionario[2]} | {funcionario[3]}")

    conn.close()


# Funções para o menu Admin
def cadastrar_funcionario_admin():
    conn = conectar_banco()
    cursor = conn.cursor()

    nome = input("Digite o nome do funcionário: ")
    cpf = input("Digite o CPF do funcionário: ")
    if not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        return
    
    email = input("Digite o email do funcionário: ")
    if not validar_email(email):
        print("CPF inválido. Tente novamente.")
        return
    
        # Verifica se o CPF ou o e-mail já existem
    if verificar_existencia(cpf=cpf, email=email):
        print("Erro: CPF ou e-mail já estão cadastrados no sistema!")
        return
    
    telefone = input("Digite o telefone: ")
    senha = input("Digite a senha: ")
    cargo = input("Digite o cargo do funcionário: ")
    salario = float(input("Digite o salário do funcionário: "))  # Converte para float
    id_departamento = int(input("Digite o ID do departamento: "))  # Converte para inteiro

    # Insere os dados no banco com todas as colunas necessárias
    cursor.execute('''INSERT INTO Funcionario (nome, CPF, email, telefone, senha, cargo, salario, id_departamento)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (nome, cpf, email, telefone, senha, cargo, salario, id_departamento))

    conn.commit()
    conn.close()
    print("Funcionário cadastrado com sucesso!")



def ver_todos_os_funcionarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Funcionario")
    funcionarios = cursor.fetchall()
    conn.close()

    if funcionarios:
        print("Todos os Funcionários:")
        for funcionario in funcionarios:
            print(funcionario)
    else:
        print("Nenhum funcionário encontrado.")

def ver_relatorio_completo_vendas():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedido")
    relatorio = cursor.fetchall()
    conn.close()

    if relatorio:
        print("Relatório Completo de Vendas:")
        for venda in relatorio:
            print(venda)
    else:
        print("Nenhuma venda encontrada.")

def gerenciar_financas():
    # Implementar gerenciamento das finanças
    pass

# Função principal do menu
def menu():
    while True:
        print('...:: ᑭᖇOTᕮᑕ ::...')
        print(" !!!BEM VINDO!!!")
        print("\nEscolha um setor:")
        print("1. Funcionário 'outros'")
        print("2. Gerente")
        print("3. RH")
        print("4. Admin")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            break

        setor = None
        if escolha == '1':
            setor = "Funcionário"
        elif escolha == '2':
            setor = "Gerente"
        elif escolha == '3':
            setor = "RH"
        elif escolha == '4':
            setor = "Admin"
        else:
            print("Opção inválida!")
            continue

        usuario = login(setor)

        if usuario:
            print(f"Bem-vindo, {usuario}!")
            if setor == "Funcionário":
                while True:
                    print("\nMenu Funcionário:")
                    print("1. Cadastrar Cliente Físico")
                    print("2. Inserir Cliente Jurídico")
                    print("3. Editar ou Excluir Pedido")
                    print("4. Mostrar Produto")
                    print("5. Visualizar ou Cadastrar Serviços")
                    print("6. Visualizar ou Editar Estoque")
                    print("7. Cadastrar Pedido")
                    print("0. Sair")

                    acao = input("Escolha uma opção: ")
                    if acao == '0':
                        break
                    elif acao == '1':
                        cadastrar_cliente_fisico()
                    elif acao == '2':
                        inserir_cliente_juridico()
                    elif acao == '3':
                        editar_ou_excluir_pedido()
                    elif acao == '4':
                        mostrar_produto()
                    elif acao == '5':
                        visualizar_ou_cadastrar_servicos()
                    elif acao == '6':
                        visualizar_ou_editar_estoque()
                    elif acao == '7':
                        cadastrar_pedido()
                    else:
                        print("Opção inválida!")

            elif setor == "Gerente":
                while True:
                    print("\nMenu Gerente:")
                    print("1. Cadastrar Fornecedores")
                    print("2. Visualizar Estoque")
                    print("3. Editar Estoque")
                    print("4. Ver Status dos Serviços")
                    print("5. Relatório de Vendas")
                    print("6. Ver Status das Finanças")
                    print("7. Ver Todos os Funcionários")
                    print("0. Sair")

                    acao = input("Escolha uma opção: ")
                    if acao == '0':
                        break
                    elif acao == '1':
                        cadastrar_fornecedor()
                    elif acao == '2':
                        visualizar_estoque()
                    elif acao == '3':
                        editar_estoque()
                    elif acao == '4':
                        ver_status_servicos()
                    elif acao == '5':
                        relatorio_vendas()
                    elif acao == '6':
                        ver_status_financas()
                    elif acao == '7':
                        ver_todos_os_funcionarios()
                    else:
                        print("Opção inválida!")

            elif setor == "RH":
                while True:
                    print("\nMenu RH:")
                    print("1. Finanças (administrar o salário dos funcionários)")
                    print("2. Relatório de vendas")
                    print("3. Exibir funcionários")
                    print("4. Editar Funcionários")
                    print("5. Serviços (ver status do serviço)")
                    print("6. Cadastrar Funcionário")
                    print("0. Sair")

                    acao = input("Escolha uma opção: ")
                    if acao == '0':
                        break
                    elif acao == '1':
                        administrar_salario_funcionarios()
                    elif acao == '2':
                        ver_relatorio_completo_vendas()
                    elif acao == '3':
                        exibir_funcionarios()
                    elif acao == '4':
                        cadastrar_gerente()
                    elif acao == '5':
                        pass
                    elif acao == '6':
                        cadastrar_funcionario_admin()
                    else:
                        print("Opção inválida!")

            elif setor == "Admin":
                while True:
                    print("\nMenu Admin:")
                    print("1. Cadastrar Funcionário")
                    print("2. Cadastrar Gerente(Promover/demitir)")
                    print("3. Ver Todos os Funcionários")
                    print("4. Ver Relatório Completo de Vendas")
                    print("5. Gerenciar Finanças")
                    print("0. Sair")

                    acao = input("Escolha uma opção: ")
                    if acao == '0':
                        break
                    elif acao == '1':
                        cadastrar_funcionario_admin()
                    elif acao == '2':
                        cadastrar_gerente()
                    elif acao == '3':
                        ver_todos_os_funcionarios()
                    elif acao == '4':
                        ver_relatorio_completo_vendas()
                    elif acao == '5':
                        gerenciar_financas()
                    else:
                        print("Opção inválida!")

        else:
            print("Login falhou! Tente novamente.")

if __name__ == "__main__":
    menu()
