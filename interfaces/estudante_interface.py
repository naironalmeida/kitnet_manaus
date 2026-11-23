
"""Tela de cadastro e consulta de Estudantes."""

import tkinter as tk
from tkinter import ttk

from interfaces import JanelaBase
from models.estudante import Estudante
from services.estudante_service import EstudanteService

class EstudanteInterface(JanelaBase):
    """Tela de cadastro e consulta de estudantes; encaminha operações ao serviço correspondente."""
    CAMPOS = [
        ("nome", "Nome completo", None),
        ("cpf", "CPF (somente números)", None),
        ("telefone", "Telefone (com DDD)", None),
        ("email", "E-mail", None),
        ("curso", "Curso", None),
        ("instituicao", "Instituição", None),
    ]
    COLUNAS = [
        ("id", "ID", 50),
        ("nome", "Nome", 220),
        ("cpf", "CPF", 120),
        ("telefone", "Telefone", 130),
        ("email", "E-mail", 200),
        ("curso", "Curso", 140),
        ("instituicao", "Instituição", 140),
    ]

    # Paleta de cores
    AZUL_MARINHO = "#142B46"
    AZUL = "#2878B9"
    AZUL_CLARO = "#DCE8F5"
    FUNDO = "#F1F5F9"
    BRANCO = "#FFFFFF"
    TEXTO = "#26364A"
    CINZA = "#64748B"
    VERMELHO = "#C0392B"
    VERDE = "#218838"
    def __init__(self, master, usuario):
        """Inicializa a janela e prepara seus componentes e dependências."""
        super().__init__(
            master,
            usuario,
            "Estudantes",
            geometria="1150x750"
        )
        self.service = EstudanteService()
        self.busca = tk.StringVar()
        self._configurar_estilos()
        self._montar()
        self.carregar()
    def _configurar_estilos(self):
        """Define estilos visuais usados pelos componentes da tela."""
        estilo = ttk.Style(self)

        # Tema que permite personalizar as cores dos widgets
        estilo.theme_use("clam")

        # Fundo dos painéis
        estilo.configure(
            "Estudante.TFrame",
            background=self.FUNDO
        )
        estilo.configure(
            "Painel.TLabelframe",
            background=self.BRANCO,
            bordercolor="#DCE4ED",
            relief="solid",
            borderwidth=1
        )
        estilo.configure(
            "Painel.TLabelframe.Label",
            background=self.BRANCO,
            foreground=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        )
        estilo.configure(
            "Painel.TLabel",
            background=self.BRANCO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )
        estilo.configure(
            "Campo.TEntry",
            padding=6,
            fieldbackground=self.BRANCO
        )

        # Botão de pesquisa
        estilo.configure(
            "Pesquisar.TButton",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=(14, 7),
            borderwidth=0
        )
        estilo.map(
            "Pesquisar.TButton",
            background=[
                ("active", self.AZUL),
                ("pressed", self.AZUL)
            ],
            foreground=[
                ("active", self.BRANCO)
            ]
        )
        # Tabela
        estilo.configure(
            "Estudante.Treeview",
            background=self.BRANCO,
            foreground=self.TEXTO,
            fieldbackground=self.BRANCO,
            rowheight=30,
            font=("Segoe UI", 9)
        )
        estilo.configure(
            "Estudante.Treeview.Heading",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=9,
            relief="flat"
        )
        estilo.map(
            "Estudante.Treeview",
            background=[("selected", self.AZUL)],
            foreground=[("selected", self.BRANCO)]
        )
        estilo.map(
            "Estudante.Treeview.Heading",
            background=[("active", self.AZUL)]
        )
        # Aplica o estilo à tabela criada pela classe base
        self.configure(bg=self.FUNDO)
        self.corpo.configure(style="Estudante.TFrame")

    # Montagem da interface
    def _montar(self):
        # Cabeçalho azul-marinho
        """Monta os campos, tabelas e ações disponíveis na tela."""
        cabecalho = tk.Frame(
            self.corpo,
            bg=self.AZUL_MARINHO,
            padx=20,
            pady=16
        )
        cabecalho.pack(
            fill="x",
            pady=(0, 16)
        )
        tk.Label(
            cabecalho,
            text="KITNET MANAUS",
            font=("Segoe UI", 11, "bold"),
            fg="#AFCBE8",
            bg=self.AZUL_MARINHO
        ).pack(anchor="w")
        tk.Label(
            cabecalho,
            text="Gerenciamento de estudantes",
            font=("Segoe UI", 19, "bold"),
            fg=self.BRANCO,
            bg=self.AZUL_MARINHO
        ).pack(anchor="w", pady=(5, 2))
        tk.Label(
            cabecalho,
            text="Cadastre, atualize, consulte e gerencie os estudantes.",
            font=("Segoe UI", 9),
            fg="#DCE8F5",
            bg=self.AZUL_MARINHO
        ).pack(anchor="w")

        # Formulário
        formulario = self.criar_formulario(
            self.corpo,
            self.CAMPOS,
            colunas=2,
            titulo="Dados do estudante"
        )
        formulario.configure(
            style="Painel.TLabelframe"
        )
        formulario.pack(
            fill="x",
            pady=(0, 12)
        )

        # Personaliza os campos criados pela JanelaBase
        for widget in self.widgets.values():
            widget.configure(
                style="Campo.TEntry"
            )

        # Personaliza os rótulos do formulário
        for filho in formulario.winfo_children():
            if isinstance(filho, ttk.Label):
                filho.configure(style="Painel.TLabel")

        # Botões de operação
        painel_botoes = tk.Frame(
            self.corpo,
            bg=self.FUNDO
        )
        painel_botoes.pack(
            fill="x",
            pady=(0, 15)
        )
        botoes = [
            ("Cadastrar", self.cadastrar, self.AZUL),
            ("Atualizar", self.atualizar, self.VERDE),
            ("Excluir", self.excluir, self.VERMELHO),
            ("Limpar", self.limpar_formulario, self.CINZA),
        ]
        for texto, comando, cor in botoes:
            tk.Button(
                painel_botoes,
                text=texto,
                command=comando,
                font=("Segoe UI", 9, "bold"),
                bg=cor,
                fg=self.BRANCO,
                activebackground=self.AZUL_MARINHO,
                activeforeground=self.BRANCO,
                relief="flat",
                bd=0,
                padx=18,
                pady=9,
                cursor="hand2"
            ).pack(
                side="left",
                padx=(0, 8)
            )

        # Painel de pesquisa
        painel_busca = ttk.LabelFrame(
            self.corpo,
            text="Consulta de estudantes",
            padding=12,
            style="Painel.TLabelframe"
        )
        painel_busca.pack(
            fill="x",
            pady=(0, 12)
        )
        ttk.Label(
            painel_busca,
            text="Buscar por nome, CPF, curso ou instituição:",
            style="Painel.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 7)
        )
        linha_busca = ttk.Frame(
            painel_busca,
            style="Estudante.TFrame"
        )
        linha_busca.pack(fill="x")
        entrada_busca = ttk.Entry(
            linha_busca,
            textvariable=self.busca,
            style="Campo.TEntry"
        )
        entrada_busca.pack(
            side="left",
            fill="x",
            expand=True
        )
        entrada_busca.bind(
            "<Return>",
            lambda _e: self.carregar()
        )
        ttk.Button(
            linha_busca,
            text="Pesquisar",
            command=self.carregar,
            style="Pesquisar.TButton"
        ).pack(
            side="left",
            padx=(8, 0)
        )

        # Painel da tabela
        painel_tabela = ttk.LabelFrame(
            self.corpo,
            text="Estudantes cadastrados",
            padding=10,
            style="Painel.TLabelframe"
        )
        painel_tabela.pack(
            fill="both",
            expand=True
        )
        tabela = self.criar_tabela(
            painel_tabela,
            self.COLUNAS
        )
        tabela.pack(
            fill="both",
            expand=True
        )
        self.tree.configure(
            style="Estudante.Treeview"
        )

        # Cores alternadas das linhas
        self.tree.tag_configure(
            "linha_par",
            background="#FFFFFF"
        )
        self.tree.tag_configure(
            "linha_impar",
            background="#EAF1F8"
        )

    # Carregamento da tabela

    def carregar(self):
        """Consulta os dados e atualiza a tabela exibida."""
        def acao():
            estudantes = self.service.listar(
                self.busca.get()
            )
            linhas = []
            for e in estudantes:
                linhas.append(
                    (
                        e.id,
                        (
                            e.id,
                            e.nome,
                            e.cpf_formatado(),
                            e.telefone_formatado(),
                            e.email,
                            e.curso,
                            e.instituicao
                        )
                    )
                )
            self.popular_tabela(linhas)

            # Aplica cores alternadas nas linhas
            for indice, item in enumerate(
                self.tree.get_children()
            ):
                tag = (
                    "linha_par"
                    if indice % 2 == 0
                    else "linha_impar"
                )
                self.tree.item(
                    item,
                    tags=(tag,)
                )
        self.executar(acao)

    # Seleção de estudante
    def ao_selecionar(self):
        """Preenche ou ajusta os campos quando uma linha é selecionada."""
        identificador = self.id_selecionado()
        if identificador is None:
            return
        estudante = self.service.buscar_por_id(
            identificador
        )
        if estudante:
            self.definir_valores({
                "nome": estudante.nome,
                "cpf": estudante.cpf,
                "telefone": estudante.telefone,
                "email": estudante.email,
                "curso": estudante.curso,
                "instituicao": estudante.instituicao,
            })

    # Cadastro

    def cadastrar(self):
        """Valida os dados informados e solicita o cadastro ao serviço."""
        dados = self.obter_dados()
        ok = self.executar(
            lambda: self.service.cadastrar(
                Estudante(**dados),
                self.usuario["id"]
            ),
            "Estudante cadastrado com sucesso!"
        )
        if ok:
            self.limpar_formulario()
            self.carregar()

    # Atualização

    def atualizar(self):
        """Valida as alterações e solicita a atualização ao serviço."""
        dados = self.obter_dados()
        def acao():
            identificador = self.exigir_selecao(
                "um estudante"
            )
            self.service.atualizar(
                Estudante(
                    id=identificador,
                    **dados
                ),
                self.usuario["id"]
            )
        if self.executar(
            acao,
            "Estudante atualizado com sucesso!"
        ):
            self.carregar()

    # Exclusão

    def excluir(self):
        """Remove o registro selecionado respeitando as regras de negócio."""
        def acao():
            identificador = self.exigir_selecao(
                "um estudante"
            )
            if not self.confirmar(
                "Deseja realmente excluir o estudante selecionado?"
            ):
                return
            self.service.excluir(
                identificador,
                self.usuario["id"]
            )
            self.limpar_formulario()
            self.carregar()
        self.executar(acao)