import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "empresa.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _migrate_funcionario_string_departamento_to_fk(cur: sqlite3.Cursor):
    """Migra tabela funcionario antiga (com coluna 'departamento' texto) para novo formato com 'departamento_id'.

    Estratégia:
      - Cria nova tabela funcionario_new com novo schema.
      - Copia colunas compatíveis (perdendo a informação textual de departamento antiga).
      - Descarta tabela antiga e renomeia a nova.
    Esta migração é best-effort e usada apenas em ambiente didático.
    """
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS funcionario_new (
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
    # Copia dados preservando colunas existentes (departamento textual é descartado)
    cur.execute(
        """
        INSERT INTO funcionario_new (id, nome, cargo, salario, data_admissao, ativo)
        SELECT id, nome, cargo, salario, data_admissao, ativo FROM funcionario;
        """
    )
    cur.execute("DROP TABLE funcionario;")
    cur.execute("ALTER TABLE funcionario_new RENAME TO funcionario;")

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        # Cria tabela departamento primeiro
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            );
            """
        )
        # Verifica se já existe tabela funcionario e se precisa migrar
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='funcionario';"
        )
        exists = cur.fetchone() is not None
        if exists:
            # Checa colunas atuais
            cur.execute("PRAGMA table_info(funcionario);")
            cols = [row[1] for row in cur.fetchall()]
            if 'departamento_id' not in cols and 'departamento' in cols:
                _migrate_funcionario_string_departamento_to_fk(cur)
        # Cria (ou garante) tabela funcionario no novo formato
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
    print(f"Banco criado / migrado em: {DB_PATH}")
        
       