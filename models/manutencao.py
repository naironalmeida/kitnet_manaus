"""Modelo de domínio: Manutenção."""

from dataclasses import dataclass

from typing import Optional

@dataclass

class Manutencao:

    """Representa uma manutenção e seus estados permitidos."""
    ABERTA = "Aberta"

    EM_ANDAMENTO = "Em andamento"

    CONCLUIDA = "Concluída"

    CANCELADA = "Cancelada"

    STATUS_VALIDOS = (ABERTA, EM_ANDAMENTO, CONCLUIDA, CANCELADA)

    STATUS_ABERTOS = (ABERTA, EM_ANDAMENTO)

    CATEGORIAS = ("Elétrica", "Hidráulica", "Pintura", "Mobília", "Limpeza", "Estrutural", "Outros")

    kitnet_id: int

    descricao: str

    categoria: str

    custo: float = 0.0

    status: str = ABERTA

    id: Optional[int] = None

    def __post_init__(self):

        """Normaliza os valores recebidos ao criar a instância."""
        self.descricao = (self.descricao or "").strip()

        self.categoria = (self.categoria or "").strip()

    def validar(self):

        """Verifica os campos e regras do registro antes de usá-lo."""
        if not self.kitnet_id:

            raise ValueError("Selecione a kitnet da manutenção.")

        if not self.descricao:

            raise ValueError("Informe a descrição da manutenção.")

        if self.categoria not in self.CATEGORIAS:

            raise ValueError(f"Categoria inválida. Use: {', '.join(self.CATEGORIAS)}.")

        if not isinstance(self.custo, (int, float)) or self.custo < 0:

            raise ValueError("O custo da manutenção não pode ser negativo.")

        if self.status not in self.STATUS_VALIDOS:

            raise ValueError(f"Status inválido. Use: {', '.join(self.STATUS_VALIDOS)}.")

    def esta_aberta(self):

        """Indica se a manutenção ainda está em andamento."""
        return self.status in self.STATUS_ABERTOS

    @classmethod

    def from_row(cls, row):

        """Converte uma linha retornada pelo banco em uma instância do modelo."""
        return cls(**dict(row))
