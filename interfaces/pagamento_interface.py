
"""Tela de Pagamentos."""

from datetime import date

import tkinter as tk
from tkinter import ttk

from interfaces import JanelaBase
from models.pagamento import Pagamento
from services import converter_inteiro, converter_valor, formatar_moeda
from services.locacao_service import LocacaoService
from services.pagamento_service import PagamentoService

class PagamentoInterface(JanelaBase):

    """Tela de cobranças e recebimentos, integrada ao serviço de pagamentos."""
    CAMPOS = [
        ("locacao", "Locação ativa", []),
        ("valor", "Valor da parcela (R$)", None),
        ("vencimento", "Vencimento (AAAA-MM-DD)", None),
        ("quantidade", "Qtde. de mensalidades", None),
        ("data_pagamento", "Data do pagamento (baixa)", None),
    ]

    COLUNAS = [
        ("id", "ID", 50),
        ("locacao", "Locação", 70),
        ("estudante", "Estudante", 190),
        ("kitnet", "Kitnet", 220),
        ("valor", "Valor", 100),
        ("vencimento", "Vencimento", 95),
        ("pagamento", "Pago em", 95),
        ("status", "Status", 80),
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
        super().__init__(master, usuario, "Pagamentos")

        self.service = PagamentoService()
        self.locacoes = {}
        self.filtro = tk.StringVar(value="Todos")

        self._configurar_estilos()
        self._montar()
        self.novo()

    def _configurar_estilos(self):
        """Define estilos visuais usados pelos componentes da tela."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        self.configure(bg=self.FUNDO)
        self.corpo.configure(style="Pagamento.TFrame")

        estilo.configure(
            "Pagamento.TFrame",
            background=self.FUNDO
        )

        estilo.configure(
            "Pagamento.TLabelframe",
            background=self.BRANCO,
            bordercolor="#D5DEE8",
            relief="solid"
        )

        estilo.configure(
            "Pagamento.TLabelframe.Label",
            background=self.BRANCO,
            foreground=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Pagamento.TLabel",
            background=self.BRANCO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Pagamento.Barra.TFrame",
            background=self.FUNDO
        )

        estilo.configure(
            "Pagamento.Barra.TLabel",
            background=self.FUNDO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Pagamento.TEntry",
            padding=6,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO
        )

        estilo.configure(
            "Pagamento.TCombobox",
            padding=6,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO
        )

        estilo.configure(
            "Pagamento.Treeview",
            background=self.BRANCO,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Pagamento.Treeview.Heading",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=8
        )

        estilo.map(
            "Pagamento.Treeview",
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
            text="Gerenciamento de pagamentos",
            bg=self.AZUL_MARINHO,
            fg="#DCE6F1",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

        # Formulário
        formulario = self.criar_formulario(
            self.corpo,
            self.CAMPOS,
            colunas=2,
            titulo="Dados do pagamento"
        )

        formulario.configure(style="Pagamento.TLabelframe")
        formulario.pack(fill="x", pady=(0, 10))

        for widget in formulario.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Pagamento.TLabel")

        for chave, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry):
                widget.configure(style="Pagamento.TEntry")
            else:
                widget.configure(style="Pagamento.TCombobox")

        # Botões
        botoes = ttk.Frame(
            self.corpo,
            style="Pagamento.TFrame"
        )
        botoes.pack(fill="x", pady=(0, 12))

        tk.Button(
            botoes,
            text="Registrar parcela",
            command=self.registrar,
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
            text="Gerar mensalidades",
            command=self.gerar_mensalidades,
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
            text="Dar baixa (selecionado)",
            command=self.dar_baixa,
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
            text="Excluir (selecionado)",
            command=self.excluir,
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

        # Filtro por status
        barra = ttk.Frame(
            self.corpo,
            style="Pagamento.Barra.TFrame"
        )
        barra.pack(fill="x", pady=(0, 8))

        ttk.Label(
            barra,
            text="Filtrar por status:",
            style="Pagamento.Barra.TLabel"
        ).pack(side="left")

        combo = ttk.Combobox(
            barra,
            textvariable=self.filtro,
            state="readonly",
            width=14,
            values=("Todos",) + Pagamento.STATUS_VALIDOS
        )

        combo.pack(side="left", padx=6)
        combo.configure(style="Pagamento.TCombobox")

        combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self.carregar()
        )

        # Tabela
        self.criar_tabela(
            self.corpo,
            self.COLUNAS
        ).pack(fill="both", expand=True, pady=(4, 0))

        self.tree.configure(style="Pagamento.Treeview")

        self.tree.tag_configure(
            "Atrasado",
            foreground=self.VERMELHO
        )

        self.tree.tag_configure(
            "Pago",
            foreground=self.VERDE
        )

    def novo(self):
        """Prepara o formulário para um novo registro."""
        self.limpar_formulario()
        self.carregar_opcoes()

        hoje = date.today().isoformat()

        self.definir_valores({
            "vencimento": hoje,
            "quantidade": "6",
            "data_pagamento": hoje
        })

        self.carregar()

    def carregar_opcoes(self):
        """Busca no serviço os registros disponíveis para seleção."""
        def acao():
            self.locacoes = {
                r["id"]: r
                for r in LocacaoService().listar_ativas()
            }

            self.definir_opcoes(
                "locacao",
                [
                    f"{r['id']} - {r['estudante']} / {r['kitnet']}"
                    for r in self.locacoes.values()
                ]
            )

        self.executar(acao)

    def _locacao_escolhida(self, _evento=None):
        """Identifica a locação selecionada no formulário."""
        try:
            loc = self.locacoes.get(
                self.extrair_id(
                    self.vars["locacao"].get(),
                    "locação"
                )
            )
        except ValueError:
            return

        if loc:
            self.definir_valores({
                "valor": f"{loc['valor_contratado']:.2f}".replace(".", ",")
            })

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
                        r["locacao_id"],
                        r["estudante"],
                        r["kitnet"],
                        formatar_moeda(r["valor"]),
                        r["vencimento"],
                        r["data_pagamento"],
                        r["status"]
                    ),
                    r["status"]
                )
                for r in linhas
            ])

        self.executar(acao)

    def registrar(self):
        """Grava uma operação no histórico, usando a conexão recebida quando disponível."""
        d = self.obter_dados()

        def acao():
            pagamento = Pagamento(
                locacao_id=self.extrair_id(
                    d["locacao"],
                    "locação"
                ),
                valor=converter_valor(d["valor"]),
                vencimento=d["vencimento"]
            )

            self.service.registrar(
                pagamento,
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Parcela registrada com sucesso!"
        ):
            self.carregar()

    def gerar_mensalidades(self):
        """Solicita a geração de cobranças mensais para a locação."""
        d = self.obter_dados()
        resultado = {}

        def acao():
            resultado["qtd"] = self.service.gerar_mensalidades(
                self.extrair_id(
                    d["locacao"],
                    "locação"
                ),
                converter_inteiro(
                    d["quantidade"],
                    "Quantidade de mensalidades"
                ),
                d["vencimento"],
                self.usuario["id"]
            )

        if self.executar(acao):
            self.carregar()

            self.executar(
                lambda: None,
                f"{resultado['qtd']} mensalidade(s) gerada(s) com sucesso!"
            )

    def dar_baixa(self):
        """Registra o recebimento do pagamento selecionado."""
        data = self.obter_dados()["data_pagamento"]

        def acao():
            identificador = self.exigir_selecao(
                "um pagamento"
            )

                        # O serviço registra o recebimento e atualiza o histórico.
            self.service.baixar(
                identificador,
                data,
                self.usuario["id"]
            )

        if self.executar(
            acao,
            "Pagamento baixado com sucesso!"
        ):
            self.carregar()

    def excluir(self):
        """Remove o registro selecionado respeitando as regras de negócio."""
        def acao():
            identificador = self.exigir_selecao(
                "um pagamento"
            )

            if not self.confirmar(
                f"Excluir o pagamento #{identificador}?"
            ):
                return

            self.service.excluir(
                identificador,
                self.usuario["id"]
            )

            self.carregar()

        self.executar(acao)
