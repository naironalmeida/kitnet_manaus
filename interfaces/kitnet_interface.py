
"""Tela de cadastro e consulta de Kitnets."""

import tkinter as tk
from tkinter import ttk

from interfaces import JanelaBase
from models.kitnet import Kitnet
from services import converter_inteiro, converter_valor, formatar_moeda
from services.kitnet_service import KitnetService

class KitnetInterface(JanelaBase):

    """Tela de cadastro e consulta de kitnets, ligada às regras do serviço de kitnets."""
    CAMPOS = [
        ("endereco", "Endereço", None),
        ("bairro", "Bairro", None),
        ("quartos", "Quartos", None),
        ("valor_aluguel", "Valor do aluguel (R$)", None),
        ("status", "Status", Kitnet.STATUS_VALIDOS),
    ]

    COLUNAS = [
        ("id", "ID", 50),
        ("endereco", "Endereço", 280),
        ("bairro", "Bairro", 150),
        ("quartos", "Quartos", 70),
        ("valor", "Aluguel", 110),
        ("status", "Status", 120),
    ]

    # Paleta de cores
    AZUL_MARINHO = "#142B46"
    AZUL = "#2878B9"
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
            "Kitnets",
            geometria="1150x750"
        )

        self.service = KitnetService()
        self.busca = tk.StringVar()
        self.filtro = tk.StringVar(value="Todos")

        self._configurar_estilos()
        self._montar()
        self.limpar()
        self.carregar()

    # --------------------------------------------------
    # Estilos
    # --------------------------------------------------

    def _configurar_estilos(self):

        """Define estilos visuais usados pelos componentes da tela."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Kitnet.TFrame",
            background=self.FUNDO
        )

        estilo.configure(
            "Kitnet.TLabelframe",
            background=self.BRANCO,
            bordercolor="#DCE4ED",
            relief="solid",
            borderwidth=1
        )

        estilo.configure(
            "Kitnet.TLabelframe.Label",
            background=self.BRANCO,
            foreground=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Kitnet.TLabel",
            background=self.BRANCO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Kitnet.TEntry",
            padding=6,
            fieldbackground=self.BRANCO
        )

        estilo.configure(
            "Kitnet.TCombobox",
            padding=6,
            fieldbackground=self.BRANCO
        )

        estilo.configure(
            "Kitnet.Pesquisar.TButton",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=(14, 7),
            borderwidth=0
        )

        estilo.map(
            "Kitnet.Pesquisar.TButton",
            background=[
                ("active", self.AZUL),
                ("pressed", self.AZUL)
            ],
            foreground=[
                ("active", self.BRANCO)
            ]
        )

        estilo.configure(
            "Kitnet.Treeview",
            background=self.BRANCO,
            foreground=self.TEXTO,
            fieldbackground=self.BRANCO,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Kitnet.Treeview.Heading",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=9,
            relief="flat"
        )

        estilo.map(
            "Kitnet.Treeview",
            background=[("selected", self.AZUL)],
            foreground=[("selected", self.BRANCO)]
        )

        estilo.map(
            "Kitnet.Treeview.Heading",
            background=[("active", self.AZUL)]
        )

        self.configure(bg=self.FUNDO)
        self.corpo.configure(style="Kitnet.TFrame")

    # --------------------------------------------------
    # Montagem da interface
    # --------------------------------------------------

    def _montar(self):

        # Cabeçalho
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
            text="Gerenciamento de kitnets",
            font=("Segoe UI", 19, "bold"),
            fg=self.BRANCO,
            bg=self.AZUL_MARINHO
        ).pack(anchor="w", pady=(5, 2))

        tk.Label(
            cabecalho,
            text="Cadastre, atualize, consulte e gerencie os imóveis.",
            font=("Segoe UI", 9),
            fg="#DCE8F5",
            bg=self.AZUL_MARINHO
        ).pack(anchor="w")

        # Formulário
        formulario = self.criar_formulario(
            self.corpo,
            self.CAMPOS,
            colunas=2,
            titulo="Dados da kitnet"
        )

        formulario.configure(
            style="Kitnet.TLabelframe"
        )

        formulario.pack(
            fill="x",
            pady=(0, 12)
        )

        # Personalização dos campos
        for chave, widget in self.widgets.items():

            if chave == "status":
                widget.configure(style="Kitnet.TCombobox")
            else:
                widget.configure(style="Kitnet.TEntry")

        # Personalização dos rótulos
        for filho in formulario.winfo_children():

            if isinstance(filho, ttk.Label):
                filho.configure(style="Kitnet.TLabel")

        # Botões
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
            ("Limpar", self.limpar, self.CINZA),
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

        # Painel de consulta
        painel_busca = ttk.LabelFrame(
            self.corpo,
            text="Consulta de kitnets",
            padding=12,
            style="Kitnet.TLabelframe"
        )

        painel_busca.pack(
            fill="x",
            pady=(0, 12)
        )

        linha_busca = ttk.Frame(
            painel_busca,
            style="Kitnet.TFrame"
        )

        linha_busca.pack(fill="x")

        # Campo de pesquisa
        ttk.Label(
            linha_busca,
            text="Buscar endereço ou bairro:",
            style="Kitnet.TLabel"
        ).pack(
            side="left",
            padx=(0, 6)
        )

        entrada = ttk.Entry(
            linha_busca,
            textvariable=self.busca,
            style="Kitnet.TEntry",
            width=28
        )

        entrada.pack(
            side="left",
            fill="x",
            expand=True
        )

        entrada.bind(
            "<Return>",
            lambda _e: self.carregar()
        )

        # Filtro por status
        ttk.Label(
            linha_busca,
            text="Status:",
            style="Kitnet.TLabel"
        ).pack(
            side="left",
            padx=(12, 5)
        )

        combo = ttk.Combobox(
            linha_busca,
            textvariable=self.filtro,
            state="readonly",
            width=19,
            values=("Todos",) + Kitnet.STATUS_VALIDOS,
            style="Kitnet.TCombobox"
        )

        combo.pack(side="left")

        combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self.carregar()
        )

        # Botão de pesquisa
        ttk.Button(
            linha_busca,
            text="Pesquisar",
            command=self.carregar,
            style="Kitnet.Pesquisar.TButton"
        ).pack(
            side="left",
            padx=(8, 0)
        )

        # Painel da tabela
        painel_tabela = ttk.LabelFrame(
            self.corpo,
            text="Kitnets cadastradas",
            padding=10,
            style="Kitnet.TLabelframe"
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
            style="Kitnet.Treeview"
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

    # --------------------------------------------------
    # Limpar formulário
    # --------------------------------------------------

    def limpar(self):

        """Limpa os campos e a seleção atual da tela."""
        self.limpar_formulario()

        self.definir_valores({
            "quartos": "1",
            "status": Kitnet.DISPONIVEL
        })

    # --------------------------------------------------
    # Carregar tabela
    # --------------------------------------------------

    def carregar(self):

        """Consulta os dados e atualiza a tabela exibida."""
        def acao():

            status = (
                None
                if self.filtro.get() == "Todos"
                else self.filtro.get()
            )

            kitnets = self.service.listar(
                status,
                self.busca.get()
            )

            linhas = []

            for k in kitnets:

                linhas.append(
                    (
                        k.id,
                        (
                            k.id,
                            k.endereco,
                            k.bairro,
                            k.quartos,
                            formatar_moeda(k.valor_aluguel),
                            k.status
                        )
                    )
                )

            self.popular_tabela(linhas)

            # Aplica cores alternadas
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

    # --------------------------------------------------
    # Seleção de kitnet
    # --------------------------------------------------

    def ao_selecionar(self):

        """Preenche ou ajusta os campos quando uma linha é selecionada."""
        identificador = self.id_selecionado()

        if identificador is None:
            return

        kitnet = self.service.buscar_por_id(
            identificador
        )

        if kitnet:

            self.definir_valores({
                "endereco": kitnet.endereco,
                "bairro": kitnet.bairro,
                "quartos": kitnet.quartos,
                "valor_aluguel": (
                    f"{kitnet.valor_aluguel:.2f}"
                    .replace(".", ",")
                ),
                "status": kitnet.status,
            })

    # --------------------------------------------------
    # Montar objeto Kitnet
    # --------------------------------------------------

    def _montar_kitnet(self, identificador=None):

        """Monta a representação de uma kitnet para exibição."""
        dados = self.obter_dados()

        return Kitnet(
            id=identificador,
            endereco=dados["endereco"],
            bairro=dados["bairro"],
            quartos=converter_inteiro(
                dados["quartos"],
                "Quartos"
            ),
            valor_aluguel=converter_valor(
                dados["valor_aluguel"]
            ),
            status=dados["status"] or Kitnet.DISPONIVEL,
        )

    # --------------------------------------------------
    # Cadastro
    # --------------------------------------------------

    def cadastrar(self):

        """Valida os dados informados e solicita o cadastro ao serviço."""
        ok = self.executar(
            lambda: self.service.cadastrar(
                self._montar_kitnet(),
                self.usuario["id"]
            ),
            "Kitnet cadastrada com sucesso!"
        )

        if ok:
            self.limpar()
            self.carregar()

    # --------------------------------------------------
    # Atualização
    # --------------------------------------------------

    def atualizar(self):

        """Valida as alterações e solicita a atualização ao serviço."""
        def acao():

            identificador = self.exigir_selecao(
                "uma kitnet"
            )

                        # As regras de disponibilidade são verificadas pelo serviço antes de salvar.
            self.service.atualizar(
                self._montar_kitnet(identificador),
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Kitnet atualizada com sucesso!"
        ):
            self.carregar()

    # --------------------------------------------------
    # Exclusão
    # --------------------------------------------------

    def excluir(self):

        """Remove o registro selecionado respeitando as regras de negócio."""
        def acao():

            identificador = self.exigir_selecao(
                "uma kitnet"
            )

            if not self.confirmar(
                "Deseja realmente excluir a kitnet selecionada?"
            ):
                return

            self.service.excluir(
                identificador,
                self.usuario["id"]
            )

            self.limpar()
            self.carregar()

        self.executar(acao)
