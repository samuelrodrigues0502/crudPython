from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.departamento_controller import DepartamentoController
from app.bd.manutencaoBD import zerarBD

def menuInicial():
    print("\n==================== MENU RH MINI ====================")
    print("1. Gerenciar departamentos")
    print("2. Gerenciar funcionários") 
    print("3. Zerar banco de dados (apaga TODOS os dados)")
    print("0. Sair")
    print("=====================================================\n")
    
def menuFuncionarios():
    print("\n Cadastro de Funcionários")
    print("1. Cadastrar funcionário")
    print("2. Listar funcionários")
    print("3. Buscar funcionário por ID")
    print("4. Atualizar funcionário")
    print("5. Remover funcionário")
    print("0. Voltar")
    print("=====================================================\n")
    
def menuDepartamentos():
    print("\n Cadastro de Departamentos")
    print("1. Cadastrar departamento")
    print("2. Listar departamentos")
    print("3. Remover departamento")
    print("4. Atualizar departamento")
    print("0. Voltar")
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

def cadastrar_funcionario():
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

def listar_funcionarios():
    print("\n=== LISTA DE FUNCIONÁRIOS ===")
    funcionarios = FuncionarioController.listar()
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return
    for func in funcionarios:
        dep_nome = func.departamento_nome if func.departamento_nome else "(sem)"
        print(f"ID: {func.id} \nNome: {func.nome} \nCargo: {func.cargo} \nSalário: {func.salario} \nDepartamento: {dep_nome} \nData Admissão: {func.data_admissao} \nAtivo: {'Sim' if func.ativo else 'Não'}")
        print("-" * 40)
def buscar_por_id_funcionario():
    print("\n=== BUSCAR FUNCIONÁRIO POR ID ===")
    func_id = intValid("ID do funcionário: ")
    func = FuncionarioController.obter(func_id)
    if not func:
        print("Funcionário não encontrado.")
        return
    print("Funcionário encontrado:")
    dep_nome = func.departamento_nome if func.departamento_nome else "(sem)"
    print(f"\nID: {func.id} \nNome: {func.nome} \nCargo: {func.cargo} \nSalário: {func.salario} \nDepartamento: {dep_nome} \nData Admissão: {func.data_admissao} \nAtivo: {'Sim' if func.ativo else 'Não'}")

def atualizar_funcionario():
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
        sucesso = FuncionarioController.atualizar(func_id, nome, cargo, salario, departamento_id, data_admissao, ativoInt)
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
    
def atualizar_departamento():
    print("\n=== ATUALIZAR Departamento ===")
    depart_id = intValid("ID do departamneto a atualizar: ")
    existe = DepartamentoController.obter(depart_id)
    if not existe:
        print("Departamento não encontrado.")
        return
    print(f"Atual Departamento: {existe}")
    
    nome = input("Novo Nome do departamento: ").strip()
    descricao = input("Nova Descrição (opcional): ").strip()
    
    try:
        sucesso = DepartamentoController.atualizar(depart_id, nome, descricao if descricao else None)
    except ValueError as e:
        print(f"Erro ao atualizar departamento: {e}")
    
def remover_funcionario():
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
        menuInicial()
        opc = input("Digite a opção desejada: ").strip()
        if opc == "2":
            while True:
                menuFuncionarios()
                opc_func = input("Digite a opção desejada: ").strip()
                if opc_func == "1":
                    cadastrar_funcionario()
                elif opc_func == '2':
                    listar_funcionarios()
                elif opc_func == '3':
                    buscar_por_id_funcionario()
                elif opc_func == '4':
                    atualizar_funcionario()
                elif opc_func == '5':
                    remover_funcionario()
                elif opc_func == '0':
                    break
                else:
                    print("Opção Inválida.")
        elif opc == "1":
            while True:
                menuDepartamentos()
                opc_dep = input("Digite a opção desejada: ").strip()
                if opc_dep == "1":
                    cadastrar_departamento()
                elif opc_dep == '2':
                    listar_departamentos()
                elif opc_dep == '3':
                    remover_departamento()
                elif opc_dep == '4':
                    atualizar_departamento()
                elif opc_dep == '0':
                    break
                else:
                    print("Opção Inválida.")
        elif opc == "3":
            zerarBD()
        elif opc == '0':
            print('Encerrando...Adeus...Até logo...')
            break
        else:
            print("Opção Inválida.")
         
    