from abc import ABC, abstractclassmethod

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
            print("---------- Operação falou: Saldo insuficiente para saque ----------")
        
        elif valor_saque > 0:
            self.saldo -= valor_saque
            print("---------- Saque realizado com sucesso ----------")
            return True
        
        else:
            print("---------- Operaçãoe falou: valor inválido ----------")
        return False
        

    def depositar(self, valor_deposito):
        if valor_deposito > 0:
            self.saldo += valor_deposito
            print("---------- Depósito realizado com sucesso ----------")
            return True
        else:
            print("---------- Operação falhou: Valor inválido ----------")
            return False
        
class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite_valor = 500, limite_saque = 3):
        super().__init__(numero, cliente)
        self.limite = limite_valor
        self.limite_saque = limite_saque

    def sacar(self, valor_saque):
        qtd_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        valor_sacado = 0
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                valor_sacado += transacao["valor"]
        
        print(valor_sacado)
        print(qtd_saque)

        excedeu_limite_saque = qtd_saque > self.limite_saque
        excedeu_valor = valor_sacado > self.limite
        
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
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = float(valor)

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo":transacao.__class__.__name__,
                "valor":transacao.valor
            }
        )

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.list = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.list.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

        
def menu():
    menu = """\n
    ================ MENU ================
    [d]Depositar
    [s]Sacar
    [e]Extrato
    [nc]Nova conta
    [lc]Listar contas
    [nu]Novo usuário
    [q]Sair
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

def Depositar(clientes):
    cpf = int(input("Digite o CPF"))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Erro: cliente não encontrado")
        
    else:
        valor = float(input("Digite o valor: "))
        transacao = Deposito(valor)
        conta = recuperar_conta_cliente(cliente)

        if not conta: 
            return
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nErro: Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = int(input("Informe o CPF do cliente: "))

    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nErro: Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(clientes[0])
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            if transacao["tipo"] == "Deposito":
                extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:.2f}"
            if transacao["tipo"] == "Saque":
                extrato += f"\n{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print("------------------------------------------")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = int(input("Informe o CPF (somente número): "))
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nErro: Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nErro: Cliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = Conta_corrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(conta)

  
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            Depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\nErro: Operação inválida, por favor selecione novamente a operação desejada.")


main()
