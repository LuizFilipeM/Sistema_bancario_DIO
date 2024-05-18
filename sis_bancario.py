"""
REGRAS DE NEGOCIO
Implementar apenas as 3 operações básicas (sacar, depositar e ver extrato)
*Depositar: Não é exigido verificao de usuário.
*Sacar: máximo de 3 saques por dia, máximo de 500.00 por saque, não possui cheque especial.
*Extrato: Exibir um extrato da conta e o saldo no final, caso não tenha sido efetuado transações exibir
        "Não foram realizadas movimentações."
"""

saldo = 1000
limite = 500
numero_de_saques = 0
LIMITE_SAQUES = 3
extrato = ""

menu = """
########## MENU ##########
0 - Realizar saque;
1 - Realizar depósito;
2 - Ver extrato;
3 - Sair.
"""
opcao = int(input(menu))

while(True):
    #SAQUE
    if opcao == 0:
        valor = float(input("Qual o valor do saque desejado?\n"))
        if valor > limite:
            print("Valor de saque excede o limite po saque")
            
        elif valor > saldo:
            print("Saldo insuficiente.")
            
        elif numero_de_saques > LIMITE_SAQUES:
            print("Número de saques diários excedido.")

        elif valor < 0:
            print("Valor de saque não é aceito.")    

        else:
            saldo -= valor
            numero_de_saques += 1
            extrato += f"Saque realizado no no valor de R$ {valor:.2f}\n"

    #Depósito
    if opcao == 1:
        valor = float(input("Qual valor do depósito?\n"))
        if valor < 0:
            print("Valor não aceito para depósito.")

        else:    
            saldo += valor
            extrato += f"Depósito realizado no valor de R$ {valor:.2f}\n"

    #EXTRATO
    if opcao == 2:
        if extrato == "":
            print("Não há movimentações até o momento.")
        else:
            print("#####EXTRATO#####\n")
            print(extrato)
            print(f"Saldo: {saldo}")

    #SAIR
    if opcao == 3:
        print("OBRIGADO POR USAR NOSSO SISTEMA!\n")
        break
    
    opcao = int(input(menu))