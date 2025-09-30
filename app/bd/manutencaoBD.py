
def zerarBD():
    confirm = input("Tem certeza que deseja zerar o banco? Todos os dados serão apagados! (s/n): ").strip().lower()
    if confirm != 's':
        print("Ação cancelada.")
        return
    try:
        from app.bd.connection import get_connection
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM funcionario;")
            cur.execute("DELETE FROM sqlite_sequence WHERE name='funcionario';")
            conn.commit()
        print("Banco zerado. Todos os dados foram removidos.")
    except Exception as e:
        print("Erro ao zerar banco:", e)