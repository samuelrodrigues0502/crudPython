from app.controllers.funcionario_controller import FuncionarioController
from app.bd.manutencaoBD import zerarBD

def menu():
    print("\n==================== MENU FUNCIONÁRIOS ====================")
    print("1. Cadastrar funcionário")
    print("2. Listar funcionários")
    print("3. Buscar funcionário por ID")
    print("4. Atualizar funcionário")
    print("5. Remover funcionário")
    print("6. Zerar banco (apagar todos os dados)")
    print("0. Sair")
    print("===========================================================\n")

def intValid(inteiro):
    while True:
        valor = input(inteiro).strip()
        if valor.isdigit():
            return int(valor)
        print("Valor inválido. Tente novamente.")

def cadastrar():
    print("\n=== CADASTRAR FUNCIONÁRIO ===")
    nome = input("Nome: ").strip()
    cargo = input("Cargo: ").strip()
    salario_str = input("Salário (ex: 4500.50): ").strip()
    departamento = input("Departamento (opcional): ").strip()
    data_admissao = input("Data de Admissão (YYYY-MM-DD): ").strip()
    
    departamento = departamento if departamento else None
    
    try:
        salario = float(salario_str)
    except ValueError:
        print("Salário inválido. Deve ser um número.")
        return
    
    try:
        func_id = FuncionarioController.criar(nome, cargo, salario, departamento, data_admissao)
        print(f"Funcionário cadastrado com ID: {func_id}")
    except ValueError as e:
        print(f"Erro ao cadastrar funcionário: {e}")
    
def listar():
    print("\n=== LISTA DE FUNCIONÁRIOS ===")
    funcionarios = FuncionarioController.listar()
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return
    for func in funcionarios:
        print(f"ID: {func.id} \nNome: {func.nome} \nCargo: {func.cargo} \nSalário: {func.salario} \nDepartamento: {func.departamento} \nData Admissão: {func.data_admissao} \nAtivo: {'Sim' if func.ativo else 'Não'}")
        print("-" * 40)
def buscar_por_id():
    print("\n=== BUSCAR FUNCIONÁRIO POR ID ===")
    func_id = intValid("ID do funcionário: ")
    func = FuncionarioController.obter(func_id)
    if not func:
        print("Funcionário não encontrado.")
        return
    print("Funcionário encontrado:")
    print(f"\nID: {func.id} \nNome: {func.nome} \nCargo: {func.cargo} \nSalário: {func.salario} \nDepartamento: {func.departamento} \nData Admissão: {func.data_admissao} \nAtivo: {'Sim' if func.ativo else 'Não'}")
   
def atualizar():
    print("\n=== ATUALIZAR FUNCIONÁRIO ===")
    func_id = intValid("ID do funcionário a atualizar: ")
    existe = FuncionarioController.obter(func_id)
    if not existe:
        print("Funcionário não encontrado.")
        return
    print(f"Atual funcionário: {existe}")
    
    nome = input("Novo Nome: ").strip()
    cargo = input("Novo Cargo: ").strip()
    salario_str = input("Novo Salário (ex: 4500.50): ").strip()
    departamento = input("Novo Departamento (opcional): ").strip()
    data_admissao = input("Nova Data de Admissão (YYYY-MM-DD): ").strip()
    ativo = intValid("Ativo (1 para Sim, 0 para Não): ")
    
    departamento = departamento if departamento else None
    
    try:
        salario = float(salario_str)
    except ValueError:
        print("Salário inválido. Deve ser um número.")
        return
    try:
        ativoInt = int(ativo)
    except ValueError:
        print("Valor de ativo inválido.")
        return
    
    try:
        sucesso = FuncionarioController.atualizar(func_id, nome, cargo, salario, departamento, data_admissao, ativo)
        if sucesso:
            print("Funcionário atualizado com sucesso.")
        else:
            print("Funcionário não encontrado.")
    except ValueError as e:
        print(f"Erro ao atualizar funcionário: {e}")
def remover():
    print("\n=== REMOVER FUNCIONÁRIO ===")
    func_id = intValid("ID do funcionário a remover: ")
    temCerteza = input(f"Tem certeza que deseja remover o funcionário com ID {func_id}? (s/n): ").strip().lower()
    if temCerteza != 's':
        print("Remoção cancelada.")
        return
    sucesso = FuncionarioController.remover(func_id)
    if sucesso:
        print("Funcionário removido com sucesso.")
    else:
        print("Funcionário não encontrado.")

    
def executar_menu():
    while True:
        menu()
        opc = input("Digite a opção desejada: ").strip()
        if opc == "1":
            cadastrar()
        elif opc == '2':
            listar()
        elif opc == '3':
            buscar_por_id()
        elif opc == '4':
            atualizar()
        elif opc == '5':
            remover()
        elif opc == '6':
            zerarBD()
        elif opc == '0':
            print('Encerrando...Adeus...Até logo...')
            break
        else:
            print("Opção Inválida.")
            
    