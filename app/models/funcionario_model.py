from dataclasses import dataclass
from typing import Optional, List
from app.bd.connection import get_connection

@dataclass
class Funcionario:
    id: Optional[int]
    nome: str
    cargo: str
    salario: float
    departamento_id: Optional[int]
    data_admissao: str
    ativo: int = 1
    departamento_nome: Optional[str] = None  # preenchido em JOIN

class FuncionarioModel:
    @staticmethod
    def criar(func: Funcionario) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO funcionario (nome, cargo, salario, departamento_id, data_admissao, ativo)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (func.nome, func.cargo, func.salario, func.departamento_id, func.data_admissao, func.ativo)
            )
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def listar() -> List[Funcionario]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT f.id, f.nome, f.cargo, f.salario, f.departamento_id, f.data_admissao, f.ativo,
                       d.nome AS departamento_nome
                FROM funcionario f
                LEFT JOIN departamento d ON d.id = f.departamento_id
                ORDER BY f.id;
                """
            )
            rows = cur.fetchall()
            return [
                Funcionario(
                    id=r["id"],
                    nome=r["nome"],
                    cargo=r["cargo"],
                    salario=r["salario"],
                    departamento_id=r["departamento_id"],
                    data_admissao=r["data_admissao"],
                    ativo=r["ativo"],
                    departamento_nome=r["departamento_nome"],
                )
                for r in rows
            ]

    @staticmethod
    def obter_por_id(func_id: int) -> Optional[Funcionario]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT f.id, f.nome, f.cargo, f.salario, f.departamento_id, f.data_admissao, f.ativo,
                       d.nome AS departamento_nome
                FROM funcionario f
                LEFT JOIN departamento d ON d.id = f.departamento_id
                WHERE f.id = ?
                """,
                (func_id,)
            )
            r = cur.fetchone()
            if r:
                return Funcionario(
                    id=r["id"],
                    nome=r["nome"],
                    cargo=r["cargo"],
                    salario=r["salario"],
                    departamento_id=r["departamento_id"],
                    data_admissao=r["data_admissao"],
                    ativo=r["ativo"],
                    departamento_nome=r["departamento_nome"],
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
                SET nome = ?, cargo = ?, salario = ?, departamento_id = ?, data_admissao = ?, ativo = ?
                WHERE id = ?
                """,
                (
                    func.nome,
                    func.cargo,
                    func.salario,
                    func.departamento_id,
                    func.data_admissao,
                    func.ativo,
                    func.id,
                ),
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