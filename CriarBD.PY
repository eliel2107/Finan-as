# Importando SQLite
import sqlite3 as lite

# Criando conexão
con = lite.connect('dados.db')

# Criando tabela de Categorias
with con:
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
        );
    """)

# Criando tabela de Receita
with con:
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            adicionado_em DATE,
            valor DECIMAL
        );
    """)

# Criando tabela de Gastos
with con:
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            retirado_em DATE,
            valor DECIMAL
        );
    """)


