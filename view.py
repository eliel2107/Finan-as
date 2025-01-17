import sqlite3 as lite
import pandas as pd

# Criando conexão
con = lite.connect("dados.db")

# Criando as tabelas
with con:
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
        adicionado_em DATE,
        valor REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
        retirado_em DATE,
        valor REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )
    """)

# Funções de Inserções -------------------------------------------------
# Inserir categorias
def inserir_categoria(lista_inserir):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query, (lista_inserir[0],))

# Inserir Receitas
def inserir_receitas(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO receitas(categoria, adicionado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Inserir Gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos(categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Funções para deletar -------------------------------------------------
# Deletar receitas
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM receitas WHERE id= ?"
        cur.execute(query, (i,))

# Deletar gastos
def deletar_gastos(valor):
    if isinstance(valor, list):
        for i in valor:
            deletar_gastos(i)
    else:
        with con:
            cur = con.cursor()
            query = "DELETE FROM Gastos WHERE id = ?"
            cur.execute(query, (valor,))

# Funções para ver dados ---------------

# Ver Categorias
def ver_categoria():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens 

# Ver Receitas
def ver_receitas():
    try:
        lista_itens = []
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM receitas")
            linha = cur.fetchall()
            for l in linha:
                lista_itens.append(l)
        return lista_itens
    except lite.OperationalError as e:
        print(f"Erro: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

# Ver Gastos
def ver_gastos():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

# Função para dados da tabela
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista

# Função para dados de gráfico de barras
def bar_valores():
    # Receita Total
    receitas = ver_receitas()
    receitas_lista = [receita[3] for receita in receitas]
    receitas_total = sum(receitas_lista)

    # Despesas Total
    gastos = ver_gastos()
    gastos_lista = [gasto[3] for gasto in gastos]
    gastos_total = sum(gastos_lista)

    # Saldo total
    saldo_total = receitas_total - gastos_total

    return [receitas_total, gastos_total, saldo_total]

# Função gráfico pie
def pie_valores():
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns=['id', 'Categoria', 'Data', 'Valor'])
    dataframe = dataframe.groupby('Categoria')['Valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return [lista_categorias, lista_quantias]

# Função da porcentagem
def porcentagem_valor():
    # Receita Total
    receitas = ver_receitas()
    receitas_lista = [receita[3] for receita in receitas]
    receitas_total = sum(receitas_lista)

    # Despesas Total
    gastos = ver_gastos()
    gastos_lista = [gasto[3] for gasto in gastos]
    gastos_total = sum(gastos_lista)

    # Verificar se receitas_total é zero para evitar divisão por zero
    if receitas_total == 0:
        return 0

    # Porcentagem total
    total = ((receitas_total - gastos_total) / receitas_total) * 100

    return total