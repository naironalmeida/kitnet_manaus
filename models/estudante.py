"""Modelo de domínio: Estudante."""

import re

from dataclasses import dataclass

from typing import Optional

@dataclass

class Estudante:

    """Representa os dados e validações de um estudante cadastrado."""
    nome: str

    cpf: str

    telefone: str

    email: str

    curso: str

    instituicao: str

    id: Optional[int] = None

    def __post_init__(self):

        """Normaliza os valores recebidos ao criar a instância."""
        self.nome = (self.nome or "").strip()

        self.cpf = re.sub(r"\D", "", self.cpf or "")

        self.telefone = re.sub(r"\D", "", self.telefone or "")

        self.email = (self.email or "").strip().lower()

        self.curso = (self.curso or "").strip()

        self.instituicao = (self.instituicao or "").strip()

    def validar(self):
    # Nome: somente letras e espaços
        """Verifica os campos e regras do registro antes de usá-lo."""
        if not self.nome:
            raise ValueError("Informe o nome do estudante.")

        if not re.fullmatch(r"[^\W\d_]+(?:\s+[^\W\d_]+)*", self.nome):
            raise ValueError("O nome deve conter somente letras e espaços.")

        # CPF
        if len(self.cpf) != 11 or len(set(self.cpf)) == 1:
            raise ValueError("CPF inválido: informe 11 dígitos.")

        # Telefone
        if len(self.telefone) not in (10, 11):
            raise ValueError("Telefone inválido: informe DDD + número (10 ou 11 dígitos).")

    # E-mail
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", self.email):
            raise ValueError("E-mail inválido.")

    # Curso: somente letras e espaços
        if not self.curso:
            raise ValueError("Informe o curso do estudante.")

        if not re.fullmatch(r"[^\W\d_]+(?:\s+[^\W\d_]+)*", self.curso):
            raise ValueError("O curso deve conter somente letras e espaços.")

    # Instituição
        if not self.instituicao:
            raise ValueError("Informe a instituição de ensino.")

    def cpf_formatado(self):

        """Retorna o CPF formatado para exibição."""
        c = self.cpf

        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c) == 11 else c

    def telefone_formatado(self):

        """Retorna o telefone formatado para exibição."""
        t = self.telefone

        if len(t) == 11:

            return f"({t[:2]}) {t[2:7]}-{t[7:]}"

        if len(t) == 10:

            return f"({t[:2]}) {t[2:6]}-{t[6:]}"

        return t

    @classmethod

    def from_row(cls, row):

        """Converte uma linha retornada pelo banco em uma instância do modelo."""
        return cls(**dict(row))
