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
        if DepartamentoModel.obter_por_id(dep_id) is None:
            raise ValueError("Departamento não encontrado")
        if DepartamentoModel.existe_funcionario_para_departamento(dep_id):
            raise ValueError("Não é possível remover: existem funcionários vinculados.")
        
        return DepartamentoModel.remover(dep_id)
    @staticmethod
    def existe_funcionario_para_departamento(dep_id: int) -> bool:
        return DepartamentoModel.existe_funcionario_para_departamento(dep_id)
    
    @staticmethod
    def atualizar(dep_id: int, nome: str, descricao: str | None = None) -> bool:
        dep_existente = DepartamentoModel.obter_por_id(dep_id)
        if not dep_existente:
            raise ValueError("Departamento não encontrado")
        nome_limpo = (nome or "").strip()
        if not nome_limpo:
            raise ValueError("nome do departamento obrigatório")
        dep_atualizado = Departamento(id=dep_id, nome=nome_limpo, descricao=descricao.strip() if descricao else None)
    
        return DepartamentoModel.atualizar(dep_atualizado)