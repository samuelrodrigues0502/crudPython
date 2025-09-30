import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "empresa.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cargo TEXT NOT NULL,
                salario REAL NOT NULL,
                departamento TEXT,
                data_admissao TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1
            );
            """
        )
        conn.commit()
    
if __name__ == "__main__":
    init_db()
    print(f"Banco criado em: {DB_PATH}")
        
       