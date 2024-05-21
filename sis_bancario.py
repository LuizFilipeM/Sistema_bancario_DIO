saldo = 1000
limite = 500
numero_de_saques = 0
LIMITE_SAQUES = 3
extrato = ""

def deposito(saldo, valor, extrato,/):
    if valor < 0:
        print("Valor não aceito para depósito.")

    else:    
        saldo += valor
        extrato += f"Depósito realizado no valor de R$ {valor:.2f}\n"

    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_de_saques, limite_saques):
    if valor > limite:
        print("Valor de saque excede o limite por saque.")
        
    elif valor > saldo:
        print("Saldo insuficiente.")
        
    elif numero_de_saques >= limite_saques:
        print("Número de saques diários excedido.")

    elif valor <= 0:
        print("Valor de saque não é aceito.")    

    else:
        saldo -= valor
        numero_de_saques += 1
        extrato += f"Saque realizado no no valor de R$ {valor:.2f}\n"
        print("Saque realizado com sucesso!\n")

    return saldo, extrato, numero_de_saques

def exibe_extrato(saldo,/,*, extrato):
    if extrato == "":
        print("Não há movimentações até o momento.\n")
    else:
        print("#####EXTRATO#####\n")
        print(extrato)
        print(f"Saldo: {saldo}")

    return

def cadastra_usuario(usuarios):
    cpf = input("Digite seu CPF (apenas números): ")
    for i in usuarios:
        if cpf in i:
            print("Usuário já cadastrado.")
            return
    nome = input("Digite o nome completo:\n")
    data_nasc = input("Digite a data denascimento no formato dd/mm/aaaa:\n")
    endereco = input("Digite seu endereço no formato: logradouro, nmr - bairro - cidade/sigla do estado\n")
    usuarios.append([cpf, nome, data_nasc, endereco])

def cria_conta_corr(user, usuarios, contas):
    for i in usuarios:
        if user in i:
            numero_conta = len(contas) + 1
            contas.append(["0001", numero_conta, user[0][0]])        
            return

def main():
    usuarios = [["123","luiz","13/03/2003", "sao joao del rei"]]
    contas = []

    menu = """
        ########## MENU ##########
        0 - Realizar saque;
        1 - Realizar depósito;
        2 - Ver extrato;
        3 - Cadastrar Usuário;
        4 - Criar conta corrente;
        5 - Sair.
    """
    opcao = int(input(menu))

    while(True):
        #SAQUE
        if opcao == 0:
            valor = float(input("Qual valor do saque?\n"))
            retorno = saque(saldo = saldo, valor = valor, extrato = extrato, limite = limite, numero_de_saques = numero_de_saques, limite_saques = LIMITE_SAQUES)
            saldo = retorno[0]
            extrato = retorno[1]
            numero_de_saques = retorno[2]
            
        #DEPOSITO
        if opcao == 1:
            valor = float(input("Qual valor do deposito?\n"))
            retorno = deposito(saldo, valor, extrato)
            saldo = retorno[0]
            extrato = retorno[1]

        #EXTRATO
        if opcao == 2:
            exibe_extrato(saldo, extrato = extrato)

        #cadastrar usuario
        if opcao == 3:
            cadastra_usuario(usuarios)
            

        #criar conta
        if opcao == 4:
            user = input("Digite o cpf: ")
            cria_conta_corr(user, usuarios, contas)
            

        #SAIR
        if opcao == 5:
            print("OBRIGADO POR USAR NOSSO SISTEMA!\n")
            break
        
        opcao = int(input(menu))


main()