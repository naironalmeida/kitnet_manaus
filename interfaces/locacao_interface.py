
"""Tela de gerenciamento de Locações."""

from datetime import date

import tkinter as tk
from tkinter import ttk

from interfaces import JanelaBase
from models.locacao import Locacao
from services import converter_valor, formatar_moeda
from services.estudante_service import EstudanteService
from services.kitnet_service import KitnetService
from services.locacao_service import LocacaoService

class LocacaoInterface(JanelaBase):

    """Tela de locações; conecta estudantes e kitnets às operações do serviço de locação."""
    CAMPOS = [
        ("estudante", "Estudante (sem locação ativa)", []),
        ("kitnet", "Kitnet disponível", []),
        ("data_inicio", "Início (AAAA-MM-DD)", None),
        ("data_fim", "Fim previsto (opcional)", None),
        ("valor_contratado", "Valor contratado (R$)", None),
    ]

    COLUNAS = [
        ("id", "ID", 50),
        ("estudante", "Estudante", 200),
        ("kitnet", "Kitnet", 240),
        ("inicio", "Início", 95),
        ("fim", "Fim", 95),
        ("valor", "Valor", 100),
        ("status", "Status", 90),
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
            "Locações",
            geometria="1200x760"
        )

        self.service = LocacaoService()
        self.kitnets = {}
        self.filtro = tk.StringVar(value="Todos")

        self._configurar_estilos()
        self._montar()
        self.novo()
        self.carregar()

    # --------------------------------------------------
    # Estilos
    # --------------------------------------------------

    def _configurar_estilos(self):

        """Define estilos visuais usados pelos componentes da tela."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Locacao.TFrame",
            background=self.FUNDO
        )

        estilo.configure(
            "Locacao.TLabelframe",
            background=self.BRANCO,
            bordercolor="#DCE4ED",
            relief="solid",
            borderwidth=1
        )

        estilo.configure(
            "Locacao.TLabelframe.Label",
            background=self.BRANCO,
            foreground=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Locacao.TLabel",
            background=self.BRANCO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Locacao.TEntry",
            padding=6,
            fieldbackground=self.BRANCO
        )

        estilo.configure(
            "Locacao.TCombobox",
            padding=6,
            fieldbackground=self.BRANCO
        )

        estilo.configure(
            "Locacao.Filtro.TCombobox",
            padding=5,
            fieldbackground=self.BRANCO
        )

        estilo.configure(
            "Locacao.Pesquisar.TButton",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=(14, 7),
            borderwidth=0
        )

        estilo.map(
            "Locacao.Pesquisar.TButton",
            background=[
                ("active", self.AZUL),
                ("pressed", self.AZUL)
            ],
            foreground=[
                ("active", self.BRANCO)
            ]
        )

        estilo.configure(
            "Locacao.Treeview",
            background=self.BRANCO,
            foreground=self.TEXTO,
            fieldbackground=self.BRANCO,
            rowheight=32,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Locacao.Treeview.Heading",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=9,
            relief="flat"
        )

        estilo.map(
            "Locacao.Treeview",
            background=[("selected", self.AZUL)],
            foreground=[("selected", self.BRANCO)]
        )

        estilo.map(
            "Locacao.Treeview.Heading",
            background=[("active", self.AZUL)]
        )

        self.configure(bg=self.FUNDO)
        self.corpo.configure(style="Locacao.TFrame")

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
            text="Gerenciamento de locações",
            font=("Segoe UI", 19, "bold"),
            fg=self.BRANCO,
            bg=self.AZUL_MARINHO
        ).pack(anchor="w", pady=(5, 2))

        tk.Label(
            cabecalho,
            text="Registre, acompanhe, encerre e cancele locações.",
            font=("Segoe UI", 9),
            fg="#DCE8F5",
            bg=self.AZUL_MARINHO
        ).pack(anchor="w")

        # Formulário
        formulario = self.criar_formulario(
            self.corpo,
            self.CAMPOS,
            colunas=2,
            titulo="Dados da locação"
        )

        formulario.configure(
            style="Locacao.TLabelframe"
        )

        formulario.pack(
            fill="x",
            pady=(0, 12)
        )

        # Personalização dos campos
        for chave, widget in self.widgets.items():

            if chave in ("estudante", "kitnet"):
                widget.configure(style="Locacao.TCombobox")
            else:
                widget.configure(style="Locacao.TEntry")

        # Personalização dos rótulos
        for filho in formulario.winfo_children():

            if isinstance(filho, ttk.Label):
                filho.configure(style="Locacao.TLabel")

        # Evento de seleção de kitnet
        self.widgets["kitnet"].bind(
            "<<ComboboxSelected>>",
            self._kitnet_escolhida
        )

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
            (
                "Registrar locação",
                self.registrar,
                self.AZUL
            ),
            (
                "Encerrar selecionada",
                self.encerrar,
                self.VERDE
            ),
            (
                "Cancelar selecionada",
                self.cancelar,
                self.VERMELHO
            ),
            (
                "Novo / Limpar",
                self.novo,
                self.CINZA
            ),
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
                padx=15,
                pady=9,
                cursor="hand2"
            ).pack(
                side="left",
                padx=(0, 8)
            )

        # Painel de filtros
        painel_filtro = ttk.LabelFrame(
            self.corpo,
            text="Consulta de locações",
            padding=12,
            style="Locacao.TLabelframe"
        )

        painel_filtro.pack(
            fill="x",
            pady=(0, 12)
        )

        linha_filtro = ttk.Frame(
            painel_filtro,
            style="Locacao.TFrame"
        )

        linha_filtro.pack(fill="x")

        ttk.Label(
            linha_filtro,
            text="Filtrar por status:",
            style="Locacao.TLabel"
        ).pack(
            side="left",
            padx=(0, 8)
        )

        combo = ttk.Combobox(
            linha_filtro,
            textvariable=self.filtro,
            state="readonly",
            width=20,
            values=("Todos",) + Locacao.STATUS_VALIDOS,
            style="Locacao.Filtro.TCombobox"
        )

        combo.pack(side="left")

        combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self.carregar()
        )

        # Painel da tabela
        painel_tabela = ttk.LabelFrame(
            self.corpo,
            text="Locações cadastradas",
            padding=10,
            style="Locacao.TLabelframe"
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
            style="Locacao.Treeview"
        )

        # Cores alternadas
        self.tree.tag_configure(
            "linha_par",
            background="#FFFFFF"
        )

        self.tree.tag_configure(
            "linha_impar",
            background="#EAF1F8"
        )

        # Cores dos status
        self.tree.tag_configure(
            "Ativa",
            foreground="#218838"
        )

        self.tree.tag_configure(
            "Encerrada",
            foreground=self.CINZA
        )

        self.tree.tag_configure(
            "Cancelada",
            foreground=self.VERMELHO
        )

    # --------------------------------------------------
    # Nova locação / limpar
    # --------------------------------------------------

    def novo(self):

        """Prepara o formulário para um novo registro."""
        self.limpar_formulario()
        self.carregar_opcoes()

        self.definir_valores({
            "data_inicio": date.today().isoformat()
        })

    # --------------------------------------------------
    # Carregar opções dos campos
    # --------------------------------------------------

    def carregar_opcoes(self):

        """Busca no serviço os registros disponíveis para seleção."""
        def acao():

            estudantes = EstudanteService().listar_sem_locacao_ativa()

            self.kitnets = {
                k.id: k
                for k in KitnetService().listar_disponiveis()
            }

            self.definir_opcoes(
                "estudante",
                [
                    f"{e.id} - {e.nome}"
                    for e in estudantes
                ]
            )

            self.definir_opcoes(
                "kitnet",
                [
                    f"{k.id} - {k.endereco} ({k.bairro})"
                    for k in self.kitnets.values()
                ]
            )

        self.executar(acao)

    # --------------------------------------------------
    # Seleção da kitnet
    # --------------------------------------------------

    def _kitnet_escolhida(self, _evento=None):

        """Identifica a kitnet selecionada no formulário."""
        try:

            identificador = self.extrair_id(
                self.vars["kitnet"].get(),
                "kitnet"
            )

            kitnet = self.kitnets.get(identificador)

        except ValueError:
            return

        if kitnet:

            self.definir_valores({
                "valor_contratado": (
                    f"{kitnet.valor_aluguel:.2f}"
                    .replace(".", ",")
                )
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

            linhas = self.service.listar(status)

            dados_tabela = []

            for r in linhas:

                dados_tabela.append(
                    (
                        r["id"],
                        (
                            r["id"],
                            r["estudante"],
                            r["kitnet"],
                            r["data_inicio"],
                            r["data_fim"],
                            formatar_moeda(r["valor_contratado"]),
                            r["status"]
                        ),
                        r["status"]
                    )
                )

            self.popular_tabela(dados_tabela)

            # Aplica as cores alternadas somente nas linhas
            # que não possuem um status especial.
            for indice, item in enumerate(
                self.tree.get_children()
            ):

                status_item = self.tree.item(item, "tags")

                if status_item:
                    continue

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
    # Registrar locação
    # --------------------------------------------------

    def registrar(self):

        """Grava uma operação no histórico, usando a conexão recebida quando disponível."""
        dados = self.obter_dados()

        def acao():

            locacao = Locacao(
                estudante_id=self.extrair_id(
                    dados["estudante"],
                    "estudante"
                ),

                kitnet_id=self.extrair_id(
                    dados["kitnet"],
                    "kitnet"
                ),

                data_inicio=dados["data_inicio"],
                data_fim=dados["data_fim"],

                valor_contratado=converter_valor(
                    dados["valor_contratado"]
                ),
            )

            self.service.criar(
                locacao,
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Locação registrada com sucesso!"
        ):

            self.novo()
            self.carregar()

    # --------------------------------------------------
    # Encerrar locação
    # --------------------------------------------------

    def encerrar(self):

        """Solicita o encerramento da locação selecionada."""
        def acao():

            identificador = self.exigir_selecao(
                "uma locação"
            )

            if not self.confirmar(
                f"Encerrar a locação #{identificador} e liberar a kitnet?"
            ):
                return

                        # O serviço encerra o contrato e ajusta o estado da kitnet.
            self.service.encerrar(
                identificador,
                self.usuario["id"]
            )

            self.novo()
            self.carregar()

        self.executar(acao)

    # --------------------------------------------------
    # Cancelar locação
    # --------------------------------------------------

    def cancelar(self):

        """Solicita o cancelamento do registro selecionado."""
        def acao():

            identificador = self.exigir_selecao(
                "uma locação"
            )

            if not self.confirmar(
                f"Cancelar a locação #{identificador} e liberar a kitnet?"
            ):
                return

            self.service.cancelar(
                identificador,
                self.usuario["id"]
            )

            self.novo()
            self.carregar()

        self.executar(acao)
