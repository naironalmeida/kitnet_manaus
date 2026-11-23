
"""Tela de login e menu principal do KITNET MANAUS."""

import tkinter as tk
from tkinter import messagebox

from interfaces.estilo import aplicar_estilo_minimalista

from interfaces.estudante_interface import EstudanteInterface
from interfaces.kitnet_interface import KitnetInterface
from interfaces.locacao_interface import LocacaoInterface
from interfaces.manutencao_interface import ManutencaoInterface
from interfaces.pagamento_interface import PagamentoInterface
from interfaces.relatorio_interface import RelatorioInterface

from services import ErroNegocio
from services.usuario_service import UsuarioService

def _aplicar_tema():
    try:
        aplicar_estilo_minimalista(tk._default_root)
    except tk.TclError:
        pass

class LoginJanela(tk.Tk):
    """Janela de login do sistema."""

    def __init__(self):
        """Inicializa a janela e prepara seus componentes e dependências."""
        super().__init__()

        _aplicar_tema()

        self.title("KITNET MANAUS - Login")
        self.geometry("380x320")
        self.resizable(False, False)

        self.usuario = None

        self.var_login = tk.StringVar()
        self.var_senha = tk.StringVar()

        self._montar()

        self.bind("<Return>", lambda _e: self.entrar())

    def _montar(self):

        """Monta os campos, tabelas e ações disponíveis na tela."""
        quadro = tk.Frame(self, padx=25, pady=25)
        quadro.pack(fill="both", expand=True)

        tk.Label(
            quadro,
            text="KITNET MANAUS",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 4))

        tk.Label(
            quadro,
            text="Sistema de gestão de kitnets para estudantes"
        ).pack(pady=(0, 18))

        tk.Label(quadro, text="Login").pack(anchor="w")

        self.entrada_login = tk.Entry(
            quadro,
            textvariable=self.var_login
        )
        self.entrada_login.pack(fill="x", pady=(0, 8))

        tk.Label(quadro, text="Senha").pack(anchor="w")

        tk.Entry(
            quadro,
            textvariable=self.var_senha,
            show="*"
        ).pack(fill="x", pady=(0, 14))

        tk.Button(
            quadro,
            text="Entrar",
            command=self.entrar
        ).pack(fill="x")

        self.entrada_login.focus_set()

    def entrar(self):

        """Valida as credenciais e prossegue para o menu principal."""
        try:
            self.usuario = UsuarioService.autenticar(
                self.var_login.get(),
                self.var_senha.get()
            )

        except ErroNegocio as erro:

            messagebox.showerror(
                "Acesso negado",
                str(erro),
                parent=self
            )

            self.var_senha.set("")
            return

        self.destroy()

class MenuPrincipal(tk.Tk):

    """Menu central que direciona o usuário aos módulos do sistema."""
    MODULOS = [
        ("Estudantes", EstudanteInterface, "Cadastro e consulta de estudantes"),
        ("Kitnets", KitnetInterface, "Gerenciamento dos imóveis"),
        ("Locações", LocacaoInterface, "Controle de contratos e locações"),
        ("Pagamentos", PagamentoInterface, "Acompanhamento financeiro"),
        ("Manutenções", ManutencaoInterface, "Controle de reparos e serviços"),
        ("Relatórios", RelatorioInterface, "Consultas e relatórios gerenciais"),
    ]

    AZUL_ESCURO = "#142B46"
    AZUL = "#2878B9"
    FUNDO = "#F1F5F9"
    BRANCO = "#FFFFFF"
    TEXTO = "#26364A"
    CINZA = "#64748B"

    def __init__(self, usuario):
        """Inicializa a janela e prepara seus componentes e dependências."""
        super().__init__()

        _aplicar_tema()

        self.usuario = usuario
        self.janelas = {}

        self.title("KITNET MANAUS - Painel de Controle")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=self.FUNDO)

        self._montar()

    def _montar(self):

        # Estrutura principal
        """Monta os campos, tabelas e ações disponíveis na tela."""
        principal = tk.Frame(self, bg=self.FUNDO)
        principal.pack(fill="both", expand=True)

        # MENU LATERAL
        lateral = tk.Frame(
            principal,
            bg=self.AZUL_ESCURO,
            width=230
        )

        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)

        # Identidade visual
        marca = tk.Frame(
            lateral,
            bg=self.AZUL_ESCURO
        )

        marca.pack(fill="x", padx=20, pady=(30, 35))

        tk.Label(
            marca,
            text="◆",
            font=("Segoe UI", 24, "bold"),
            fg="#55B5F2",
            bg=self.AZUL_ESCURO
        ).pack(anchor="w")

        tk.Label(
            marca,
            text="KITNET MANAUS",
            font=("Segoe UI", 16, "bold"),
            fg=self.BRANCO,
            bg=self.AZUL_ESCURO
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            marca,
            text="GESTÃO IMOBILIÁRIA",
            font=("Segoe UI", 8),
            fg="#A9BED3",
            bg=self.AZUL_ESCURO
        ).pack(anchor="w")

        # Navegação
        tk.Label(
            lateral,
            text="MENU PRINCIPAL",
            font=("Segoe UI", 9, "bold"),
            fg="#91A9C2",
            bg=self.AZUL_ESCURO
        ).pack(anchor="w", padx=22, pady=(0, 12))

        for nome, classe, descricao in self.MODULOS:

            tk.Button(
                lateral,
                text=f"   {nome}",
                font=("Segoe UI", 10),
                bg=self.AZUL_ESCURO,
                fg=self.BRANCO,
                activebackground="#25496D",
                activeforeground=self.BRANCO,
                relief="flat",
                bd=0,
                anchor="w",
                padx=15,
                pady=12,
                cursor="hand2",
                command=lambda n=nome, c=classe: self.abrir_modulo(n, c)
            ).pack(fill="x", padx=10, pady=2)

        # Área do usuário
        usuario_area = tk.Frame(
            lateral,
            bg="#1C3B5B",
            padx=12,
            pady=12
        )

        usuario_area.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=15
        )

        tk.Label(
            usuario_area,
            text=self.usuario["nome"],
            font=("Segoe UI", 10, "bold"),
            fg=self.BRANCO,
            bg="#1C3B5B"
        ).pack(anchor="w")

        tk.Label(
            usuario_area,
            text=self.usuario["perfil"],
            font=("Segoe UI", 9),
            fg="#B8CADB",
            bg="#1C3B5B"
        ).pack(anchor="w", pady=(3, 0))

        # Botão sair
        tk.Button(
            lateral,
            text="↪   Sair do sistema",
            font=("Segoe UI", 10),
            bg=self.AZUL_ESCURO,
            fg="#FCA5A5",
            activebackground="#25496D",
            activeforeground=self.BRANCO,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            pady=12,
            cursor="hand2",
            command=self.sair
        ).pack(side="bottom", fill="x")

        # ÁREA CENTRAL
        conteudo = tk.Frame(
            principal,
            bg=self.FUNDO
        )

        conteudo.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Cabeçalho
        cabecalho = tk.Frame(
            conteudo,
            bg=self.BRANCO,
            height=65
        )

        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        tk.Label(
            cabecalho,
            text="Painel de Controle",
            font=("Segoe UI", 12, "bold"),
            fg=self.TEXTO,
            bg=self.BRANCO
        ).pack(side="left", padx=30, pady=20)

        tk.Label(
            cabecalho,
            text=f"Olá, {self.usuario['nome']}",
            font=("Segoe UI", 10),
            fg=self.CINZA,
            bg=self.BRANCO
        ).pack(side="right", padx=30)

        # Corpo do painel
        corpo = tk.Frame(
            conteudo,
            bg=self.FUNDO
        )

        corpo.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        tk.Label(
            corpo,
            text="Bem-vindo ao KITNET MANAUS",
            font=("Segoe UI", 22, "bold"),
            fg=self.AZUL_ESCURO,
            bg=self.FUNDO
        ).pack(anchor="w")

        tk.Label(
            corpo,
            text="Gerencie seus imóveis, estudantes e operações em um só lugar.",
            font=("Segoe UI", 10),
            fg=self.CINZA,
            bg=self.FUNDO
        ).pack(anchor="w", pady=(5, 25))

        tk.Label(
            corpo,
            text="ACESSO AOS MÓDULOS",
            font=("Segoe UI", 10, "bold"),
            fg=self.CINZA,
            bg=self.FUNDO
        ).pack(anchor="w", pady=(0, 12))

        # Grade dos cartões
        grade = tk.Frame(
            corpo,
            bg=self.FUNDO
        )

        grade.pack(fill="both", expand=True)

        for coluna in range(3):
            grade.columnconfigure(coluna, weight=1)

        for linha in range(2):
            grade.rowconfigure(linha, weight=1)

        for indice, (nome, classe, descricao) in enumerate(self.MODULOS):

            linha, coluna = divmod(indice, 3)

            cartao = tk.Frame(
                grade,
                bg=self.BRANCO,
                highlightbackground="#DCE4ED",
                highlightthickness=1
            )

            cartao.grid(
                row=linha,
                column=coluna,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            interno = tk.Frame(
                cartao,
                bg=self.BRANCO
            )

            interno.pack(
                fill="both",
                expand=True,
                padx=18,
                pady=18
            )

            tk.Label(
                interno,
                text=nome,
                font=("Segoe UI", 13, "bold"),
                fg=self.AZUL_ESCURO,
                bg=self.BRANCO
            ).pack(anchor="w")

            tk.Label(
                interno,
                text=descricao,
                font=("Segoe UI", 9),
                fg=self.CINZA,
                bg=self.BRANCO,
                wraplength=200,
                justify="left"
            ).pack(anchor="w", pady=(8, 15))

            tk.Button(
                interno,
                text="Abrir →",
                font=("Segoe UI", 9, "bold"),
                bg=self.AZUL,
                fg=self.BRANCO,
                activebackground="#1D5F96",
                activeforeground=self.BRANCO,
                relief="flat",
                bd=0,
                padx=12,
                pady=8,
                cursor="hand2",
                command=lambda n=nome, c=classe: self.abrir_modulo(n, c)
            ).pack(anchor="w")

        # Rodapé
        tk.Label(
            conteudo,
            text="KITNET MANAUS | Sistema de Gestão de Locações",
            font=("Segoe UI", 8),
            fg=self.CINZA,
            bg=self.FUNDO
        ).pack(pady=(0, 12))

    def abrir_modulo(self, nome, classe):

        """Abre o módulo selecionado conforme as permissões do usuário."""
        janela = self.janelas.get(nome)

        if janela is not None and janela.winfo_exists():
            janela.deiconify()
            janela.lift()
            janela.focus_force()
            return

        self.janelas[nome] = classe(self, self.usuario)

    def sair(self):

        """Fecha a sessão e encerra a janela principal."""
        if messagebox.askyesno(
            "Sair",
            "Deseja encerrar o sistema?",
            parent=self
        ):
            self.destroy()

if __name__ == "__main__":

    login = LoginJanela()
    login.mainloop()

    if login.usuario:
        app = MenuPrincipal(login.usuario)
        app.mainloop()
