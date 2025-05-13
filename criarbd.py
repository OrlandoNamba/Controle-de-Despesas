import sqlite3 as lite  # Importando SQLite

""" Projeto: Controle de Despesas Pessoal
    @Autor: Orlando Namba              """

# Criando conexão
con = lite.connect('dados.db')

# Criando tabela de categoria
with con:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Categoria(id INTEGER PRIMARY KEY, nome TEXT)")

# Criando tabela de receita
with con:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Receitas(id INTEGER PRIMARY KEY, categoria TEXT, adicionando_em DATE, valor DECIMAL)")

# Criando tabela de gasto
with con:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY, categoria TEXT, retirado_em DATE, valor DECIMAL)")