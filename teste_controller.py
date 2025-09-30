from app.controllers.funcionario_controller import FuncionarioController

# Criar
id1 = FuncionarioController.criar("Ana", "Dev", 5000, "TI", "2025-09-30")
print("Criado:", id1)

# Atualizar
ok = FuncionarioController.atualizar(
    func_id=id1,
    nome="Ana Paula",
    cargo="Dev Pleno",
    salario=6200,
    departamento="TI",
    data_admissao="2025-09-30",
    ativo=1
)
print("Atualização:", ok)

# Obter para conferir
print("Após atualizar:", FuncionarioController.obter(id1))

# Remover
rem = FuncionarioController.remover(id1)
print("Removido?", rem)

# Conferir remoção
print("Após remover:", FuncionarioController.obter(id1))

# Tentar atualizar um inexistente
fail_update = FuncionarioController.atualizar(
    func_id=9999,
    nome="X",
    cargo="Y",
    salario=1000,
    departamento=None,
    data_admissao="2025-09-30",
    ativo=1
)
print("Atualizar inexistente:", fail_update)

# Testar validação
try:
    FuncionarioController.criar("", "Cargo", 1000, None, "2025-09-30")
except ValueError as e:
    print("Erro esperado (nome vazio):", e)