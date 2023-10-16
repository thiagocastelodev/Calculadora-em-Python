# Importando as Bibliotecas
from PIL import     Image  # Usado para abrir a imagem
import customtkinter as ctk  # Usado na criação da interface
from functools import partial  # Usado ao adicionar comados a botões númericos
from tkinter import END, INSERT  # Usados em alguns funções
from operacoes import calcular  # Usado para fazer o calculo da expressão

# Criando a Tela
tela = ctk.CTk()  # Cria a tela principal
tela.title('Calculadora')  # Adiciona um titulo
tela.resizable(False, False)  # Deixa como falso o redimensionamento da tela
tela.iconbitmap('Imagens/Calculadora - ICON.ico')  # Adiciona um icone

# Fontes
fonte = ('Montserrat', 20)  # Cria uma tupla com nome da fonte e tamanho

# Criando Frames
frame1 = ctk.CTkFrame(tela)  # Cria um frame
frame1.pack()

# Criando os fuções de comados


def colocar_texto(texto):
    """
    Função usada para colocar texto dentro da caixa de texto.

    Args:
        texto (str): texto.
    """
    caixa_de_entrada.insert(INSERT, texto)
    if texto == '()':
        caixa_de_entrada.icursor(caixa_de_entrada.index(INSERT)-1)


def apagar_tudo():
    """
    Função que é chamada para limpar a caixa de texto.
    """
    caixa_de_entrada.configure(validate="none")
    caixa_de_entrada.delete(0, END)
    caixa_de_entrada.configure(validate="key", validatecommand=(reg, '%S'))


def apagar_ultimo():
    """
    Função que é chamada para apagar o ultimo caracter da caixa de texto.
    """
    caixa_de_entrada.configure(validate="none")
    caixa_de_entrada.delete(caixa_de_entrada.index(
        INSERT)-1, caixa_de_entrada.index(INSERT))
    caixa_de_entrada.configure(validate="key", validatecommand=(reg, '%S'))


# Lista de caracteres válidos para se digitar na calculadora
validos = ['+', '-', '*', '/', '%', '!', '.', '0',
           '1', '2', '3', '4', '5', '6', '7', '8', '9', '()', '(', ')',
           '√', 'π', '^', 'x']


def valida_entrada(texto):
    """
    Função que válida todo texto digitado na caixa de texto.

    Args:
        texto (str): texto.

    Returns:
        bool: True or False.
    """
    if texto in validos:
        return True
    elif len(texto) > 1 and len(texto) == len([c for c in texto if c in validos]):
        return True
    else:
        return False


def dar_foco():
    """
    Função que é chamada para sempre o foco se manter na caixa de texto.
    """
    caixa_de_entrada.focus_set()


def botao_igual_função():
    """
    Função responsável por chamar outra função que vai fazer o calculo,apagar o texto atual
    e colocar o resultado na caixa de texto.
    """
    if caixa_de_entrada.get() != '':
        try:
            resultado = calcular(caixa_de_entrada.get().strip())
            apagar_tudo()
            caixa_de_entrada.insert(END, resultado)
        except:
            apagar_tudo()
            caixa_de_entrada.configure(validate="none")
            caixa_de_entrada.insert(END, 'Expressão Inválida!')
            caixa_de_entrada.configure(
                validate="key", validatecommand=(reg, '%S'))


def botao_enter(event):
    """
    Função resposável pelo evento do botão enter que chama a funçao do botão igual.
    """
    botao_igual_função()


def backspace(event):
    """
    Função resposável pelo evento do botão backspace que chama a funçao do apagar_ultimo.
    """
    apagar_ultimo()


# Caixa de Entrada
caixa_de_entrada = ctk.CTkEntry(
    frame1, width=390, height=60, font=fonte, takefocus=True)
reg = caixa_de_entrada.register(valida_entrada)
caixa_de_entrada.configure(validate="key", validatecommand=(reg, '%S'))

# Posiciono a caixa de entrada
caixa_de_entrada.grid(column=0, row=0, columnspan=4)

# Botões

# Botão que adiciona o simbolo de raiz
botao_raiz = ctk.CTkButton(frame1, text='√', width=50, fg_color='transparent', text_color='black',
                           font=fonte, hover_color='#F8F8FF',
                           command=partial(colocar_texto, '√'))
# Aqui temos um padrão que vai repetir onde posiciono o botão utilizando grid
botao_raiz.grid(column=0, row=1, padx=5, pady=5)

# Botão que adiciona o simbolo de Pi
botao_pi = ctk.CTkButton(frame1, text='π', width=50, fg_color='transparent',
                         text_color='black', font=fonte, hover_color='#F8F8FF',
                         command=partial(colocar_texto, 'π'))
botao_pi.grid(column=1, row=1, padx=5, pady=5)

# Botão que adiciona o simbolo de potencia
botao_potencia = ctk.CTkButton(frame1, text='^', width=50, fg_color='transparent',
                               text_color='black', font=fonte, hover_color='#F8F8FF',
                               command=partial(colocar_texto, '^'))
botao_potencia.grid(column=2, row=1, padx=5, pady=5)

# Botão que adiciona o simbolo de exclamação
botao_exclamaçao = ctk.CTkButton(frame1, text='!', width=50, fg_color='transparent',
                                 text_color='black', font=fonte, hover_color='#F8F8FF',
                                 command=partial(colocar_texto, '!'))
botao_exclamaçao.grid(column=3, row=1, padx=5, pady=5)

# Botão de limpar toda entrada
botao_limpar = ctk.CTkButton(frame1, text='C', width=70, height=70,
                             font=fonte, text_color='black', fg_color='#CD5C5C', hover_color='#F8F8FF',
                             command=apagar_tudo)
botao_limpar.grid(column=0, row=2, pady=3, padx=5)

# Botão que adiciona o simbolo de parênteses
botao_parenteses = ctk.CTkButton(frame1, text='()', width=70, height=70, font=fonte, text_color='black', hover_color='#F8F8FF',
                                 command=partial(colocar_texto, '()'))
botao_parenteses.grid(column=1, row=2, padx=5)

# Botão que adiciona o simbolo de porcentagem
botao_porcentagem = ctk.CTkButton(frame1, text='%', width=70, height=70, font=fonte, text_color='black', hover_color='#F8F8FF',
                                  command=partial(colocar_texto, '%'))
botao_porcentagem.grid(column=2, row=2, pady=3, padx=5)

# Botão que adiciona o simbolo de divisão ou barra
botao_barra = ctk.CTkButton(frame1, text='/', width=70, height=70, font=fonte, text_color='black', hover_color='#F8F8FF',
                            command=partial(colocar_texto, '/'))
botao_barra.grid(column=3, row=2, pady=3, padx=5)

# Botão que adiciona o simbolo de multiplicação ou x
botao_multiplicaçao = ctk.CTkButton(frame1, text='x', width=70, height=70, font=fonte, text_color='black', hover_color='#F8F8FF',
                                    command=partial(colocar_texto, 'x'))
botao_multiplicaçao.grid(column=3, row=3, padx=5)

# Botão que adiciona o simbolo de subtração ou -
botao_subtraçao = ctk.CTkButton(frame1, text='-', width=70, height=70, font=fonte, text_color='black', hover_color='#F8F8FF',
                                command=partial(colocar_texto, '-'))
botao_subtraçao.grid(column=3, row=4, padx=5)

# Botão que adiciona o simbolo de adição ou +
botao_adiçao = ctk.CTkButton(frame1, text='+', width=70, height=70, font=fonte, text_color='black', hover_color='#F8F8FF',
                             command=partial(colocar_texto, '+'))
botao_adiçao.grid(column=3, row=5, padx=5)

# Botão que adiciona um ponto
botao_ponto = ctk.CTkButton(frame1, text='.', width=70, height=70,
                            font=fonte, text_color='black', fg_color='#B0C4DE', hover_color='#F8F8FF',
                            command=partial(colocar_texto, '.'))
botao_ponto.grid(column=1, row=6, padx=5)

# Abre uma imagem e salvo na variavel imagem_backspace
imagem_backspace = ctk.CTkImage(Image.open(
    'Imagens/Backspace - ICON.webp'), size=(20, 25))

# Botão que apaga ultimo número ou sinal
botao_backspace = ctk.CTkButton(frame1, image=imagem_backspace, text=None, width=70,
                                height=70, fg_color='#B0C4DE', hover_color='#F8F8FF',
                                command=apagar_ultimo)
botao_backspace.grid(column=2, row=6, pady=3, padx=5)

# Botão que adiciona o simbolo de igualdade e faz a expresâo escrita na entrada ser resolvida
botao_igual = ctk.CTkButton(frame1, text='=', width=70, height=70,
                            font=fonte, text_color='black', fg_color='#4169E1', hover_color='#F8F8FF',
                            command=botao_igual_função)
botao_igual.grid(column=3, row=6, padx=5)

# Cria todos os botões númericos e adiciona na possição correta
coluna, linha = 0, 6
for n in range(10):
    botao_numerico = ctk.CTkButton(frame1, text=n, width=70, height=70,
                                   font=fonte, text_color='black', fg_color='#B0C4DE', hover_color='#F8F8FF',
                                   command=partial(colocar_texto, n))
    botao_numerico.grid(column=coluna, row=linha, pady=3)
    if not n % 3 == 0:  # Faz uma verificação se númerico atual definido como n é divisivel por 3
        coluna += 1    # Se divisivel que dizer que posso mudar de linha pois ja terminou os numeros na mesma
    else:              # e volto uma linha para cima, se não divisivel continuo na mesma linha e mudo a coluna
        coluna, linha = 0, linha - 1

# Funcionalidades Extras

# Chama a função responsável pelo foco na caixa de texto
tela.after(10, dar_foco)
# Faz a ligação do botão Enter com função botão_enter
tela.bind('<Return>', botao_enter)
# Faz a ligação do botão backspace com função backspace
tela.bind('<BackSpace>', backspace)


# Faz o programa se inciar
tela.mainloop()
