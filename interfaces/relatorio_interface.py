
"""Tela de Relatórios."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from interfaces import JanelaBase
from services.relatorio_service import RelatorioService
from services.exportacao_service import ExportacaoService

class RelatorioInterface(JanelaBase):
    # Cores da interface
    """Tela que consulta relatórios e aciona a exportação dos dados."""
    AZUL_MARINHO = "#142B46"
    AZUL = "#2878B9"
    FUNDO = "#F1F5F9"
    BRANCO = "#FFFFFF"
    TEXTO = "#26364A"
    CINZA = "#64748B"
    VERDE = "#218838"

    def __init__(self, master, usuario):
        """Inicializa a janela e prepara seus componentes e dependências."""
        super().__init__(master, usuario, "Relatórios", "1100x650")

        self.service = RelatorioService()
        self.catalogo = self.service.catalogo()

        self.escolhido = tk.StringVar(
            value=next(iter(self.catalogo))
        )

        self.total = tk.StringVar(value="")

        self._configurar_estilos()
        self._montar()
        self.gerar()

    def _configurar_estilos(self):
        """Define estilos visuais usados pelos componentes da tela."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        self.configure(bg=self.FUNDO)
        self.corpo.configure(style="Relatorio.TFrame")

        estilo.configure(
            "Relatorio.TFrame",
            background=self.FUNDO
        )

        estilo.configure(
            "Relatorio.TLabel",
            background=self.FUNDO,
            foreground=self.TEXTO,
            font=("Segoe UI", 9)
        )
        estilo.configure(
            "Relatorio.TLabelframe",
            background=self.BRANCO,
            bordercolor="#D5DEE8",
            relief="solid"
        )
        estilo.configure(
            "Relatorio.TLabelframe.Label",
            background=self.BRANCO,
            foreground=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        )
        estilo.configure(
            "Relatorio.TCombobox",
            padding=6,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO
        )
        estilo.configure(
            "Relatorio.Treeview",
            background=self.BRANCO,
            fieldbackground=self.BRANCO,
            foreground=self.TEXTO,
            rowheight=32,
            font=("Segoe UI", 9)
        )
        estilo.configure(
            "Relatorio.Treeview.Heading",
            background=self.AZUL_MARINHO,
            foreground=self.BRANCO,
            font=("Segoe UI", 9, "bold"),
            padding=9
        )
        estilo.map(
            "Relatorio.Treeview",
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
            text="Relatórios e exportação de dados",
            bg=self.AZUL_MARINHO,
            fg="#DCE6F1",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))
        # Painel de seleção de relatório
        painel = ttk.LabelFrame(
            self.corpo,
            text="Consultar relatórios",
            style="Relatorio.TLabelframe",
            padding=12
        )
        painel.pack(fill="x", pady=(0, 10))

        barra = ttk.Frame(
            painel,
            style="Relatorio.TFrame"
        )
        barra.pack(fill="x")

        ttk.Label(
            barra,
            text="Relatório:",
            style="Relatorio.TLabel"
        ).pack(side="left")

        combo = ttk.Combobox(
            barra,
            textvariable=self.escolhido,
            state="readonly",
            width=32,
            values=list(self.catalogo),
            style="Relatorio.TCombobox"
        )
        combo.pack(side="left", padx=6)

        combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self.gerar()
        )

        # Botão gerar
        tk.Button(
            barra,
            text="Gerar / Atualizar",
            command=self.gerar,
            bg=self.AZUL,
            fg=self.BRANCO,
            activebackground=self.AZUL_MARINHO,
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="left", padx=6)

        # Total de registros
        total_frame = tk.Frame(
            barra,
            bg=self.FUNDO
        )
        total_frame.pack(side="right")

        tk.Label(
            total_frame,
            textvariable=self.total,
            bg=self.FUNDO,
            fg=self.AZUL_MARINHO,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right")

        # Painel de exportações
        exportacao = ttk.LabelFrame(
            self.corpo,
            text="Exportar dados",
            style="Relatorio.TLabelframe",
            padding=12
        )
        exportacao.pack(fill="x", pady=(0, 10))

        botoes_exportacao = ttk.Frame(
            exportacao,
            style="Relatorio.TFrame"
        )
        botoes_exportacao.pack(fill="x")

        tk.Button(
            botoes_exportacao,
            text="Pagamentos (.xlsx/.xls)",
            command=self.exportar_pagamentos,
            bg=self.VERDE,
            fg=self.BRANCO,
            activebackground="#176B2C",
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botoes_exportacao,
            text="Alunos (.txt)",
            command=self.exportar_alunos,
            bg=self.AZUL,
            fg=self.BRANCO,
            activebackground=self.AZUL_MARINHO,
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        ).pack(side="left", padx=8)

        tk.Button(
            botoes_exportacao,
            text="Kitnets (.json)",
            command=self.exportar_kitnets,
            bg=self.AZUL_MARINHO,
            fg=self.BRANCO,
            activebackground=self.AZUL,
            activeforeground=self.BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        ).pack(side="left", padx=8)

        # Tabela de relatórios
        tabela = ttk.LabelFrame(
            self.corpo,
            text="Resultado do relatório",
            style="Relatorio.TLabelframe",
            padding=8
        )
        tabela.pack(fill="both", expand=True)

        self.criar_tabela(
            tabela,
            [("c0", "", 100)]
        ).pack(fill="both", expand=True)

        self.tree.configure(
            style="Relatorio.Treeview"
        )

    def gerar(self):

        """Executa o relatório escolhido e atualiza a visualização."""
        def acao():
            colunas, linhas = self.catalogo[
                self.escolhido.get()
            ]()

            self.configurar_colunas([
                (f"c{i}", nome, 150)
                for i, nome in enumerate(colunas)
            ])

            self.popular_tabela([
                (i, linha)
                for i, linha in enumerate(linhas)
            ])

            self.total.set(
                f"{len(linhas)} registro(s)"
            )

        self.executar(acao)

    def exportar_pagamentos(self):
        """Exporta os pagamentos consultados para uma planilha Excel."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar Planilha de Pagamentos",
            defaultextension=".xlsx",
            initialfile="pagamentos_kitnet_manaus.xlsx",
            filetypes=[
                ("Excel Moderno (*.xlsx)", "*.xlsx"),
                ("Excel 97-2003 (*.xls)", "*.xls")
            ],
            parent=self
        )

        if not caminho:
            return

        try:
            total = ExportacaoService.exportar_pagamentos_excel(
                caminho
            )

            messagebox.showinfo(
                "Sucesso",
                f"{total} pagamentos exportados com sucesso!",
                parent=self
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self
            )

    def exportar_alunos(self):
        """Exporta os dados de estudantes para um arquivo de texto."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar Lista de Alunos (TXT)",
            defaultextension=".txt",
            initialfile="alunos_cadastrados.txt",
            filetypes=[
                ("Arquivo de Texto (*.txt)", "*.txt")
            ],
            parent=self
        )

        if not caminho:
            return

        try:
            total = ExportacaoService.exportar_estudantes_txt(
                caminho
            )

            messagebox.showinfo(
                "Sucesso",
                f"{total} alunos exportados com sucesso!",
                parent=self
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self
            )

    def exportar_kitnets(self):
        """Exporta os dados de kitnets para um arquivo JSON."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar Kitnets (JSON)",
            defaultextension=".json",
            initialfile="kitnets_cadastradas.json",
            filetypes=[
                ("Arquivo JSON (*.json)", "*.json")
            ],
            parent=self
        )

        if not caminho:
            return

        try:
            total = ExportacaoService.exportar_kitnets_json(
                caminho
            )

            messagebox.showinfo(
                "Sucesso",
                f"{total} kitnets exportadas com sucesso!",
                parent=self
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self
            )
