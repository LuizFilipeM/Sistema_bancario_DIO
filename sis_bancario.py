from abc import ABC, abstractclassmethod
import os
from datetime import datetime
import pytz

class Conta:
    def __init__(self,cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @property
    def get_saldo(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def __str__(self):
        return (f"Número: {self.numero}\n"
                f"Saldo: {self.saldo}")

    def sacar(self, valor_saque):
        saldo = self.saldo
        execedeu_saldo = valor_saque > saldo
        if execedeu_saldo:
            print("---------- Operação falhou: Saldo insuficiente para saque ----------")
        
        elif not self.historico.transacoes_dia():
            print("---------- Operação falhou: limite de transacções diárias ----------")
            return False

        elif valor_saque > 0:
            self.saldo -= valor_saque
            return True
        
        else:
            print("---------- Operação falhou: valor inválido ----------")
        return False
        
    def depositar(self, valor_deposito):
        if not self.historico.transacoes_dia():
            print("---------- Operação falhou: limite de transacções diárias ----------")
            return False
        
        if valor_deposito > 0:
            self.saldo += valor_deposito
            return True
        
        else:
            print("---------- Operação falhou: Valor inválido ----------")
            return False
        
class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite_valor = 500, limite_saque = 5):
        super().__init__(numero, cliente)
        self.limite = limite_valor
        self.limite_saque = limite_saque

    def sacar(self, valor_saque):
        qtd_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite_saque = qtd_saque >= self.limite_saque
        excedeu_valor = valor_saque > self.limite
        
        if excedeu_valor:
            print("\n--- Operação falhou! O valor do saque excede o limite. ---")

        elif excedeu_limite_saque:
            print("\n--- Operação falhou! Número máximo de saques excedido. ---")

        else:
            return super().sacar(valor_saque)

        return False

class Transacao(ABC):

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = float(valor)
        data1 = datetime.now(pytz.timezone("America/Sao_Paulo"))
        self.data = data1.strftime("%d/%m/%Y %H:%M:%S")

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
        else:
            return False

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = float(valor)
        data1 = datetime.now(pytz.timezone("America/Sao_Paulo"))
        self.data = data1.strftime("%d/%m/%Y %H:%M:%S")
        
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
        else: return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo":transacao.__class__.__name__,
                "valor":transacao.valor,
                "data": transacao.data
            }
        )

    def transacoes_dia(self):
        qtd_transacoes = len([movimentacao for movimentacao in self.transacoes if movimentacao["data"][:2] == datetime.now().strftime("%d")])
        print(self.transacoes)
        print(f"Numero de trasnacoes: {qtd_transacoes}")
        return qtd_transacoes <= 10

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.list = []

    def realizar_transacao(self, conta, transacao):
        if transacao.registrar(conta) == False:
            return 0

    def adicionar_conta(self, conta):
        self.list.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class ContaIterador:
    def __init__(self, contas, op = None):
        self.contas = contas
        self.op = op
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self.index]
            self.index +=1
            return conta
        except IndexError:
            raise StopIteration
    
def log_transacao(func):
    def envelope(*args, **kwargs):
        if func(*args, **kwargs) == 0: return
        print(f'\nOperação realizada com sucesso: {func.__name__}')
        return func    
    return envelope

def menu():
    menu = """
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc]Nova conta
    [lc]Listar contas
    [nu]Novo usuário
    [lt]Listar transacoes com filtro de tipo
    [l] Limpar terminal
    [q] Sair
    => """
    return input(menu)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.list:
        print("\nErro: Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.list[0]

@log_transacao
def Depositar(clientes, data_atual):
    cpf = int(input("Digite o CPF: "))
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Erro: cliente não encontrado")
        return 0
        
    else:
        valor = float(input("Digite o valor: "))
        transacao = Deposito(valor)
        conta_corrente = recuperar_conta_cliente(cliente)
            
        if not conta_corrente: 
            return 0

        return cliente.realizar_transacao(conta_corrente, transacao)

@log_transacao
def sacar(clientes, data_atual):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nErro: Cliente não encontrado!")
        return 0

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta_corrente = recuperar_conta_cliente(cliente)

    if not conta_corrente:
        return 0

    if cliente.realizar_transacao(conta_corrente, transacao) == False: return 0

@log_transacao
def exibir_extrato(clientes):
    cpf = int(input("Informe o CPF do cliente: "))

    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nErro: Cliente não encontrado!")
        return 0

    conta = recuperar_conta_cliente(clientes[0])
    if not conta:
        return 0

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        #AS ESTRUTURAS CONDICIONAIS ESTÃO SENDO UTILIZADAS APENAS PARA FORMATAR A IMPRESSÃO
        #DO EXTRATO, MANTENDO OS VALORES NA MESMA COLUNA
        for transacao in transacoes:
            if transacao["tipo"] == "Deposito":
                extrato += f"\n{transacao['data']}: {transacao['tipo']}:\tR$ {transacao['valor']:.2f}"
            if transacao["tipo"] == "Saque":
                extrato += f"\n{transacao['data']}: {transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print("------------------------------------------")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao
def criar_cliente(clientes):
    cpf = int(input("Informe o CPF (somente número): "))
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nErro: Já existe cliente com esse CPF!")
        return 0

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

@log_transacao
def criar_conta(numero_conta, clientes, contas_corrente):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nErro: Cliente não encontrado, fluxo de criação de conta encerrado!")
        return 0

    conta = Conta_corrente.nova_conta(cliente, numero_conta)
    contas_corrente.append(conta)
    cliente.adicionar_conta(conta)

def listar_contas(contas_corrente):
    for conta in ContaIterador(contas_corrente):
        print (conta)
        print("_" * 50)
    
def gerador_transacoes(cliente, op):
    historico = cliente.list[0].historico
    
    for i in historico.transacoes:
        if op == '0':
            yield i
        elif i["tipo"] == op:
            yield i
        
def listar_transacoes(cliente, op = 0):
    for i in gerador_transacoes(cliente, op):
        print(f"\n{i['data']}: {i['tipo']}:\tR$ {i['valor']:.2f}")

def main():
    data_atual = datetime.now().strftime("%d")
    clientes = []
    contas_corrente = []

    while True:
        opcao = menu()

        if opcao == "d":
            Depositar(clientes, data_atual)

        elif opcao == "s":
            sacar(clientes, data_atual)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas_corrente) + 1
            criar_conta(numero_conta, clientes, contas_corrente)

        elif opcao == "lc":
            listar_contas(contas_corrente)
        
        elif opcao == "lt":
            op = input("""
    Para saques digite 'Saque'
    Para depósitos digite 'Deposito'
    Para todas as transacoes Digite '0'
                       """)
            listar_transacoes(clientes[0],op)

        elif opcao == "l":
            os.system("cls")

        elif opcao == "q":
            break

        else:
            print("\nErro: Operação inválida, por favor selecione novamente a operação desejada.")
        
main()
