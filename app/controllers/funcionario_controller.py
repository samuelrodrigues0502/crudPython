from datetime import datetime
from typing import List, Optional
from app.models.funcionario_model import FuncionarioModel, Funcionario

class FuncionarioController:
    @staticmethod
    def _validar(nome: str, cargo: str, salario: float, data_admissao: str, ativo: int = 1):
        if not nome or not nome.strip():
            raise ValueError("nome obrigatório")
        if not cargo or not cargo.strip():
            raise ValueError("cargo obrigatório")
        if salario <= 0:
            raise ValueError("salario deve ser > 0")
        try:
            datetime.strptime(data_admissao, "%Y-%m-%d")
        except ValueError:
            raise ValueError("data_admissao deve estar no formato YYYY-MM-DD")
        if ativo not in (0, 1):
            raise ValueError("ativo deve ser 0 ou 1")

    @staticmethod
    def criar(nome: str, cargo: str, salario: float, departamento: str | None, data_admissao: str) -> int:
        # Valida dados
        FuncionarioController._validar(nome, cargo, salario, data_admissao, 1)
        
        func = Funcionario(
            id=None,
            nome=nome.strip(),
            cargo=cargo.strip(),
            salario=float(salario),
            departamento=departamento.strip() if departamento else None,
            data_admissao=data_admissao,
            ativo=1
        )
        return FuncionarioModel.criar(func)

    @staticmethod
    def listar() -> List[Funcionario]:
        return FuncionarioModel.listar()

    @staticmethod
    def obter(func_id: int) -> Optional[Funcionario]:
        return FuncionarioModel.obter_por_id(func_id)

    @staticmethod
    def atualizar(func_id: int, nome: str, cargo: str, salario: float, departamento: str | None, data_admissao: str, ativo: int = 1) -> bool:
        existe = FuncionarioModel.obter_por_id(func_id)
        if not existe:
            return False
        # Valida novos dados
        FuncionarioController._validar(nome, cargo, salario, data_admissao, ativo)
        funcionario_atualizado = Funcionario(
            id=func_id,
            nome=nome.strip(),
            cargo=cargo.strip(),
            salario=float(salario),
            departamento=departamento.strip() if departamento else None,
            data_admissao=data_admissao,
            ativo=ativo
        )
        return FuncionarioModel.atualizar(funcionario_atualizado)

    @staticmethod
    def remover(func_id: int) -> bool:
        existe = FuncionarioModel.obter_por_id(func_id)
        if not existe:
            return False
        return FuncionarioModel.remover(func_id)