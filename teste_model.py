from app.bd.connection import init_db
from app.models.funcionario_model import FuncionarioModel, Funcionario

def separador(titulo):
    print("\n" + "="*20 + " " + titulo + " " + "="*20)

# Garantir que a tabela existe
init_db()

separador("CRIANDO")
novo_id = FuncionarioModel.criar(
    Funcionario(
        id=None,
        nome="João Silva",
        cargo="Desenvolvedor",
        salario=6500.00,
        departamento="TI",
        data_admissao="2025-09-30"
    )
)
print("ID criado:", novo_id)

separador("LISTANDO")
todos = FuncionarioModel.listar()
for f in todos:
    print(f)

separador("OBTER POR ID")
f = FuncionarioModel.obter_por_id(novo_id)
print("Obtido:", f)

separador("ATUALIZANDO")
f.nome = "João Silva Junior"
f.salario = 7000.00
atualizado = FuncionarioModel.atualizar(f)
print("Atualizado?", atualizado)
print("Após atualizar:", FuncionarioModel.obter_por_id(novo_id))

separador("REMOVENDO")
removido = FuncionarioModel.remover(novo_id)
print("Removido?", removido)
print("Após remover:", FuncionarioModel.obter_por_id(novo_id))