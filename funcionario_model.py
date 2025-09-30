from dataclasses import dataclass
from typing import Optional, List
from app.bd.connection import get_connection

@dataclass
class Funcionario:
    id: Optional[int]
    nome: str
    cargo: str
    salario: float
    departamento: Optional[str]
    data_admissao: str
    ativo: int = 1

class FuncionarioModel:
    @staticmethod
    def criar(func: Funcionario) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO funcionario (nome, cargo, salario, departamento, data_admissao, ativo)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (func.nome, func.cargo, func.salario, func.departamento, func.data_admissao, func.ativo)
            )
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def listar() -> List[Funcionario]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nome, cargo, salario, departamento, data_admissao, ativo
                FROM funcionario
                ORDER BY id
                """
            )
            rows = cur.fetchall()
            return [
                Funcionario(
                    id=row["id"],
                    nome=row["nome"],
                    cargo=row["cargo"],
                    salario=row["salario"],
                    departamento=row["departamento"],
                    data_admissao=row["data_admissao"],
                    ativo=row["ativo"],
                )
                for row in rows
            ]

    @staticmethod
    def obter_por_id(func_id: int) -> Optional[Funcionario]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nome, cargo, salario, departamento, data_admissao, ativo
                FROM funcionario
                WHERE id = ?
                """,
                (func_id,)
            )
            row = cur.fetchone()
            if row:
                return Funcionario(
                    id=row["id"],
                    nome=row["nome"],
                    cargo=row["cargo"],
                    salario=row["salario"],
                    departamento=row["departamento"],
                    data_admissao=row["data_admissao"],
                    ativo=row["ativo"],
                )
            return None

    @staticmethod
    def atualizar(func: Funcionario) -> bool:
        if func.id is None:
            return False
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE funcionario
                SET nome = ?, cargo = ?, salario = ?, departamento = ?, data_admissao = ?, ativo = ?
                WHERE id = ?
                """,
                (func.nome, func.cargo, func.salario, func.departamento, func.data_admissao, func.ativo, func.id)
            )
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def remover(func_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM funcionario WHERE id = ?", (func_id,))
            conn.commit()
            return cur.rowcount > 0