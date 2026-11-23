# KITNET_MANAUS

Sistema desktop desenvolvido em Python para gestão de locações, moradores/estudantes, unidades (kitnets), pagamentos, manutenções, despesas e relatórios.

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação.
- `corrigir_encoding.py`: Utilitário para ajuste/correção de codificação de arquivos ou textos.
- `kitnet_manaus.db`: Banco de dados local SQLite.
- `database/`: Conexão com o banco (`conexao.py`), criação de tabelas (`criar_tabelas.py`) e inicialização (`__init__.py`).
- `models/`: Entidades e modelos de dados (`kitnet.py`, `estudante.py`, `locacao.py`, `pagamento.py`, `manutencao.py`, `despesa.py`).
- `services/`: Regras de negócio, operações e exportação (`kitnet_service.py`, `estudante_service.py`, `locacao_service.py`, `pagamento_service.py`, `manutencao_service.py`, `despesa_service.py` / `relatorio_service.py`, `exportacao_service.py`, `usuario_service.py`).
- `interfaces/`: Telas, estilos e menus da interface (`menu.py`, `estilo.py`, `kitnet_interface.py`, `estudante_interface.py`, `locacao_interface.py`, `pagamento_interface.py`, `manutencao_interface.py`, `relatorio_interface.py`).

## Como Executar

1. Acesse a pasta do projeto no terminal:
   ```powershell
   cd C:\Users\nairo\Downloads\KITNET_MANAUS\KITNET_MANAUS
