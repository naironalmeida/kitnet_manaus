
"""Tela de Manutenções."""

import tkinter as tk
from tkinter import ttk

from interfaces import JanelaBase
from models.manutencao import Manutencao
from services import converter_valor, formatar_moeda
from services.kitnet_service import KitnetService
from services.manutencao_service import ManutencaoService

class ManutencaoInterface(JanelaBase):

    """Tela para acompanhar manutenções e registrar suas etapas."""
    CAMPOS = [
        ("kitnet", "Kitnet", []),
        ("categoria", "Categoria", Manutencao.CATEGORIAS),
        ("descricao", "Descrição", None),
        ("custo", "Custo (R$)", None),
    ]

    COLUNAS = [
        ("id", "ID", 50),
        ("kitnet", "Kitnet", 230),
        ("descricao", "Descrição", 260),
        ("categoria", "Categoria", 110),
        ("custo", "Custo", 100),
        ("status", "Status", 100),
    ]

    # Cores da interface
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
        super().__init__(master, usuario, "Manutenções")

        self.service = ManutencaoService()
        self.filtro = tk.StringVar(value="Todos")

        self._configurar_estilos()
        self._montar()
        self.novo()

    def _configurar_estilos(self):
        """Define estilos visuais usados pelos componentes da tela."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        # Fundo principal
        self.configure(bg=self.FUNDO)
        self.corpo.configure(style="Manutencao.TFrame")

        estilo.configure(
            "Manutencao.TFrame",
            background=self.FUNDO
        )

        # Painéis
        estilo.configure(
            "Manutencao.TLabelframe",
            background=self.BRANCO,
            bordercolor="#D5DEE8",
            relief="solid"
        )

        estilo.configure(
            "Manutencao.TLabelframe.Label",
            background=self.BRANCO,
            foreground=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Manutencao.TLabel",
            background=self.BRANCO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Manutencao.Barra.TFrame",
            background=self.FUNDO
        )

        estilo.configure(
            "Manutencao.Barra.TLabel",
            background=self.FUNDO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )

        # Campos de entrada
        estilo.configure(
            "Manutencao.TEntry",
            padding=6,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO
        )

        estilo.configure(
            "Manutencao.TCombobox",
            padding=6,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO
        )

        # Tabela
        estilo.configure(
            "Manutencao.Treeview",
            background=self.BRANCO,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Manutencao.Treeview.Heading",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=8
        )

        estilo.map(
            "Manutencao.Treeview",
            background=[("selected", self.AZUL)],
            foreground=[("selected", self.BRANCO)]
        )

    def _montar(self):

        # Cabeçalho
        """Monta os campos, tabelas e ações disponíveis na tela."""
        cabecalho = tk.Frame(
            self.corpo,
            bg=self.AZUL_MARINHO,
            padx=18,
            pady=14
        )
        cabecalho.pack(fill="x", pady=(0, 12))

        tk.Label(
            cabecalho,
            text="KITNET MANAUS",
            bg=self.AZUL_MARINHO,
            fg=self.BRANCO,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Gerenciamento de manutenções",
            bg=self.AZUL_MARINHO,
            fg="#DCE6F1",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

        # Formulário
        formulario = self.criar_formulario(
            self.corpo,
            self.CAMPOS,
            colunas=2,
            titulo="Dados da manutenção"
        )
        formulario.configure(style="Manutencao.TLabelframe")
        formulario.pack(fill="x", pady=(0, 10))

        for widget in formulario.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Manutencao.TLabel")

        for chave, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry):
                widget.configure(style="Manutencao.TEntry")
            else:
                widget.configure(style="Manutencao.TCombobox")

        # Botões
        botoes = ttk.Frame(
            self.corpo,
            style="Manutencao.TFrame"
        )
        botoes.pack(fill="x", pady=(0, 12))

        tk.Button(
            botoes,
            text="Abrir manutenção",
            command=self.abrir,
            bg=self.AZUL,
            fg=self.BRANCO,
            activebackground=self.AZUL_MARINHO,
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            botoes,
            text="Iniciar selecionada",
            command=self.iniciar,
            bg=self.AZUL_MARINHO,
            fg=self.BRANCO,
            activebackground=self.AZUL,
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="left", padx=6)

        tk.Button(
            botoes,
            text="Concluir selecionada",
            command=self.concluir,
            bg=self.VERDE,
            fg=self.BRANCO,
            activebackground="#176B2C",
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="left", padx=6)

        tk.Button(
            botoes,
            text="Cancelar selecionada",
            command=self.cancelar,
            bg=self.VERMELHO,
            fg=self.BRANCO,
            activebackground="#922B21",
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="left", padx=6)

        tk.Button(
            botoes,
            text="Novo / Atualizar",
            command=self.novo,
            bg=self.CINZA,
            fg=self.BRANCO,
            activebackground="#475569",
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="left", padx=6)

        # Barra de filtros
        barra = ttk.Frame(
            self.corpo,
            style="Manutencao.Barra.TFrame"
        )
        barra.pack(fill="x", pady=(0, 8))

        ttk.Label(
            barra,
            text="Filtrar por status:",
            style="Manutencao.Barra.TLabel"
        ).pack(side="left")

        combo = ttk.Combobox(
            barra,
            textvariable=self.filtro,
            state="readonly",
            width=16,
            values=("Todos",) + Manutencao.STATUS_VALIDOS
        )
        combo.pack(side="left", padx=6)
        combo.configure(style="Manutencao.TCombobox")
        combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self.carregar()
        )

        ttk.Label(
            barra,
            text="Dica: ao concluir, informe o custo final no campo 'Custo' (gera uma despesa).",
            style="Manutencao.Barra.TLabel"
        ).pack(side="left", padx=12)

        # Tabela
        self.criar_tabela(
            self.corpo,
            self.COLUNAS
        ).pack(fill="both", expand=True, pady=(4, 0))

        self.tree.configure(style="Manutencao.Treeview")

        self.tree.tag_configure(
            "Concluída",
            foreground=self.VERDE
        )

        self.tree.tag_configure(
            "Cancelada",
            foreground=self.CINZA
        )

        self.tree.tag_configure(
            "Aberta",
            foreground=self.AZUL
        )

    def novo(self):
        """Prepara o formulário para um novo registro."""
        self.limpar_formulario()
        self.carregar_opcoes()

        self.definir_valores({
            "custo": "0,00"
        })

        self.carregar()

    def carregar_opcoes(self):
        """Busca no serviço os registros disponíveis para seleção."""
        def acao():
            kitnets = KitnetService().listar()

            self.definir_opcoes(
                "kitnet",
                [
                    f"{k.id} - {k.endereco} [{k.status}]"
                    for k in kitnets
                ]
            )

        self.executar(acao)

    def carregar(self):
        """Consulta os dados e atualiza a tabela exibida."""
        def acao():
            status = (
                None
                if self.filtro.get() == "Todos"
                else self.filtro.get()
            )

            linhas = self.service.listar(status)

            self.popular_tabela([
                (
                    r["id"],
                    (
                        r["id"],
                        r["kitnet"],
                        r["descricao"],
                        r["categoria"],
                        formatar_moeda(r["custo"]),
                        r["status"]
                    ),
                    r["status"]
                )
                for r in linhas
            ])

        self.executar(acao)

    def ao_selecionar(self):
        """Preenche ou ajusta os campos quando uma linha é selecionada."""
        identificador = self.id_selecionado()

        if identificador is None:
            return

        m = self.service.buscar_por_id(identificador)

        if m:
            self.selecionar_opcao_por_id(
                "kitnet",
                m.kitnet_id
            )

            self.definir_valores({
                "categoria": m.categoria,
                "descricao": m.descricao,
                "custo": f"{m.custo:.2f}".replace(".", ",")
            })

    def _custo(self):
        """Lê e valida o custo informado no formulário."""
        texto = self.obter_dados()["custo"]

        return converter_valor(texto) if texto else 0.0

    def abrir(self):
        """Solicita a abertura de uma manutenção."""
        d = self.obter_dados()

        def acao():
            manutencao = Manutencao(
                kitnet_id=self.extrair_id(
                    d["kitnet"],
                    "kitnet"
                ),
                descricao=d["descricao"],
                categoria=d["categoria"],
                custo=self._custo()
            )

            self.service.abrir(
                manutencao,
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Manutenção aberta com sucesso!"
        ):
            self.novo()

    def iniciar(self):
        """Solicita o início da manutenção selecionada."""
        def acao():
            self.service.iniciar(
                self.exigir_selecao("uma manutenção"),
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Manutenção iniciada."
        ):
            self.novo()

    def concluir(self):
        """Solicita a conclusão da manutenção selecionada."""
        def acao():
            identificador = self.exigir_selecao(
                "uma manutenção"
            )

                        # Ao concluir, o serviço registra eventual custo como despesa.
            self.service.concluir(
                identificador,
                self._custo(),
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Manutenção concluída. A kitnet foi liberada, se não houver outras abertas."
        ):
            self.novo()

    def cancelar(self):
        """Solicita o cancelamento do registro selecionado."""
        def acao():
            identificador = self.exigir_selecao(
                "uma manutenção"
            )

            if not self.confirmar(
                f"Cancelar a manutenção #{identificador}?"
            ):
                return

            self.service.cancelar(
                identificador,
                self.usuario["id"]
            )

        if self.executar(acao):
            self.novo()
