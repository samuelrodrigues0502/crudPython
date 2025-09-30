from app.bd.connection import init_db
from app.views.cli_view import executar_menu

def main():
    init_db()
    executar_menu()

if __name__ == "__main__":
    main()