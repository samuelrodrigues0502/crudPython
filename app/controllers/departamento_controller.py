from typing import List, Optional
from app.models.departamento_model import DepartamentoModel, Departamento

class DepartamentoController:
    @staticmethod
    def criar(nome: str, descricao: str | None = None) -> int:
        nome_limpo = (nome or "").strip()
        if not nome_limpo:
            raise ValueError("nome do departamento obrigatório")
        dep = Departamento(id=None, nome=nome_limpo, descricao=descricao.strip() if descricao else None)
        return DepartamentoModel.criar(dep)

    @staticmethod
    def listar() -> List[Departamento]:
        return DepartamentoModel.listar()

    @staticmethod
    def obter(dep_id: int) -> Optional[Departamento]:
        return DepartamentoModel.obter_por_id(dep_id)

    @staticmethod
    def remover(dep_id: int) -> bool:
        return DepartamentoModel.remover(dep_id)
