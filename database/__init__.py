"""Camada de banco de dados do KITNET MANAUS."""
from database.conexao import Conexao # chama a classe conexao que está dentro da conexao.py
from database.criar_tabelas import criar_tabelas #busca a função criar tabelas que está dentro do arquivo criar tabelas.py

__all__ = ["Conexao", "criar_tabelas"]
