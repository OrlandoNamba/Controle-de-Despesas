from tkinter import *
import tkinter as tk
from tkinter import Tk, StringVar, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date
from view import bar_valores, pie_valores, porcentagem_valor, inserir_categoria, ver_categorias, inserir_receita, inserir_gastos, tabela, deletar_gastos, deletar_receitas
import locale
import os
import sys

""" Projeto: Controle de Despesas Pessoal
    @Autor: Orlando Namba                                    """

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')      # Definindo o locale para o Brasil

# ================= cores =====================================================
co0 = "#2e2d2b"   # Preta
co1 = "#ffffff"   # branca
co2 = "#4fa882"   # verde
co3 = "#38576b"   # azul - valor
co4 = "#403d3d"   # cinza escuro - letra
co5 = "#e06636"   # laranja - profit
co6 = "#038cfc"   # azul
co7 = "#3fbfb9"   # verde agua
co8 = "#263238"   # cinza escuro azulado
co9 = "#e9edf5"   # branco azulado
# =============================================================================
co10 = "#68c985"  # verde
co11 = "#ffdad6"  # rosa claro
co12 = "#cbecd5"  # verde claro
co13 = "#ff5747"  # vermelho

#           azul     vermelho     verde     laranja   cinza azul  vermelho claro
colors = ['#4583de', '#ff5747', '#68c985', '#ee9944', '#444466', '#bb5555']

# ================= criando janela ============================================

def resource_path(relative_path):
    """Pega o caminho absoluto do recurso, compatível com PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Quando empacotado
    except Exception:
        base_path = os.path.abspath(".")  # Durante o desenvolvimento
    return os.path.join(base_path, relative_path)

janela = Tk()
icone_path = resource_path('img/icone.ico')
janela.iconbitmap(icone_path)

janela.title("Minhas Finanças | Sinfy")
janela.geometry('870x680')
janela.configure(background=co1)


# Bloqueia o redimensionamento da janela
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
# Tema
style.theme_use("default") 
# Define a fonte das celulas da tabela
style.configure("Treeview", highlightthickness=0, bd=0, font=('Geometria', 13))


# ================= Frames Cima =================
frameCima = Frame(janela, width=1043, height=50, bg=co1,  relief="flat",)
frameCima.grid(row=0, column=0)

# ================= Frames Meio =================
frameMeio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# ================= Frames Baixo ================
frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

# ================= Frames Grafico ================
frame_gra_2 = Frame(frameMeio, width=580, height=250, bg=co1)
frame_gra_2.place(x=415, y=5)


# Configurando a logo do aplicativo
logo_path = resource_path('img/logo.png')
app_img = Image.open(logo_path)
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" Minhas Finanças", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Geometria 16 bold'), bg=co1, fg=co4)
app_logo.place(x=0, y=0)


# Variavel Global
global tree

def resource_path(relative_path):
    """Pega o caminho absoluto do recurso, compatível com PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Quando empacotado
    except Exception:
        base_path = os.path.abspath(".")  # Durante o desenvolvimento
    return os.path.join(base_path, relative_path)


# Funcao inserir Categoria
def inserir_categoria_b():
    nome = e_categoria.get()
    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Passando funcao inserir gastos presente na view
    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso', 'Categoria inserido com sucesso!')
    e_categoria.delete(0, 'end')

    # Pegando os valores da categoria
    categorias_funcao = ver_categorias()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

    # Atualizando lista de categoria
    combo_categoria_despesas['values'] = categoria


# Funcao inserir Receita

def inserir_receitas_b():
    nome = 'Receita'
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Chamando funcao inserir Receita presente na view
    inserir_receita(lista_inserir)
    messagebox.showinfo('Sucesso', 'Receita inserido com sucesso!')

    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


# Funcao inserir Despesa
def inserir_despesas_b():
    nome = combo_categoria_despesas.get()
    data = e_cal_despeas.get()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Chamando funcao inserir Despesas presente na view
    inserir_gastos(lista_inserir)
    messagebox.showinfo('Sucesso', 'Despesa inserida com sucesso!')

    combo_categoria_despesas.delete(0, 'end')
    e_cal_despeas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


# Funcao deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Excluido com sucesso!')

            # Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Excluido com sucesso!')

            # Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:
        messagebox.showerror('Erro', 'Selecione um dos dados na tabela')


# funcao para abrir imagem
def ver_imagem():
    global l_imagem, imagem, imagem_string

    treev_dados = tree.focus()
    treev_dicionario = tree.item(treev_dados)
    treev_lista = treev_dicionario['values']
    valor = [int(treev_lista[0])]

    iten = ver_iten(valor)

    imagem = iten[0][8]

    # Abrindo imagem
    imagem = Image.open(imagem)
    imagem = imagem.resize((170, 170))
    imagem = ImageTk.PhotoImage(imagem)

    l_imagem = Label(frameMeio, image=imagem, bg=co1, fg=co4)
    l_imagem.place(x=700, y=10)


# Porcentagem 
def porcentagem():
    l_nome = Label(frameMeio, text="Total de Gastos", height=1, anchor=NW, font=('Geometria 14 bold'), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')

    valor = porcentagem_valor()[0]

    # Condição para alterar cor da barra de progresso entre vermelho e verde
    if valor > 50:
        style.configure("black.Horizontal.TProgressbar", background=co13)
    else:
        style.configure("black.Horizontal.TProgressbar", background=co10)

    style.configure("TProgressbar", thickness=20)

    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = porcentagem_valor()[0]

    l_porcentagem = Label(frameMeio, text=f'{valor:.2f} %', height=1, anchor=NW, font=('Geometria 12 '), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)


# Funcao para grafico bar

def grafico_bar():
    # Limpa o gráfico antigo
    for widget in frameMeio.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    # Cria o novo gráfico
    lista_categorias = ['Renda', 'Gastos', 'Saldo']
    lista_valores = bar_valores()

    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    ax.bar(lista_categorias, lista_valores, color=['#4fa882', '#e06636', '#038cfc'], width=0.9)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)


# Funcao de resumo total
def resumo():
    valor = bar_valores()

    # Linha de separação
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Geometria 1 '), bg='#545454',)
    l_linha.place(x=309, y=54)  # Traço em baixo do texto Salário

    # Renda
    l_sumario = Label(frameMeio, text="Renda                                          ".upper(), height=1, anchor=NW, font=('Geometria 12 bold'), bg=co1, fg='#4583de')
    l_sumario.place(x=306, y=35)

    l_sumario = Label(frameMeio, text=locale.format_string('R$ %.2f', valor[0], grouping=True), height=1, anchor=NW, font=('Geometria 15 bold'), bg=co1, fg='#545454')
    l_sumario.place(x=306, y=70)

    # Linha de separação
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Geometria 1 '), bg='#545454',)
    l_linha.place(x=309, y=134)  # Traço em baixo do texto Despesas

    # Gastos
    l_sumario = Label(frameMeio, text="Gastos                                         ".upper(), height=1, anchor=NW, font=('Geometria 12 bold'), bg=co1, fg=co13)
    l_sumario.place(x=306, y=115)

    l_sumario = Label(frameMeio, text=locale.format_string('R$ %.2f', valor[1], grouping=True), height=1, anchor=NW, font=('Geometria 15 bold'), bg=co1, fg='#545454')
    l_sumario.place(x=306, y=150)

    # Linha de separação
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Geometria 1 '), bg='#545454',)
    l_linha.place(x=309, y=209)  # Traço em baixo do texto Saldo

    # Saldo
    l_sumario = Label(frameMeio, text="Saldo                                          ".upper(), height=1, anchor=NW, font=('Geometria 12 bold'), bg=co1, fg='#68c985')
    l_sumario.place(x=306, y=190)

    l_sumario = Label(frameMeio, text=locale.format_string('R$ %.2f', valor[2], grouping=True), height=1, anchor=NW, font=('Geometria 15 bold'), bg=co1, fg='#545454')
    l_sumario.place(x=306, y=220)


# Funcao grafico pie
def grafico_pie():
    global frame_gra_2

    # Verifica se o frame_gra_2 existe, caso contrário recria
    if not frame_gra_2.winfo_exists():
        frame_gra_2 = Frame(frameMeio, width=580, height=250, bg=co1)
        frame_gra_2.place(x=415, y=5)

    # Faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    cores_personalizadas = ['#dbdb2e', '#84948f', '#d90b9e', '#ee9944', '#664444', '#77427d', '#1ABC9C', '#BDC3C7']
    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=cores_personalizadas, shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_2)
    canva_categoria.get_tk_widget().grid(row=0, column=0)


frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co11)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co12)
frame_configuracao.grid(row=0, column=2, padx=5)


# Tabela Renda mensal
app_tabela = Label(frameMeio, text="Tabela Renda e Gastos", height=1, anchor=NW, font=('Geometria 14 bold'), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)


# funcao para mostrar_renda
def mostrar_renda():
    # criando uma visualização em árvore com barras de rolagem duplas
    tabela_head = ['Cod', 'Categoria', 'Data', 'Valor']

    lista_itens = tabela()

    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended", columns=tabela_head, show="headings")

    # vertical scrollbar
    vsb = ttk.Scrollbar()

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd = ["center", "center", "center", "center"]
    h = [45, 130, 130, 80]
    n = 0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)

        # Ajusta a largura da coluna para a string do cabeçalho
        tree.column(col, width=h[n], anchor=hd[n])

        n += 1

    for item in lista_itens:
        tree.insert('', 'end', values=item)


# Configuracoes Despesas
l_info = Label(frame_operacoes, text="Novas Despesas", height=1, anchor=NW, relief="flat", font=('Geometria 10 bold'), bg=co11, fg=co4)
l_info.place(x=10, y=10)


# Categoria
l_categoria = Label(frame_operacoes, text="Categoria", height=1, anchor=NW, relief="flat", font=('Geometria 10'), bg=co11, fg=co4)
l_categoria.place(x=10, y=40)


# Pegando os categorias
categorias_funcao = ver_categorias()
categorias = []

for i in categorias_funcao:
    categorias.append(i[1])

combo_categoria_despesas = ttk.Combobox(
    frame_operacoes, width=10, font=('Geometria 10'))

combo_categoria_despesas['values'] = (categorias)
combo_categoria_despesas.place(x=110, y=41)


# Despesas
l_cal_despeas = Label(frame_operacoes, text="Data", height=1, anchor=NW, font=('Geometria 10 '), bg=co11, fg=co4)
l_cal_despeas.place(x=10, y=70)
e_cal_despeas = DateEntry(frame_operacoes, width=10, background='darkblue', foreground='white', borderwidth=2, year=2025, date_pattern='dd/mm/yyyy')
e_cal_despeas.place(x=110, y=71)


# Valor
l_valor_despesas = Label(frame_operacoes, text="Valor Total", height=1, anchor=NW, font=('Geometria 10 '), bg=co11, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operacoes, width=11, justify='left', relief="solid")
e_valor_despesas.place(x=110, y=101)


# Botão Inserir Despesas
add_icon_path = resource_path("img/add.png")
add_icon = Image.open(add_icon_path)
add_icon = add_icon.resize((20, 20))
add_icon = ImageTk.PhotoImage(add_icon)
botao_inserir_despesas = Button(frame_operacoes, command=inserir_despesas_b, image=add_icon, compound=LEFT, anchor=CENTER, text="", width=22, height=22, overrelief=RIDGE, bg=co1, fg=co0)
botao_inserir_despesas.place(x=110, y=131)


# Operacao Excluir 
l_excluir = Label(frame_operacoes, text="Excluir Ação", height=1, anchor=NW, font=('Geometria 10 bold'), bg=co11, fg=co4)
l_excluir.place(x=10, y=190)


# Botão Excluir
delete_icon_path = resource_path("img/delete.png")
delete_icon = Image.open(delete_icon_path)
delete_icon = delete_icon.resize((20, 20))
delete_icon = ImageTk.PhotoImage(delete_icon)
botao_deletar = Button(frame_operacoes, command=deletar_dados, image=delete_icon, compound=LEFT, anchor=CENTER, text="", width=22, height=22, overrelief=RIDGE, bg=co1, fg=co0)
botao_deletar.place(x=110, y=190)

# Funcao resetar dados com confirmação
def resetar_dados():
    try:
        # Exibe uma janela de confirmação
        confirmar = messagebox.askyesno("Confirmação", "Todos os dados serão apagados, exceto as categorias. Deseja continuar?")
        if not confirmar:
            return  # Se o usuário clicar em "Não", interrompe a função

        # Exclui todas as receitas e despesas
        deletar_receitas([])  # Passa uma lista vazia para deletar todas as receitas
        deletar_gastos([])    # Passa uma lista vazia para deletar todas as despesas

        # Limpa a tabela de dados
        for item in tree.get_children():
            tree.delete(item)

        # Limpa os widgets gráficos antigos
        for widget in frameMeio.winfo_children():
            try:
                widget.destroy()
            except Exception:
                pass  # Ignora erros ao destruir widgets

        # Recria o texto "Tabela Renda e Gastos"
        app_tabela = Label(frameMeio, text="Tabela Renda e Gastos", height=1, anchor=NW, font=('Geometria 14 bold'), bg=co1, fg=co4)
        app_tabela.place(x=5, y=309)

        # Recria o botão "Resetar"
        botao_resetar = Button(frameMeio, command=resetar_dados, text="Resetar".upper(), width=10, overrelief=RIDGE, font=('Geometria 10 bold'), bg='#ff5747', fg=co0)
        botao_resetar.place(x=250, y=308)

        # Recria os widgets antes de atualizar a interface
        mostrar_renda()
        porcentagem()
        grafico_bar()
        resumo()
        grafico_pie()

        messagebox.showinfo('Sucesso', 'Todos os dados foram resetados com sucesso!')
    except Exception:
        pass  # Ignora qualquer erro que ocorra durante o reset


# Botão Resetar 
botao_resetar = Button(frameMeio, command=resetar_dados, text="Resetar".upper(), width=10, overrelief=RIDGE,  font=('Geometria 10 bold'), bg='#ff5747', fg=co0)
botao_resetar.place(x=250, y=308)


# Configuracoes Receitas 
l_info = Label(frame_configuracao, text="Novas Receitas", height=1, anchor=NW, relief="flat", font=('Geometria 10 bold'), bg=co12, fg=co4)
l_info.place(x=10, y=10)


# Calendario
l_cal_receitas = Label(frame_configuracao, text="Data", height=1, anchor=NW, font=('Geometria 10 '), bg=co12, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=10, background='darkblue', foreground='white', borderwidth=2, year=2025, date_pattern='dd/mm/yyyy')
e_cal_receitas.place(x=110, y=41)


# Valor 
l_valor_receitas = Label(frame_configuracao, text="Valor Total", height=1, anchor=NW, font=('Geometria 10 '), bg=co12, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=11, justify='left', relief="solid")
e_valor_receitas.place(x=110, y=71)


# Botão Inserir Receitas
add_receitas_icon_path = resource_path("img/add.png")
add_receitas_icon = Image.open(add_receitas_icon_path)
add_receitas_icon = add_receitas_icon.resize((20, 20))  
add_receitas_icon = ImageTk.PhotoImage(add_receitas_icon)
botao_inserir_receitas = Button(frame_configuracao, command=inserir_receitas_b, image=add_receitas_icon, compound=LEFT, anchor=CENTER, text="", width=22, height=22, overrelief=RIDGE, bg=co1, fg=co0)
botao_inserir_receitas.place(x=110, y=111)


# Operacao Nova Categoria 
l_info = Label(frame_configuracao, text="Categoria", height=1, anchor=NW, font=('Geometria 10 bold'), bg=co12, fg=co4)
l_info.place(x=10, y=160)
e_categoria = Entry(frame_configuracao, width=11, justify='left', relief="solid")
e_categoria.place(x=110, y=160)


# Botão Inserir Categoria
add_categoria_icon_path = resource_path("img/add.png")
add_categoria_icon = Image.open(add_categoria_icon_path)
add_categoria_icon = add_categoria_icon.resize((20, 20))
add_categoria_icon = ImageTk.PhotoImage(add_categoria_icon)
botao_inserir_categoria = Button(frame_configuracao, command=inserir_categoria_b, image=add_categoria_icon, compound=LEFT, anchor=CENTER, text="", width=22, height=22, overrelief=RIDGE, bg=co1, fg=co0)
botao_inserir_categoria.place(x=110, y=190)

# Camando funçoes
porcentagem()
grafico_bar()
resumo()
grafico_pie()
mostrar_renda()
janela.mainloop()