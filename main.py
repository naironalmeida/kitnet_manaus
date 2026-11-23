
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from database.criar_tabelas import criar_tabelas  # noqa: E402
from interfaces.menu import LoginJanela, MenuPrincipal  # noqa: E402

def main():
    """Inicializa as tabelas, autentica o usuário e abre o menu principal."""
    criar_tabelas()  # cria kitnet_manaus.db e as tabelas na primeira execução

    login = LoginJanela()
    login.mainloop()
    if login.usuario is None:
        return  # janela de login fechada sem autenticar

    MenuPrincipal(login.usuario).mainloop()

if __name__ == "__main__":
    main()
