"""Serviços de autenticação de usuários e registro de histórico."""
from database.conexao import Conexao
from database.criar_tabelas import verificar_senha
from services import ErroNegocio

class UsuarioService:
    """Autentica usuários e fornece os dados necessários às telas."""
    @staticmethod
    def autenticar(login: str, senha: str) -> dict:
        """Confere as credenciais e retorna os dados públicos do usuário autenticado."""
        login = (login or "").strip()
        if not login or not senha:
            raise ErroNegocio("Informe o login e a senha.")

        usuario = Conexao.consultar_um(
            "SELECT id, nome, login, senha_hash, perfil FROM usuarios WHERE login = ?",
            (login,),
        )
        if not usuario or not verificar_senha(senha, usuario["senha_hash"]):
            raise ErroNegocio("Login ou senha inválidos.")

        dados = dict(usuario)
        dados.pop("senha_hash", None)
        return dados

class HistoricoService:
    """Registra e consulta operações realizadas no sistema."""
    @staticmethod
    def registrar(usuario_id: int, operacao: str, descricao: str, conn=None) -> None:
        """Grava uma operação no histórico, usando a conexão recebida quando disponível."""
        sql = """
            INSERT INTO historico (usuario_id, operacao, descricao)
            VALUES (?, ?, ?)
        """
        if conn is not None:
            conn.execute(sql, (usuario_id, operacao, descricao))
        else:
            with Conexao.transacao() as c:
                c.execute(sql, (usuario_id, operacao, descricao))

    @staticmethod
    def listar(limite: int = 200) -> list:
        """Consulta registros no banco e retorna os resultados para a interface."""
        return Conexao.consultar(
            """
            SELECT h.id, u.nome AS usuario, h.operacao, h.descricao, h.data_hora
              FROM historico h
              JOIN usuarios u ON u.id = h.usuario_id
             ORDER BY h.id DESC
             LIMIT ?
            """,
            (limite,),
        )
