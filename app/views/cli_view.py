from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.departamento_controller import DepartamentoController
from app.bd.manutencaoBD import zerarBD

def menu():
    print("\n==================== MENU RH MINI ====================")
    print("1. Cadastrar funcionário")
    print("2. Listar funcionários")
    print("3. Buscar funcionário por ID")
    print("4. Atualizar funcionário")
    print("5. Remover funcionário")
    print("6. Cadastrar departamento")
    print("7. Listar departamentos")
    print("8. Remover departamento")
    print("9. Zerar banco (apagar TODOS os dados)")
    print("0. Sair")
    print("=====================================================\n")

def intValid(inteiro):
    while True:
        valor = input(inteiro).strip()
        if valor.isdigit():
            return int(valor)
        print("Valor inválido. Tente novamente.")

def _escolher_departamento_id() -> int | None:
    deps = DepartamentoController.listar()
    if not deps:
        print("Nenhum departamento cadastrado. Você pode deixar vazio ou criar um agora em 'Gerenciar departamentos'.")
        return None
    print("\nDepartamentos disponíveis:")
    for d in deps:
        print(f"  {d.id} - {d.nome}")
    valor = input("Informe o ID do departamento (ou vazio para nenhum): ").strip()
    if not valor:
        return None
    if valor.isdigit():
        return int(valor)
    print("ID inválido, ignorando departamento.")
    return None

def cadastrar():
    print("\n=== CADASTRAR FUNCIONÁRIO ===")
    nome = input("Nome: ").strip()
    cargo = input("Cargo: ").strip()
    salario_str = input("Salário (ex: 4500.50): ").strip()
    data_admissao = input("Data de Admissão (YYYY-MM-DD): ").strip()
    departamento_id = _escolher_departamento_id()
    try:
        salario = float(salario_str)
    except ValueError:
        print("Salário inválido. Deve ser um número.")
        return
    try:
        func_id = FuncionarioController.criar(nome, cargo, salario, departamento_id, data_admissao)
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
        dep_nome = func.departamento_nome if func.departamento_nome else "(sem)"
        print(f"ID: {func.id} \nNome: {func.nome} \nCargo: {func.cargo} \nSalário: {func.salario} \nDepartamento: {dep_nome} \nData Admissão: {func.data_admissao} \nAtivo: {'Sim' if func.ativo else 'Não'}")
        print("-" * 40)
def buscar_por_id():
    print("\n=== BUSCAR FUNCIONÁRIO POR ID ===")
    func_id = intValid("ID do funcionário: ")
    func = FuncionarioController.obter(func_id)
    if not func:
        print("Funcionário não encontrado.")
        return
    print("Funcionário encontrado:")
    dep_nome = func.departamento_nome if func.departamento_nome else "(sem)"
    print(f"\nID: {func.id} \nNome: {func.nome} \nCargo: {func.cargo} \nSalário: {func.salario} \nDepartamento: {dep_nome} \nData Admissão: {func.data_admissao} \nAtivo: {'Sim' if func.ativo else 'Não'}")
   
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
    print("Alterar departamento:")
    departamento_id = _escolher_departamento_id()
    data_admissao = input("Nova Data de Admissão (YYYY-MM-DD): ").strip()
    ativo = intValid("Ativo (1 para Sim, 0 para Não): ")
    
    
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
        sucesso = FuncionarioController.atualizar(func_id, nome, cargo, salario, departamento_id, data_admissao, ativo)
        if sucesso:
            print("Funcionário atualizado com sucesso.")
        else:
            print("Funcionário não encontrado.")
    except ValueError as e:
        print(f"Erro ao atualizar funcionário: {e}")
        
def cadastrar_departamento():
    print("\n=== CADASTRAR DEPARTAMENTO ===")
    nome = input("Nome do departamento: ").strip()
    descricao = input("Descrição (opcional): ").strip()
    descricao = descricao if descricao else None
    try:
        dep_id = DepartamentoController.criar(nome, descricao)
        print(f"Departamento criado com ID {dep_id}")
    except ValueError as e:
        print(f"Erro: {e}")

def listar_departamentos():
    print("\n=== LISTA DE DEPARTAMENTOS ===")
    deps = DepartamentoController.listar()
    if not deps:
        print("Nenhum departamento cadastrado.")
        return
    for d in deps:
        print(f"ID: {d.id} | Nome: {d.nome} | Desc: {d.descricao or ''}")

def remover_departamento():
    print("\n=== REMOVER DEPARTAMENTO ===")
    dep_id_str = input("ID do departamento a remover: ").strip()
    if not dep_id_str.isdigit():
        print("ID inválido.")
        return
    ok = DepartamentoController.remover(int(dep_id_str))
    print("Removido." if ok else "Não encontrado (ou pode estar vinculado via FK).")

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
            cadastrar_departamento()
        elif opc == '7':
            listar_departamentos()
        elif opc == '8':
            remover_departamento()
        elif opc == '9':
            zerarBD()
        elif opc == '0':
            print('Encerrando...Adeus...Até logo...')
            break
        else:
            print("Opção Inválida.")
            
    