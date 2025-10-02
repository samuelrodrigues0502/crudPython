import sys
from app.bd.connection import init_db
from app.views.cli_view import executar_menu
from app.views.gui_view import run_gui


def main():
    init_db()
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        executar_menu()
    else:
        run_gui()


if __name__ == "__main__":
    main()