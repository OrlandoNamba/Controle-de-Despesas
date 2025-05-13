import sqlite3 as lite  # Importando SQLite
import pandas as pd
import os
import sys
import shutil  # Para copiar o banco de dados

""" Projeto: Controle de Despesas Pessoal
    @Autor: Orlando Namba   
           """
# -----------------------------------------------------------------------------

def resource_path(relative_path):
    """Obtenha o caminho absoluto para recursos, funciona para dev e PyInstaller"""
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Define o local persistente para o banco de dados
def get_persistent_db_path():
    """Retorna o caminho persistente para o banco de dados"""
    user_data_dir = os.path.join(os.path.expanduser("~"), "ControleDeDespesas")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)  # Cria o diretório se não existir
    return os.path.join(user_data_dir, "dados.db")

# Caminho para o banco de dados persistente
persistent_db_path = get_persistent_db_path()

# Verifica se o banco de dados já existe no local persistente
if not os.path.exists(persistent_db_path):
    # Copia o banco de dados do diretório temporário para o local persistente
    shutil.copy(resource_path("dados.db"), persistent_db_path)

# Criando Conexão com o banco de dados persistente
con = lite.connect(persistent_db_path)

# -----------------------------------------------------------------------------

# Inserir Categoria
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query, i)

# Funções para Inserir ---------------------------------------------------------
# Inserir Receitas
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionando_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Inserir Gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Funções para Deletar ---------------------------------------------------------
# Deletar Receitas
def deletar_receitas(lista):
    with con:
        cur = con.cursor()
        if not lista:  # Se a lista estiver vazia, exclua todas as receitas
            cur.execute("DELETE FROM Receitas")
        else:
            cur.execute("DELETE FROM Receitas WHERE id = ?", lista)

# Deletar Gastos
def deletar_gastos(lista):
    with con:
        cur = con.cursor()  # Cria o cursor
        if not lista:  # Se a lista estiver vazia, exclua todas as despesas
            cur.execute("DELETE FROM Gastos")
        else:
            cur.execute("DELETE FROM Gastos WHERE id = ?", lista)

# Função para Ver Dados --------------------------------------------------------
# Ver Categorias
def ver_categorias():
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
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")  # Certifique-se de que a ordem das colunas está correta
        return cur.fetchall()

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

# -----------------------------------------------------------------------------
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista


def bar_valores():
    # Receita Total 
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        # Converte o valor para string antes de substituir vírgula por ponto
        receitas_lista.append(float(str(i[3]).replace(',', '.')))

    receita_total = sum(receitas_lista)

    # Despesas Total 
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        # Converte o valor para string antes de substituir vírgula por ponto
        gastos_lista.append(float(str(i[3]).replace(',', '.')))

    gasto_total = sum(gastos_lista)

    # Saldo Total 
    saldo_total = receita_total - gasto_total

    return [receita_total, gasto_total, saldo_total]


def porcentagem_valor():
    # Receita Total
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        # Converte o valor para string antes de substituir vírgula por ponto
        receitas_lista.append(float(str(i[3]).replace(',', '.')))

    receita_total = sum(receitas_lista)

    # Despesas Total
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        # Converte o valor para string antes de substituir vírgula por ponto
        gastos_lista.append(float(str(i[3]).replace(',', '.')))

    gasto_total = sum(gastos_lista)

    # Porcentagem Total
    if receita_total != 0:
        total = 100 - ((receita_total - gasto_total) / receita_total) * 100
    else:
        total = 0

    return [total]


# Cria gráfico de pizza
def pie_valores():
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns=['id', 'categoria', 'data', 'valor'])
    dataframe['valor'] = dataframe['valor'].apply(lambda x: float(str(x).replace(',', '.')))  # Converte os valores para float
    dataframe = dataframe.groupby('categoria')['valor'].sum()  # Obtenha a soma das durações por categoria

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return ([lista_categorias, lista_quantias])


# def resetar_banco_de_dados():
    try:
        # Caminho correto para o banco de dados
        db_path = "dados.db"  # Certifique-se de que este é o banco de dados usado pelo programa

        # Conecta ao banco de dados
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Apaga os dados de todas as tabelas
        cur.execute("DELETE FROM Receitas")
        cur.execute("DELETE FROM Gastos")
        cur.execute("DELETE FROM Categorias")

        # Opcional: Reinicia os IDs das tabelas
        cur.execute("DELETE FROM sqlite_sequence WHERE name='Receitas'")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='Gastos'")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='Categorias'")

        # Confirma as alterações
        con.commit()
        con.close()

        print("Banco de dados resetado com sucesso!")
    except Exception as e:
        print(f"Erro ao resetar o banco de dados: {e}")