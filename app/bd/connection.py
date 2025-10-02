import sqlite3
from pathlib import Path

# Permite redefinir dinamicamente o caminho do banco durante execução (GUI)
# Atenção: Todos os models chamam get_connection a cada operação, então
# atualizar DB_PATH aqui fará com que as próximas operações usem o novo arquivo.

DB_PATH = Path(__file__).resolve().parent / "rhPM.db"

def set_db_path(new_path) -> Path:
    """Redefine o caminho do banco para new_path e retorna o Path atualizado."""
    global DB_PATH
    DB_PATH = Path(new_path).expanduser().resolve()
    return DB_PATH

def get_db_path() -> Path:
    """Retorna o caminho atual configurado do banco."""
    return DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    # Garante que restrições de chave estrangeira sejam aplicadas
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cargo TEXT NOT NULL,
                salario REAL NOT NULL,
                departamento_id INTEGER,
                data_admissao TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id)
            );
            """
        )
        conn.commit()

if __name__ == "__main__":
    init_db()
    print(f"Banco criado em: {DB_PATH}")
        
       