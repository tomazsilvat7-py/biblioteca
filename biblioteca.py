# =========================================
# SISTEMA DE BIBLIOTECA ESCOLAR PROFISSIONAL
# Python + CustomTkinter + SQLite
# =========================================

import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
import re
import os
import sys
# =========================================
# BANCO DE DADOS
# =========================================

if getattr(sys, 'frozen', False):
    pasta_base = os.path.dirname(sys.executable)
else:
    pasta_base = os.path.dirname(os.path.abspath(__file__))

caminho_banco = os.path.join(
    pasta_base,
    "biblioteca.db"
)

conn = sqlite3.connect(caminho_banco)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    categoria TEXT,
    quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sobrenome TEXT,
    telefone TEXT,
    serie TEXT,
    livro_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    vencimento TEXT NOT NULL,
    FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE RESTRICT
)
""")

try:
    cursor.execute("ALTER TABLE emprestimos ADD COLUMN vencimento TEXT NOT NULL DEFAULT ''")
except sqlite3.OperationalError:
    pass

conn.commit()

# =========================================
# CONFIGURAÇÃO CUSTOMTKINTER
# =========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# =========================================
# CONSTANTES
# =========================================

COR_PRIMARIA = "#00b894"
COR_PRIMARIA_HOVER = "#019875"
COR_PERIGO = "#e53935"
COR_PERIGO_HOVER = "#c62828"
COR_AVISO = "#ff9800"
COR_AVISO_HOVER = "#f57c00"
COR_INFO = "#2196F3"
COR_INFO_HOVER = "#1976D2"
COR_BG = "#1a1a2e"
COR_CARD = "#16213e"
COR_CARD_LIGHT = "#1e2a4a"
COR_TEXT = "#ffffff"
COR_TEXT_MUTED = "#a0a0b0"
COR_ENTRY = "#0f3460"
MAX_TITULO = 200
MAX_AUTOR = 150
MAX_NOME = 100
MAX_TELEFONE = 20
MAX_SERIE = 50
LIMITE_EMPRESTIMOS_POR_USUARIO = 5

# =========================================
# JANELA PRINCIPAL
# =========================================

janela = ctk.CTk()
janela.title("Sistema de Biblioteca Escolar")
janela.geometry("1400x900")

# =========================================
# FECHAMENTO SEGURO DA JANELA
# =========================================

def fechar_janela():
    try:
        conn.commit()
        conn.close()
    except Exception:
        pass
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar_janela)

# =========================================
# ESTILO TREEVIEW
# =========================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=COR_CARD,
    foreground=COR_TEXT,
    fieldbackground=COR_CARD,
    rowheight=36,
    font=("Segoe UI", 10),
    borderwidth=0,
)
style.map(
    "Treeview",
    background=[("selected", COR_PRIMARIA)],
    foreground=[("selected", "white")],
)
style.configure(
    "Treeview.Heading",
    background=COR_PRIMARIA,
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
    padding=8,
)
style.map("Treeview.Heading", background=[("active", COR_PRIMARIA_HOVER)])

style.configure(
    "TCombobox",
    fieldbackground=COR_ENTRY,
    background=COR_ENTRY,
    foreground=COR_TEXT,
    font=("Segoe UI", 10),
)

# =========================================
# LAYOUT PRINCIPAL
# =========================================

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

main_canvas = ctk.CTkScrollableFrame(
    janela,
    fg_color=COR_BG,
    scrollbar_button_color=COR_PRIMARIA,
    scrollbar_button_hover_color=COR_PRIMARIA_HOVER,
)
main_canvas.grid(row=0, column=0, sticky="nsew")
main_canvas.grid_columnconfigure(0, weight=1)

# =========================================
# HEADER
# =========================================

header_frame = ctk.CTkFrame(main_canvas, fg_color=COR_CARD, corner_radius=16, height=80)
header_frame.pack(fill="x", padx=20, pady=(15, 5))
header_frame.pack_propagate(False)

header_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
header_inner.pack(fill="both", expand=True, padx=20)

titulo_label = ctk.CTkLabel(
    header_inner,
    text="📚  SISTEMA DE BIBLIOTECA",
    font=("Segoe UI", 28, "bold"),
    text_color=COR_PRIMARIA,
)
titulo_label.pack(side="left", pady=15)

btn_tema = ctk.CTkButton(
    header_inner,
    text="🌙  Alternar Tema",
    command=lambda: alternar_tema(),
    width=160,
    height=40,
    font=("Segoe UI", 12, "bold"),
    fg_color=COR_PRIMARIA,
    hover_color=COR_PRIMARIA_HOVER,
    corner_radius=10,
)
btn_tema.pack(side="right", pady=15)

# =========================================
# ABAS (TABVIEW)
# =========================================

tabview = ctk.CTkTabview(
    main_canvas,
    fg_color=COR_CARD,
    segmented_button_fg_color=COR_CARD_LIGHT,
    segmented_button_selected_color=COR_PRIMARIA,
    segmented_button_selected_hover_color=COR_PRIMARIA_HOVER,
    segmented_button_unselected_color=COR_CARD_LIGHT,
    segmented_button_unselected_hover_color="#253560",
    corner_radius=16,
)
tabview.pack(fill="both", expand=True, padx=20, pady=10)

tab_livros = tabview.add("  📖  Livros  ")
tab_emprestimos = tabview.add("  📋  Empréstimos  ")

tab_livros.grid_columnconfigure(0, weight=1)
tab_emprestimos.grid_columnconfigure(0, weight=1)

# =========================================
# LISTAS PARA CONTROLE DE TEMA
# =========================================

cards = []
card_labels = []
all_entries = []

# =========================================
# VALIDAÇÕES DE ENTRADA
# =========================================


def sanitizar_texto(valor, maximo):
    valor = valor.strip()
    if len(valor) > maximo:
        valor = valor[:maximo]
    valor = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", valor)
    return valor


def validar_numero_positivo(valor):
    if not valor or not valor.strip():
        return False
    try:
        n = int(valor.strip())
        return n >= 0
    except (ValueError, TypeError):
        return False


def validar_data_vencimento(dia, mes, ano):
    if not dia or not mes or not ano:
        return False, "Preencha dia, mês e ano."
    try:
        d = int(dia)
        m = int(mes)
        a = int(ano)
        data_venc = date(a, m, d)
        if data_venc < date.today():
            return False, "A data de vencimento não pode ser retroativa."
        return True, ""
    except ValueError:
        return False, "Data de vencimento inválida."


# =========================================
# FUNÇÃO TEMA
# =========================================

tema_escuro = True


def alternar_tema():
    global tema_escuro, COR_BG, COR_CARD, COR_CARD_LIGHT, COR_ENTRY, COR_TEXT, COR_TEXT_MUTED

    tema_escuro = not tema_escuro

    if tema_escuro:
        ctk.set_appearance_mode("dark")
        novas_cores = {
            "bg": "#1a1a2e",
            "card": "#16213e",
            "card_light": "#1e2a4a",
            "entry": "#0f3460",
            "text": "#ffffff",
            "text_muted": "#a0a0b0",
        }
    else:
        ctk.set_appearance_mode("light")
        novas_cores = {
            "bg": "#f0f0f5",
            "card": "#ffffff",
            "card_light": "#e8e8f0",
            "entry": "#f5f5f5",
            "text": "#1a1a2e",
            "text_muted": "#555570",
        }

    COR_BG = novas_cores["bg"]
    COR_CARD = novas_cores["card"]
    COR_CARD_LIGHT = novas_cores["card_light"]
    COR_ENTRY = novas_cores["entry"]
    COR_TEXT = novas_cores["text"]
    COR_TEXT_MUTED = novas_cores["text_muted"]

    main_canvas.configure(fg_color=COR_BG)
    header_frame.configure(fg_color=COR_CARD)

    style.configure("Treeview", background=COR_CARD, foreground=COR_TEXT, fieldbackground=COR_CARD)
    style.configure("Treeview.Heading", background=COR_PRIMARIA, foreground="white")
    style.configure("TCombobox", fieldbackground=COR_ENTRY, foreground=COR_TEXT)

    for card in cards:
        card.configure(fg_color=COR_CARD)

    for lbl in card_labels:
        lbl.configure(text_color=COR_TEXT)

    for entry_widget in all_entries:
        entry_widget.configure(fg_color=COR_ENTRY, text_color=COR_TEXT)


# =========================================
# TAB LIVROS - CADASTRO
# =========================================

card_cadastro = ctk.CTkFrame(tab_livros, fg_color=COR_CARD, corner_radius=16, border_width=1, border_color=COR_CARD_LIGHT)
card_cadastro.pack(fill="x", padx=15, pady=(15, 5))
cards.append(card_cadastro)

cadastro_inner = ctk.CTkFrame(card_cadastro, fg_color="transparent")
cadastro_inner.pack(fill="both", expand=True, padx=20, pady=15)

lbl_cadastro = ctk.CTkLabel(
    cadastro_inner, text="Cadastro de Livros", font=("Segoe UI", 16, "bold"), text_color=COR_PRIMARIA
)
lbl_cadastro.pack(anchor="w", pady=(0, 12))
card_labels.append(lbl_cadastro)

campos_frame = ctk.CTkFrame(cadastro_inner, fg_color="transparent")
campos_frame.pack(fill="x")

lbl_titulo = ctk.CTkLabel(campos_frame, text="Título", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_titulo.grid(row=0, column=0, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_titulo)

entry_titulo = ctk.CTkEntry(
    campos_frame, placeholder_text="Digite o título do livro", width=220, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_titulo.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_titulo)

lbl_autor = ctk.CTkLabel(campos_frame, text="Autor", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_autor.grid(row=0, column=1, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_autor)

entry_autor = ctk.CTkEntry(
    campos_frame, placeholder_text="Nome do autor", width=220, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_autor.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_autor)

lbl_categoria = ctk.CTkLabel(campos_frame, text="Categoria", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_categoria.grid(row=0, column=2, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_categoria)

combo_categoria = ctk.CTkComboBox(
    campos_frame,
    values=["Conto", "Poesia", "Ficção Científica", "Filosofia", "Ciências", "Romance", "Tecnologia", "Aventura", "Biografia", "Terror"],
    width=200, height=38, fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT,
    button_color=COR_PRIMARIA, button_hover_color=COR_PRIMARIA_HOVER,
    dropdown_fg_color=COR_CARD, dropdown_hover_color=COR_CARD_LIGHT, dropdown_text_color=COR_TEXT,
    corner_radius=8, font=("Segoe UI", 11),
)
combo_categoria.grid(row=1, column=2, padx=(0, 10), pady=(0, 10))

lbl_qtd = ctk.CTkLabel(campos_frame, text="Quantidade", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_qtd.grid(row=0, column=3, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_qtd)

entry_quantidade = ctk.CTkEntry(
    campos_frame, placeholder_text="0", width=100, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_quantidade.grid(row=1, column=3, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_quantidade)

botoes_frame = ctk.CTkFrame(cadastro_inner, fg_color="transparent")
botoes_frame.pack(fill="x", pady=(5, 0))

btn_cadastrar = ctk.CTkButton(
    botoes_frame, text="✅  Cadastrar", command=lambda: cadastrar_livro(),
    width=150, height=40, font=("Segoe UI", 12, "bold"),
    fg_color=COR_PRIMARIA, hover_color=COR_PRIMARIA_HOVER, corner_radius=10,
)
btn_cadastrar.pack(side="left", padx=(0, 10))

btn_excluir = ctk.CTkButton(
    botoes_frame, text="🗑️  Excluir", command=lambda: excluir_livro(),
    width=150, height=40, font=("Segoe UI", 12, "bold"),
    fg_color=COR_PERIGO, hover_color=COR_PERIGO_HOVER, corner_radius=10,
)
btn_excluir.pack(side="left")

# =========================================
# TAB LIVROS - TABELA
# =========================================

card_tabela = ctk.CTkFrame(tab_livros, fg_color=COR_CARD, corner_radius=16, border_width=1, border_color=COR_CARD_LIGHT)
card_tabela.pack(fill="both", expand=True, padx=15, pady=(10, 15))
cards.append(card_tabela)

tabela_inner = ctk.CTkFrame(card_tabela, fg_color="transparent")
tabela_inner.pack(fill="both", expand=True, padx=20, pady=15)

lbl_tabela = ctk.CTkLabel(
    tabela_inner, text="Livros Cadastrados", font=("Segoe UI", 16, "bold"), text_color=COR_PRIMARIA
)
lbl_tabela.pack(anchor="w", pady=(0, 10))
card_labels.append(lbl_tabela)

tree_container = ctk.CTkFrame(tabela_inner, fg_color=COR_CARD, corner_radius=10)
tree_container.pack(fill="both", expand=True)

colunas = ("ID", "Título", "Autor", "Categoria", "Quantidade")

scroll_livros = ttk.Scrollbar(tree_container, orient="vertical")

tabela_livros = ttk.Treeview(
    tree_container, columns=colunas, show="headings", height=10, yscrollcommand=scroll_livros.set
)
scroll_livros.config(command=tabela_livros.yview)
scroll_livros.pack(side="right", fill="y")
tabela_livros.pack(side="left", fill="both", expand=True)

for col in colunas:
    tabela_livros.heading(col, text=col)
    tabela_livros.column(col, anchor="center", width=200)

# =========================================
# TAB EMPRÉSTIMOS - CADASTRO
# =========================================

card_emp = ctk.CTkFrame(tab_emprestimos, fg_color=COR_CARD, corner_radius=16, border_width=1, border_color=COR_CARD_LIGHT)
card_emp.pack(fill="x", padx=15, pady=(15, 5))
cards.append(card_emp)

emp_inner = ctk.CTkFrame(card_emp, fg_color="transparent")
emp_inner.pack(fill="both", expand=True, padx=20, pady=15)

lbl_emp = ctk.CTkLabel(
    emp_inner, text="Empréstimo de Livros", font=("Segoe UI", 16, "bold"), text_color=COR_PRIMARIA
)
lbl_emp.pack(anchor="w", pady=(0, 12))
card_labels.append(lbl_emp)

campos_emp1 = ctk.CTkFrame(emp_inner, fg_color="transparent")
campos_emp1.pack(fill="x")

lbl_nome = ctk.CTkLabel(campos_emp1, text="Nome", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_nome.grid(row=0, column=0, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_nome)

entry_nome = ctk.CTkEntry(
    campos_emp1, placeholder_text="Nome do aluno", width=180, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_nome.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_nome)

lbl_sobrenome = ctk.CTkLabel(campos_emp1, text="Sobrenome", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_sobrenome.grid(row=0, column=1, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_sobrenome)

entry_sobrenome = ctk.CTkEntry(
    campos_emp1, placeholder_text="Sobrenome", width=180, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_sobrenome.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_sobrenome)

lbl_telefone = ctk.CTkLabel(campos_emp1, text="Telefone", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_telefone.grid(row=0, column=2, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_telefone)

entry_telefone = ctk.CTkEntry(
    campos_emp1, placeholder_text="(00) 00000-0000", width=180, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_telefone.grid(row=1, column=2, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_telefone)

campos_emp2 = ctk.CTkFrame(emp_inner, fg_color="transparent")
campos_emp2.pack(fill="x")

lbl_serie = ctk.CTkLabel(campos_emp2, text="Série", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_serie.grid(row=0, column=0, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_serie)

entry_serie = ctk.CTkEntry(
    campos_emp2, placeholder_text="Ex: 3º Ano A", width=180, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_serie.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_serie)

lbl_livro_id = ctk.CTkLabel(campos_emp2, text="ID Livro", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_livro_id.grid(row=0, column=1, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_livro_id)

entry_livro_id = ctk.CTkEntry(
    campos_emp2, placeholder_text="ID do livro", width=120, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT, corner_radius=8, font=("Segoe UI", 11),
)
entry_livro_id.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
all_entries.append(entry_livro_id)

lbl_venc = ctk.CTkLabel(campos_emp2, text="Vencimento", font=("Segoe UI", 11, "bold"), text_color=COR_TEXT_MUTED)
lbl_venc.grid(row=0, column=2, padx=(0, 5), pady=(0, 2), sticky="w")
card_labels.append(lbl_venc)

venc_frame = ctk.CTkFrame(campos_emp2, fg_color="transparent")
venc_frame.grid(row=1, column=2, padx=(0, 10), pady=(0, 10), sticky="w")

combo_dia = ctk.CTkComboBox(
    venc_frame, values=[f"{i:02d}" for i in range(1, 32)], width=65, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT,
    button_color=COR_PRIMARIA, button_hover_color=COR_PRIMARIA_HOVER,
    dropdown_fg_color=COR_CARD, dropdown_hover_color=COR_CARD_LIGHT, dropdown_text_color=COR_TEXT,
    corner_radius=8, font=("Segoe UI", 11),
)
combo_dia.pack(side="left", padx=(0, 4))

ctk.CTkLabel(venc_frame, text="/", text_color=COR_TEXT, font=("Segoe UI", 14, "bold")).pack(side="left")

combo_mes = ctk.CTkComboBox(
    venc_frame, values=[f"{i:02d}" for i in range(1, 13)], width=65, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT,
    button_color=COR_PRIMARIA, button_hover_color=COR_PRIMARIA_HOVER,
    dropdown_fg_color=COR_CARD, dropdown_hover_color=COR_CARD_LIGHT, dropdown_text_color=COR_TEXT,
    corner_radius=8, font=("Segoe UI", 11),
)
combo_mes.pack(side="left", padx=4)

ctk.CTkLabel(venc_frame, text="/", text_color=COR_TEXT, font=("Segoe UI", 14, "bold")).pack(side="left")

combo_ano = ctk.CTkComboBox(
    venc_frame, values=[str(i) for i in range(date.today().year, date.today().year + 6)], width=80, height=38,
    fg_color=COR_ENTRY, text_color=COR_TEXT, border_color=COR_CARD_LIGHT,
    button_color=COR_PRIMARIA, button_hover_color=COR_PRIMARIA_HOVER,
    dropdown_fg_color=COR_CARD, dropdown_hover_color=COR_CARD_LIGHT, dropdown_text_color=COR_TEXT,
    corner_radius=8, font=("Segoe UI", 11),
)
combo_ano.pack(side="left", padx=(4, 0))

btn_emp = ctk.CTkButton(
    emp_inner, text="📤  Emprestar Livro", command=lambda: emprestar_livro(),
    width=200, height=42, font=("Segoe UI", 12, "bold"),
    fg_color=COR_INFO, hover_color=COR_INFO_HOVER, corner_radius=10,
)
btn_emp.pack(anchor="w", pady=(5, 0))

# =========================================
# TAB EMPRÉSTIMOS - TABELA
# =========================================

card_tabela_emp = ctk.CTkFrame(tab_emprestimos, fg_color=COR_CARD, corner_radius=16, border_width=1, border_color=COR_CARD_LIGHT)
card_tabela_emp.pack(fill="both", expand=True, padx=15, pady=(10, 5))
cards.append(card_tabela_emp)

tabela_emp_inner = ctk.CTkFrame(card_tabela_emp, fg_color="transparent")
tabela_emp_inner.pack(fill="both", expand=True, padx=20, pady=15)

lbl_tabela_emp = ctk.CTkLabel(
    tabela_emp_inner, text="Livros Emprestados", font=("Segoe UI", 16, "bold"), text_color=COR_PRIMARIA
)
lbl_tabela_emp.pack(anchor="w", pady=(0, 10))
card_labels.append(lbl_tabela_emp)

tree_emp_container = ctk.CTkFrame(tabela_emp_inner, fg_color=COR_CARD, corner_radius=10)
tree_emp_container.pack(fill="both", expand=True)

colunas2 = ("ID", "Nome", "Sobrenome", "Telefone", "Livro", "Série", "Data Empréstimo", "Vencimento")

scroll_emp = ttk.Scrollbar(tree_emp_container, orient="vertical")

tabela_emprestimos = ttk.Treeview(
    tree_emp_container, columns=colunas2, show="headings", height=10, yscrollcommand=scroll_emp.set
)
scroll_emp.config(command=tabela_emprestimos.yview)
scroll_emp.pack(side="right", fill="y")
tabela_emprestimos.pack(side="left", fill="both", expand=True)

for col in colunas2:
    tabela_emprestimos.heading(col, text=col)
    tabela_emprestimos.column(col, anchor="center", width=170)

# =========================================
# BOTÃO DEVOLVER
# =========================================

btn_devolver = ctk.CTkButton(
    tab_emprestimos, text="📖  Devolver Livro", command=lambda: devolver_livro(),
    width=220, height=45, font=("Segoe UI", 13, "bold"),
    fg_color=COR_AVISO, hover_color=COR_AVISO_HOVER, corner_radius=10,
)
btn_devolver.pack(pady=(5, 15))

# =========================================
# FUNÇÕES
# =========================================


def atualizar_livros():
    tabela_livros.delete(*tabela_livros.get_children())
    cursor.execute("SELECT * FROM livros")
    for livro in cursor.fetchall():
        tabela_livros.insert("", "end", values=livro)


def atualizar_emprestimos():
    tabela_emprestimos.delete(*tabela_emprestimos.get_children())
    cursor.execute("""
        SELECT e.id, e.nome, e.sobrenome, e.telefone, l.titulo, e.serie, e.data, e.vencimento
        FROM emprestimos e
        INNER JOIN livros l ON l.id = e.livro_id
    """)
    for item in cursor.fetchall():
        tabela_emprestimos.insert("", "end", values=item)


def cadastrar_livro():
    try:
        titulo = sanitizar_texto(entry_titulo.get(), MAX_TITULO)
        autor = sanitizar_texto(entry_autor.get(), MAX_AUTOR)
        categoria = combo_categoria.get().strip()
        quantidade_str = entry_quantidade.get().strip()

        if not titulo or not autor:
            messagebox.showwarning("Aviso", "Preencha título e autor.")
            return

        if not quantidade_str:
            messagebox.showwarning("Aviso", "Informe a quantidade.")
            return

        if not validar_numero_positivo(quantidade_str):
            messagebox.showwarning("Aviso", "Quantidade inválida. Use apenas números inteiros >= 0.")
            return

        quantidade = int(quantidade_str)

        cursor.execute(
            "INSERT INTO livros (titulo, autor, categoria, quantidade) VALUES (?, ?, ?, ?)",
            (titulo, autor, categoria, quantidade),
        )
        conn.commit()
        atualizar_livros()

        entry_titulo.delete(0, "end")
        entry_autor.delete(0, "end")
        entry_quantidade.delete(0, "end")
        combo_categoria.set("")

        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
    except sqlite3.Error:
        conn.rollback()
        messagebox.showerror("Erro", "Não foi possível cadastrar o livro.")


def excluir_livro():
    try:
        selecao = tabela_livros.selection()

        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um livro para excluir.")
            return

        valores = tabela_livros.item(selecao, "values")
        livro_id = valores[0]

        cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE livro_id = ?", (livro_id,))
        emprestimos_ativos = cursor.fetchone()[0]

        if emprestimos_ativos > 0:
            messagebox.showwarning(
                "Aviso",
                f"Não é possível excluir: o livro possui {emprestimos_ativos} empréstimo(s) ativo(s).",
            )
            return

        confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este livro?")
        if not confirmar:
            return

        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()
        atualizar_livros()
        messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
    except sqlite3.Error:
        conn.rollback()
        messagebox.showerror("Erro", "Não foi possível excluir o livro.")


def emprestar_livro():
    try:
        nome = sanitizar_texto(entry_nome.get(), MAX_NOME)
        sobrenome = sanitizar_texto(entry_sobrenome.get(), MAX_NOME)
        telefone = sanitizar_texto(entry_telefone.get(), MAX_TELEFONE)
        serie = sanitizar_texto(entry_serie.get(), MAX_SERIE)
        livro_id_str = entry_livro_id.get().strip()

        dia = combo_dia.get().strip()
        mes = combo_mes.get().strip()
        ano = combo_ano.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do aluno.")
            return

        if not livro_id_str:
            messagebox.showwarning("Aviso", "Informe o ID do livro.")
            return

        try:
            livro_id = int(livro_id_str)
        except ValueError:
            messagebox.showwarning("Aviso", "ID do livro inválido. Use apenas números.")
            return

        data_valida, msg_erro = validar_data_vencimento(dia, mes, ano)
        if not data_valida:
            messagebox.showwarning("Aviso", msg_erro)
            return

        data_vencimento = f"{dia.zfill(2)}/{mes.zfill(2)}/{ano}"

        cursor.execute("SELECT quantidade, titulo FROM livros WHERE id = ?", (livro_id,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("Erro", "Livro não encontrado.")
            return

        quantidade = resultado[0]

        if quantidade <= 0:
            messagebox.showwarning("Aviso", "Livro indisponível no momento.")
            return

        cursor.execute(
            "SELECT COUNT(*) FROM emprestimos WHERE nome = ? AND sobrenome = ? AND livro_id = ?",
            (nome, sobrenome, livro_id),
        )
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Aviso", "Este aluno já possui um empréstimo deste mesmo livro.")
            return

        cursor.execute(
            "SELECT COUNT(*) FROM emprestimos WHERE nome = ? AND sobrenome = ?",
            (nome, sobrenome),
        )
        total_emprestimos = cursor.fetchone()[0]
        if total_emprestimos >= LIMITE_EMPRESTIMOS_POR_USUARIO:
            messagebox.showwarning(
                "Aviso",
                f"Limite de {LIMITE_EMPRESTIMOS_POR_USUARIO} empréstimos por aluno atingido.",
            )
            return

        data_atual = datetime.now().strftime("%d/%m/%Y")

        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(
            """INSERT INTO emprestimos (nome, sobrenome, telefone, serie, livro_id, data, vencimento)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (nome, sobrenome, telefone, serie, livro_id, data_atual, data_vencimento),
        )
        cursor.execute("UPDATE livros SET quantidade = quantidade - 1 WHERE id = ?", (livro_id,))
        conn.commit()

        atualizar_livros()
        atualizar_emprestimos()

        entry_nome.delete(0, "end")
        entry_sobrenome.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_serie.delete(0, "end")
        entry_livro_id.delete(0, "end")
        combo_dia.set("")
        combo_mes.set("")
        combo_ano.set("")

        messagebox.showinfo("Sucesso", "Livro emprestado com sucesso!")
    except sqlite3.Error:
        conn.rollback()
        messagebox.showerror("Erro", "Não foi possível realizar o empréstimo.")


def devolver_livro():
    try:
        selecao = tabela_emprestimos.selection()

        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para devolver.")
            return

        valores = tabela_emprestimos.item(selecao, "values")
        emprestimo_id = int(valores[0])

        cursor.execute("SELECT livro_id FROM emprestimos WHERE id = ?", (emprestimo_id,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("Erro", "Empréstimo não encontrado.")
            return

        livro_id = resultado[0]

        cursor.execute("SELECT COUNT(*) FROM livros WHERE id = ?", (livro_id,))
        if cursor.fetchone()[0] == 0:
            confirmar = messagebox.askyesno(
                "Atenção",
                "O livro deste empréstimo não existe mais.\nDeseja remover o registro de empréstimo mesmo assim?",
            )
            if not confirmar:
                return
            cursor.execute("DELETE FROM emprestimos WHERE id = ?", (emprestimo_id,))
            conn.commit()
            atualizar_emprestimos()
            messagebox.showinfo("Sucesso", "Registro de empréstimo removido.")
            return

        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("DELETE FROM emprestimos WHERE id = ?", (emprestimo_id,))
        cursor.execute("UPDATE livros SET quantidade = quantidade + 1 WHERE id = ?", (livro_id,))
        conn.commit()

        atualizar_livros()
        atualizar_emprestimos()
        messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
    except (ValueError, IndexError):
        messagebox.showerror("Erro", "Empréstimo inválido.")
    except sqlite3.Error:
        conn.rollback()
        messagebox.showerror("Erro", "Não foi possível realizar a devolução.")


# =========================================
# INICIAR
# =========================================

atualizar_livros()
atualizar_emprestimos()

janela.mainloop()
