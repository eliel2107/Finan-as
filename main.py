from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

# importando Pillow
import sys
import os
from PIL import Image, ImageTk

# Importando Barra de Progresso do tkinter
from tkinter.ttk import Progressbar

#Importando matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Calendario
from tkcalendar import Calendar, DateEntry
from datetime import date


#importando funções da view
from view import bar_valores, inserir_categoria, ver_categoria, inserir_receitas, inserir_gastos, tabela, deletar_gastos, deletar_receitas, pie_valores, porcentagem_valor


# Cores

co0 = "#2e2d2b" # Preta
co1 = "#feffff" #branca
co2 = "#4fa882" # Verde
co3 = "#38576b" # Valor
co4 = "#403d3d" # Letra
co5 = "#e06636" 
co6 = "#038cfc" 
co7 = "#3fbfb9" 
co8 = "#263238" 
co9 = "#e9edf5" 

colors = ["#5588bb", "#66bbbb", "#99bb55", "#ee9944", "#444466", "#bb5555"]

# criando janela vazia
janela = Tk()
janela.title()
janela.geometry("900x650")
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style= ttk.Style(janela)
style.theme_use('clam')

# criando frames para divisão da tela
frameCima = Frame(janela, width=1040, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1040, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela, width=1040, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_pie = Frame(frameMeio, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)


# trabalhando no frame Cima
def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Use get_resource_path para obter o caminho do logo.jpg
logo_path = get_resource_path("logo.jpg")
# Acessando a imagem
app_img = Image.open(logo_path)
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" Orçamento Pessoal", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=("verdana 20 bold"), bg=co1, fg=co4)
app_logo.place(x=0, y=0)



# definindo Tree como global
global tree

#função inserir
def inserir_categoria_b():
    nome = e_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
         if i=='':
              messagebox.showerror("Erro", "Preencha todos os campos")
              return
    # passando para a função inserir gastos presentes na view     
    inserir_categoria(lista_inserir)

    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_categoria.delete(0,'end')

    # pegando os valores da categoria
    categoria_funcao = ver_categoria()
    categoria = []

    for i in categoria_funcao:
         categoria.append(i[1])
    
    #atualizando a lista de categorias
    combo_categoria_despesas['values'] = (categoria)


#inserir novas receitas
def inserir_receita_b():
    nome = 'Receita'
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
    
    # chamando a função receitas presente na view
    inserir_receitas(lista_inserir)

    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    #atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

#inserir novas despesas
def inserir_gastos_b():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
    
    # chamando a função despesas presente na view
    inserir_gastos(lista_inserir)

    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    combo_categoria_despesas.delete(0,'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    #atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


#função deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

            # Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()
        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

            # Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()
    except IndexError:
        messagebox.showerror('Erro', 'Selecione um dos dados na tabela')

          


# Porcentagem

def porcentagem():
    l_name = Label(frameMeio, text="Porcentagem da Receita Gasta", height=1, anchor=NW, font=("Verdana"), bg=co1, fg=co4)
    l_name.place(x=7, y=5)

    # Estilo das barras
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Horizontal.TProgressbar", background="#daed6b")
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(frameMeio, length=180, style="black.Horizontal.TProgressbar")
    bar.place(x=10, y=35)
    bar["value"] = porcentagem_valor()  # Atribua diretamente o valor inteiro

    valor = porcentagem_valor()  # Atribua diretamente o valor inteiro

    l_porcentagem = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=("Verdana"), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)

# função para gráfico Bar

def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    # Faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    # ax.autoscale(enable=true, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)
    # create a list collect the plt.patches data

    c = 0
    # set individual bar labels using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
                ax.text(i.get_x()-.001, i.get_height()+.5,
                            str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
                c += 1

    ax.set_xticklabels(lista_categorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)



# Função de resumo total
def resumo():
    valor = bar_valores()

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMeio, text="Total Renda Mensal      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMeio, text="R$  {:,.2F}".format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=70)


    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensal   ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=115)
    l_sumario = Label(frameMeio, text="R$  {:,.2F}".format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=150)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=207)
    l_sumario = Label(frameMeio, text="Total de Saldo              ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=190)
    l_sumario = Label(frameMeio, text="R$  {:,.2F}".format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=220)



    

# Função Grafico pie
def grafico_pie():
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    #only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)



porcentagem()
grafico_bar()
resumo()
grafico_pie()



#Criando  frames dentro do frameBaixo
frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0, column=2)


# Tabela Renda Mensal
app_tabela = Label(frameMeio, text=" Tabela Receitas e Despesas", anchor=NW, font=("verdana 12"), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)


#Função mostrar renda
def mostrar_renda():
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")

    #Vertical Scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)

    #horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        #adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

mostrar_renda()

# Configuração despesas
l_info = Label(frame_operacoes, text='Insira novas despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

#Categoria
l_categoria = Label(frame_operacoes, text='Selecionar categoria', height=1, anchor=NW, font=('Inv 10'), bg=co1, fg=co4)
l_categoria.place(x=2, y=40)


#Pegando categorias Comboboxes
categoria_funcao = ver_categoria()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=('Inv 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=130, y=40)

#Despesas
l_cal_despesas = Label(frame_operacoes, text='Data', height=1, anchor=NW, font=('Inv 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=60, y=70)
e_cal_despesas =DateEntry(frame_operacoes, Width=12, background='darkblue', foreground='white', borderwidth=2, year=2025)
e_cal_despesas.place(x=110, y=71)

# Valor
l_valor_despesas = Label(frame_operacoes, text='Valor gasto', height=1, anchor=NW, font=('Inv 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=35, y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify="left", relief='solid')
e_valor_despesas.place(x=110, y=101)


# botão inserir
img_add_despesas = Image.open("add.png")
img_add_despesas = img_add_despesas.resize((25,25))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes,command=inserir_gastos_b, image=img_add_despesas, text="Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=("Inv 7 bold"), bg=co1, fg=co0, relief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)

# botão deletar
l_excluir = Label(frame_operacoes, text='Deletar ação', height=1, anchor=NW, font=('Inv 10 bold'), bg=co1, fg=co4)
l_excluir.place(x=10, y=190)

img_delete = Image.open("delete.jpg")
img_delete = img_delete.resize((25,25))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes, command=deletar_dados, image=img_delete, text="Deletar".upper(), width=80, compound=LEFT, anchor=NW, font=("Inv 7 bold"), bg=co1, fg=co0, relief=RIDGE)
botao_deletar.place(x=110, y=190)

#Configurando receitas ----------

l_info = Label(frame_configuracao, text='Insira novas Receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=60, y=10)

#calendario Receitas-----------------------------

l_cal_receitas = Label(frame_configuracao, text='Data', height=1, anchor=NW, font=('Inv 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=60, y=40)
e_cal_receitas =DateEntry(frame_configuracao, Width=12, background='darkblue', foreground='white', borderwidth=2, year=2025)
e_cal_receitas.place(x=110, y=41)

# Valor
l_valor_receitas = Label(frame_configuracao, text='Valor', height=1, anchor=NW, font=('Inv 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=60, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify="left", relief='solid')
e_valor_receitas.place(x=110, y=71)

# botão inserir
img_add_receitas = Image.open("add.png")
img_add_receitas = img_add_receitas.resize((25,25))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao, command=inserir_receita_b, image=img_add_despesas, text="Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=("Inv 7 bold"), bg=co1, fg=co0, relief=RIDGE)
botao_inserir_receitas.place(x=110, y=95)


#Operações de novas categorias ----------

l_info = Label(frame_configuracao, text='Inserir nova Categoria', height=1, anchor=NW, font=('Inv 8 bold'), bg=co1, fg=co4)
l_info.place(x=95, y=140)

e_categoria = Entry(frame_configuracao, width=14, justify="left", relief='solid')
e_categoria.place(x=110, y=160)


# botão inserir
img_add_categorias = Image.open("add.png")
img_add_categorias = img_add_categorias.resize((25,25))
img_add_categorias = ImageTk.PhotoImage(img_add_categorias)
botao_inserir_categorias = Button(frame_configuracao, command=inserir_categoria_b, image=img_add_despesas, text="Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=("Inv 7 bold"), bg=co1, fg=co0, relief=RIDGE)
botao_inserir_categorias.place(x=110, y=190)




janela.mainloop()