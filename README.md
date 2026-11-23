# 🏠 Kitnet Manaus

Sistema desktop desenvolvido em **Python** para gerenciamento de locações de kitnets, estudantes, pagamentos, manutenções, despesas e relatórios.

O projeto tem como objetivo facilitar o controle administrativo de imóveis e organizar as informações relacionadas aos processos de locação.

## 🚀 Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Tkinter:** desenvolvimento da interface gráfica.
- **SQLite:** gerenciamento e armazenamento dos dados.
- **Programação Orientada a Objetos (POO):** organização e estruturação do código.

## ⚙️ Funcionalidades

- Cadastro e gerenciamento de kitnets.
- Cadastro e gerenciamento de estudantes.
- Consulta de imóveis cadastrados.
- Gerenciamento de locações.
- Controle de pagamentos.
- Registro de manutenções.
- Controle de despesas.
- Geração e exportação de relatórios.

## 📁 Estrutura do projeto

O projeto está organizado em módulos para facilitar a manutenção e a separação das responsabilidades.

- `main.py`: ponto de entrada da aplicação.
- `corrigir_encoding.py`: utilitário para ajuste e correção de codificação de arquivos ou textos.
- `kitnet_manaus.db`: banco de dados local SQLite.

### Organização dos módulos

**database/**
- `conexao.py`: conexão com o banco de dados.
- `criar_tabelas.py`: criação das tabelas.
- `__init__.py`: inicialização do módulo.

**models/**
- `kitnet.py`
- `estudante.py`
- `locacao.py`
- `pagamento.py`
- `manutencao.py`
- `despesa.py`

Responsável pela representação das entidades e modelos de dados.

**services/**
- `kitnet_service.py`
- `estudante_service.py`
- `locacao_service.py`
- `pagamento_service.py`
- `manutencao_service.py`
- `despesa_service.py`
- `relatorio_service.py`
- `exportacao_service.py`
- `usuario_service.py`

Responsável pelas regras de negócio, operações e processamento dos dados.

**interfaces/**
- `menu.py`
- `estilo.py`
- `kitnet_interface.py`
- `estudante_interface.py`
- `locacao_interface.py`
- `pagamento_interface.py`
- `manutencao_interface.py`
- `relatorio_interface.py`

Responsável pelas telas, componentes visuais e interação com o usuário.

## 🗄️ Banco de dados

O sistema utiliza SQLite para armazenar localmente as informações relacionadas aos imóveis, estudantes, locações, pagamentos, manutenções e despesas.

A conexão e a criação das tabelas são organizadas dentro do módulo `database/`.

## 💻 Como executar o projeto

### 1. Pré-requisitos

- Python 3 instalado.
- Git instalado (opcional, para clonar o repositório).

### 2. Clonar o repositório

```bash
git clone https://github.com/naironalmeida/KITNET_MANAUS.git
```

### 3. Entrar na pasta do projeto

```bash
cd KITNET_MANAUS
```

### 4. Executar a aplicação

```bash
python main.py
```

## 🎯 Objetivo acadêmico

Projeto desenvolvido no contexto da graduação em Engenharia de Software, com foco na aplicação prática de conceitos de:

- Programação Orientada a Objetos.
- Desenvolvimento de aplicações desktop.
- Organização e modularização de código.
- Modelagem e integração com banco de dados.
- Separação de responsabilidades.

## 👨‍💻 Desenvolvedores

Projeto desenvolvido em equipe, com participação de:

- Nairon Almeida
- Nai777230

---

**Kitnet Manaus** — Sistema de gerenciamento de locações desenvolvido com Python.
