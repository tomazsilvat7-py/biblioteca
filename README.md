# 📚 Sistema de Biblioteca Escolar

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-GUI-green?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>Sistema desktop completo para gerenciamento de bibliotecas escolares.</b><br>
  Cadastro de livros, controle de empréstimos, devoluções e muito mais — tudo com uma interface moderna e intuitiva.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square" alt="Platform">
</p>

---

## 📋 Índice

- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Banco de Dados](#-banco-de-dados)
- [Arquitetura](#-arquitetura)
- [Validações e Regras de Negócio](#-validações-e-regras-de-negócio)
- [Tratamento de Erros](#-tratamento-de-erros)
- [Tema Escuro/Claro](#-tema-escuroclaro)
- [Contribuição](#-contribuição)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 🎨 Demonstração

O sistema possui duas abas principais com interfaces modernas e responsivas:

| Aba Livros | Aba Empréstimos |
|:---:|:---:|
| Cadastro com título, autor, categoria e quantidade | Cadastro com dados do aluno, livro e data de vencimento |
| Tabela com todos os livros cadastrados | Tabela com todos os empréstimos ativos |
| Botões de cadastrar e excluir | Botões de emprestar e devolver |

> **Tema escuro (padrão)** e **tema claro** — alternância em tempo real pelo botão no header.

---

## ✅ Funcionalidades

### 📖 Gestão de Livros
- **Cadastro** de livros com título, autor, categoria e quantidade
- **Listagem** completa em tabela com scroll
- **Exclusão** com verificação de empréstimos ativos (impede exclusão se houver empréstimos vinculados)
- **10 categorias pré-definidas**: Conto, Poesia, Ficção Científica, Filosofia, Ciências, Romance, Tecnologia, Aventura, Biografia, Terror

### 📋 Gestão de Empréstimos
- **Empréstimo** de livros com registro completo do aluno (nome, sobrenome, telefone, série)
- **Data de vencimento** com seleção por dropdown (dia/mês/ano)
- **Devolução** com restauração automática do estoque
- **Listagem** de empréstimos ativos com dados do aluno e livro

### 🔒 Regras de Negócio
- Limite de **5 empréstimos por aluno**
- Impedir empréstimo de livros com **estoque zerado**
- Impedir **empréstimo duplicado** (mesmo aluno + mesmo livro)
- Impedir **exclusão de livros** com empréstimos ativos
- Impedir **datas de vencimento retroativas**
- **Transações atômicas** para empréstimos e devoluções

### 🛡️ Segurança
- **Sanitização** de entradas (remoção de caracteres de controle)
- **Limite de caracteres** por campo
- **Validação** de números positivos para quantidade e ID
- **Prepared statements** (parâmetros SQL) em todas as queries — prevenção contra SQL Injection
- **Foreign keys** com `ON DELETE RESTRICT`
- **Rollback** automático em caso de erro

---

## 🛠 Tecnologias

| Tecnologia | Versão | Uso |
|:---|:---:|:---|
| [Python](https://www.python.org/) | 3.10+ | Linguagem principal |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | 5.x | Interface gráfica moderna |
| [SQLite](https://www.sqlite.org/) | 3.x | Banco de dados embarcado |
| [ttk (Tkinter)](https://docs.python.org/3/library/tkinter.ttk.html) | built-in | Treeview (tabelas) |

### Por que essas tecnologias?

- **CustomTkinter**: fornece widgets modernos com cantos arredondados, temas escuro/claro nativos e visual profissional — sem a complexidade de frameworks como PyQt
- **SQLite**: banco de dados serverless, zero configuração, ideal para aplicações desktop de pequeno/médio porte
- **Python**: tipagem dinâmica, vasta biblioteca padrão, multiplataforma

---

## 📁 Estrutura do Projeto

```
biblioteca/
├── biblioteca.py          # Código-fonte completo (GUI + banco + lógica)
├── biblioteca.db          # Banco de dados SQLite (gerado automaticamente)
├── README.md              # Esta documentação
├── LICENSE                # Licença MIT
├── CONTRIBUTING.md        # Guia de contribuição
├── .gitignore             # Arquivos ignorados pelo Git
└── docs/
    └── ARCHITECTURE.md    # Documentação técnica detalhada
```

> **Nota**: O projeto é inteiramente contido em um único arquivo Python para simplicidade de distribuição. O banco de dados `biblioteca.db` é criado automaticamente na primeira execução.

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.10** ou superior
- **pip** (gerenciador de pacotes do Python)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEEMG/biblioteca.git
cd biblioteca

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 3. Instale as dependências
pip install customtkinter

# 4. Execute o sistema
python biblioteca.py
```

### Gerar executável (opcional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed biblioteca.py
```

O executável será gerado na pasta `dist/`.

---

## 📖 Como Usar

### 1. Cadastrar Livros

1. Acesse a aba **"📖 Livros"**
2. Preencha os campos:
   - **Título**: nome do livro (obrigatório)
   - **Autor**: nome do autor (obrigatório)
   - **Categoria**: selecione no dropdown (opcional)
   - **Quantidade**: número de exemplares (obrigatório)
3. Clique em **"✅ Cadastrar"**
4. O livro aparecerá na tabela abaixo

### 2. Realizar Empréstimo

1. Acesse a aba **"📋 Empréstimos"**
2. Preencha os dados do aluno:
   - **Nome** e **Sobrenome**
   - **Telefone** e **Série**
3. Informe o **ID do livro** (visível na aba Livros)
4. Selecione a **data de vencimento** nos dropdowns
5. Clique em **"📤 Emprestar Livro"**

### 3. Devolver Livro

1. Acesse a aba **"📋 Empréstimos"**
2. Selecione o empréstimo na tabela
3. Clique em **"📖 Devolver Livro"**
4. O estoque do livro será restaurado automaticamente

### 4. Excluir Livro

1. Acesse a aba **"📖 Livros"**
2. Selecione o livro na tabela
3. Clique em **"🗑️ Excluir"**
4. Confirme a exclusão

> ⚠️ Livros com empréstimos ativos **não podem** ser excluídos.

---

## 🗄 Banco de Dados

### Diagrama Entidade-Relacionamento

```
┌─────────────────────────┐         ┌──────────────────────────────────────┐
│         livros          │         │             emprestimos               │
├─────────────────────────┤         ├──────────────────────────────────────┤
│ id          INTEGER PK  │──┐      │ id          INTEGER PK               │
│ titulo      TEXT    NN  │  │      │ nome        TEXT    NN               │
│ autor       TEXT    NN  │  │      │ sobrenome   TEXT                     │
│ categoria   TEXT        │  └──────│ telefone    TEXT                     │
│ quantidade  INTEGER NN  │   1:N   │ serie       TEXT                     │
│             CHECK ≥ 0   │         │ livro_id    INTEGER NN FK → livros   │
└─────────────────────────┘         │ data        TEXT    NN               │
                                    │ vencimento  TEXT    NN               │
                                    └──────────────────────────────────────┘
```

### Tabela `livros`

| Coluna | Tipo | Restrições | Descrição |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `titulo` | TEXT | NOT NULL | Título do livro (máx. 200 caracteres) |
| `autor` | TEXT | NOT NULL | Nome do autor (máx. 150 caracteres) |
| `categoria` | TEXT | — | Categoria literária |
| `quantidade` | INTEGER | NOT NULL, DEFAULT 0, CHECK ≥ 0 | Exemplares disponíveis |

### Tabela `emprestimos`

| Coluna | Tipo | Restrições | Descrição |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `nome` | TEXT | NOT NULL | Nome do aluno (máx. 100 caracteres) |
| `sobrenome` | TEXT | — | Sobrenome do aluno |
| `telefone` | TEXT | — | Telefone de contato (máx. 20 caracteres) |
| `serie` | TEXT | — | Série/turma do aluno (máx. 50 caracteres) |
| `livro_id` | INTEGER | NOT NULL, FK → livros(id), ON DELETE RESTRICT | Livro emprestado |
| `data` | TEXT | NOT NULL | Data do empréstimo (DD/MM/AAAA) |
| `vencimento` | TEXT | NOT NULL | Data de devolução (DD/MM/AAAA) |

### Configurações do SQLite

```sql
PRAGMA journal_mode=WAL;    -- Write-Ahead Logging para melhor concorrência
PRAGMA foreign_keys=ON;      -- Ativa integridade referencial
```

---

## 🏗 Arquitetura

### Visão Geral

O sistema segue uma arquitetura **monolítica em camadas** contida em um único arquivo:

```
┌─────────────────────────────────────────────┐
│              Camada de Apresentação          │
│         (CustomTkinter + ttk Treeview)       │
├─────────────────────────────────────────────┤
│              Camada de Validação             │
│    (sanitizar_texto, validar_numero_positivo,│
│     validar_data_vencimento)                 │
├─────────────────────────────────────────────┤
│              Camada de Negócio               │
│  (cadastrar_livro, excluir_livro,           │
│   emprestar_livro, devolver_livro)           │
├─────────────────────────────────────────────┤
│              Camada de Dados                 │
│         (SQLite + sqlite3 API)               │
└─────────────────────────────────────────────┘
```

### Fluxo de uma Operação (Ex: Empréstimo)

```
Usuário preenche formulário
        │
        ▼
Validação dos campos (sanitização + regras)
        │
        ▼
Verificações de negócio
  ├── Livro existe?
  ├── Estoque > 0?
  ├── Não é duplicado?
  ├── Limite de empréstimos OK?
  └── Data de vencimento válida?
        │
        ▼
BEGIN TRANSACTION
  ├── INSERT INTO emprestimos
  └── UPDATE livros SET quantidade - 1
        │
        ▼
COMMIT → Atualiza tabelas GUI
```

> Para detalhes técnicos completos, consulte [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## ✅ Validações e Regras de Negócio

### Validações de Entrada

| Campo | Validação |
|:---|:---|
| Texto (título, autor, nome) | Sanitização + limite de caracteres |
| Quantidade | Número inteiro ≥ 0 |
| ID do livro | Número inteiro válido |
| Data de vencimento | Data válida e não retroativa |
| Todos os campos | Remoção de caracteres de controle (`\x00-\x1f`) |

### Regras de Negócio

| Regra | Implementação |
|:---|:---|
| Limite de empréstimos por aluno | Constante `LIMITE_EMPRESTIMOS_POR_USUARIO = 5` |
| Estoque não negativo | `CHECK(quantidade >= 0)` no schema + verificação em código |
| Sem empréstimo duplicado | Verificação de `(nome, sobrenome, livro_id)` antes de emprestar |
| Sem exclusão com empréstimos | Contagem de empréstivos ativos antes de excluir |
| Integridade referencial | `FOREIGN KEY ... ON DELETE RESTRICT` |
| Transações atômicas | `BEGIN TRANSACTION` + `COMMIT`/`ROLLBACK` |

---

## 🛡 Tratamento de Erros

Todas as operações de banco de dados são protegidas por blocos `try/except`:

- **`sqlite3.Error`**: rollback automático + mensagem de erro ao usuário
- **`ValueError`/`IndexError`**: capturados na devolução (ID inválido)
- **Confirmação do usuário**: exclusão e remoção de órfãos pedem confirmação via `messagebox.askyesno`

---

## 🌙 Tema Escuro/Claro

O sistema suporta alternância entre temas em **tempo real** sem reinicialização:

| Elemento | Tema Escuro | Tema Claro |
|:---|:---|:---|
| Background | `#1a1a2e` (azul escuro) | `#f0f0f5` (cinza claro) |
| Cards | `#16213e` (azul médio) | `#ffffff` (branco) |
| Texto | `#ffffff` (branco) | `#1a1a2e` (azul escuro) |
| Entradas | `#0f3460` (azul profundo) | `#f5f5f5` (cinza claro) |

A troca atualiza: janela, header, cards, labels, entradas, treeviews e comboboxes.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Veja o guia em [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
# Fork e clone
git clone https://github.com/SEEMG/biblioteca.git

# Crie uma branch
git checkout -b feature/minha-melhoria

# Commit e push
git commit -m "feat: adiciona funcionalidade X"
git push origin feature/minha-melhoria

# Abra um Pull Request
```

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**Tomaz**
Perfil: https://github.com/tomazsilvat7-py
---

<p align="center">
  Feito com ❤️ para a comunidade escolar
</p>
