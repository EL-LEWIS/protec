import re
from protec_4 import validar_email, validar_cpf, validar_cnpj

def test_validar_email():
    # Testes com emails válidos
    assert validar_email("teste@exemplo.com") == True
    assert validar_email("nome.sobrenome@dominio.co") == True
    assert validar_email("usuario+123@dominio.org") == True
    
    # Testes com emails inválidos
    assert validar_email("email_invalido.com") == False
    assert validar_email("email@com") == False
    assert validar_email("@sem_usuario.com") == False

def test_validar_cpf():
    # Testes com CPFs válidos
    assert validar_cpf("123.456.789-09") == True
    assert validar_cpf("98765432100") == True

    # Testes com CPFs inválidos
    assert validar_cpf("123.456.789-00") == False
    assert validar_cpf("111.111.111-11") == False

def test_validar_cnpj():
    # Testes com CNPJs válidos
    assert validar_cnpj("12.345.678/0001-95") == True
    assert validar_cnpj("12345678000195") == True
    
    # Testes com CNPJs inválidos
    assert validar_cnpj("12.345.678/0001-00") == False
    assert validar_cnpj("11111111000111") == False
