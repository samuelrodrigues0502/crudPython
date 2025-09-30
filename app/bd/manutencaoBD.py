def zerarBD():
    confirm = input("Tem certeza que deseja zerar TODAS as tabelas (funcionarios e departamentos)? (s/n): ").strip().lower()
    if confirm != 's':
        print("Ação cancelada.")
        return
    try:
        from app.bd.connection import get_connection
        with get_connection() as conn:
            cur = conn.cursor()
            # Ordem: primeiro filhos (funcionario), depois pais (departamento)
            cur.execute("DELETE FROM funcionario;")
            cur.execute("DELETE FROM departamento;")
            # Reseta auto-increments (sqlite_sequence) se existir
            cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('funcionario','departamento');")
            conn.commit()
        print("Banco zerado. Funcionários e Departamentos removidos.")
    except Exception as e:
        print("Erro ao zerar banco:", e)