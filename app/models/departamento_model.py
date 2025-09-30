from dataclasses import dataclass
from typing import Optional, List
from app.bd.connection import get_connection

@dataclass
class Departamento:
    id: Optional[int]
    nome: str
    descricao: Optional[str] = None

class DepartamentoModel:
    @staticmethod
    def criar(dep: Departamento) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO departamento (nome, descricao)
                VALUES (?, ?)
                """,
                (dep.nome, dep.descricao)
            )
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def listar() -> List[Departamento]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nome, descricao FROM departamento ORDER BY nome;"
            )
            rows = cur.fetchall()
            return [Departamento(id=r["id"], nome=r["nome"], descricao=r["descricao"]) for r in rows]

    @staticmethod
    def obter_por_id(dep_id: int) -> Optional[Departamento]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nome, descricao FROM departamento WHERE id = ?",
                (dep_id,)
            )
            r = cur.fetchone()
            if r:
                return Departamento(id=r["id"], nome=r["nome"], descricao=r["descricao"])
            return None

    @staticmethod
    def remover(dep_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM departamento WHERE id = ?", (dep_id,))
            conn.commit()
            return cur.rowcount > 0
