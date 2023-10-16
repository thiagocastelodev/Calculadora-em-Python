"""
Este módulo contém funções para calcular expressões matemáticas.
Ele suporta operações básicas, parênteses, porcentagens, raiz quadrada,
fatorial e potência.
"""

from math import sqrt


def calcular(expressao):
    """
    Função responsável por retornar o valor após o cálculo da expressão que foi passada.
    Primeiro ela verifica se há ocorrencia de de parenteses se sim chama funçoes responsaveis 
    pelo os mesmo e continua chamando outra função para resolver a expressão e no final retorna 
    o valor da expressão calculado. 

    Args:
        expressão (str): Expressão matemática.

    Returns:
        str: Expressão resolvida.
    """

    expressao = expressao.replace(
        'x', '*').replace('**', '^').replace('π', '3.1415926')

    if '(' in expressao:
        expressao = parenteses_validos(expressao)
        expressao = resolvedor_de_parenteses(expressao)

    expressao = resolver_expressao(separar_expressao(expressao))

    return expressao


def resolver_expressao(expressao):
    """
    Função responsável por resolver uma expressão sem parênteses retorna o valor 
    calculado da expressão.

    Args:
        expressão (list): Expressão matemática.

    Returns:
        str: Expressão calculada.
    """

    if any(verificar_existencia_sinais(expressao)):
        expressao = resolver_sinais_com_prioridade(expressao)

    while len(expressao) > 2:
        valor1, sinal, valor2, *_ = expressao
        expressao.remove(valor1)
        expressao.remove(sinal)
        expressao.remove(valor2)
        resultado = calcular_dois_valores(valor1, sinal, valor2)
        expressao.insert(0, resultado)

    return verificar_se_inteiro(expressao[0])


def verificar_existencia_sinais(expressao):
    """
    Função que faz a verificação da existencia dos seguintes sinais
    %, !, √, ^, '*' e / pois ele tem uma ordem de preferencia acima de
    soma e subtração para serem resolvidos.

    Args:
        expressão (list): Expressão matemática.

    Returns:
        retorna três boleanos.
    """

    fatorial = False
    sinais_tier_1 = False
    sinais_tier_2 = False

    for c in expressao:
        if c == "!":
            fatorial = True
        elif c in ['%', '√', '^']:
            sinais_tier_1 = True
        elif c in ['*', '/']:
            sinais_tier_2 = True

    return fatorial, sinais_tier_1, sinais_tier_2


def parenteses_validos(expressao):
    """
    Função que tem objetivo de verificar se os parênteses abertos dentro da expressão
    se fecham e se necessario faz alguns modificações na expressão recebida para evitar 
    erros na hora de calcular.

    Args:
        expressão (str): Expressão matemática com parênteses.

    Returns:
        str: Expressão modificada.
    """

    if expressao.count('(') != expressao.count(')'):
        raise ValueError('Expressão com Parenteses Invalida')

    nova_expressao = []
    ultimo_c = None
    for i, c in enumerate(expressao):

        if c == '(' and ultimo_c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '%']:
            nova_expressao.append('*')

        if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '√'] and ')' == ultimo_c:
            nova_expressao.append('*')

        ultimo_c = c
        nova_expressao.append(c)

    return ''.join(nova_expressao)


def separador_de_Parenteses(expressao):
    """
    Função que separa os parênteses de uma expressão e retorna uma lista com 
    todos os parênteses separados.

    Args:
        expressão (str): Expressão matemática com parênteses.

    Returns:
        list: Todos os parênteses da expressão.
    """

    parenteses = ''
    parenteses_abertos = 0
    liberado = True
    expressao_separada = []
    expressao_separada_aux = []

    for c in expressao:
        if c in ['(']:
            parenteses += c
            parenteses_abertos += 1
            liberado = False

        elif c in [')']:
            parenteses_abertos -= 1

            if parenteses_abertos != 0:
                parenteses += c
            else:
                parenteses += c
                expressao_separada.append(parenteses)
                expressao_separada_aux.append(parenteses[1:-1])
                parenteses = ''
                liberado = True
        else:
            if liberado:
                pass
            else:
                parenteses += c

    return expressao_separada, expressao_separada_aux


def resolvedor_de_parenteses(expressao):
    """
    Função resposável de resolver todos os parênteses de uma expressão.
    Nessa função é feito toda resolução dos parênteses de uma expressão e 
    retorna a expressão recebida de volta com os parênteses resolvidos.

    Args:
        expressão (str): Expressão matemática com parênteses.

    Returns:
        str: Expressão com todos os parênteses resolvido.
    """

    cont = 1
    while '(' in expressao:

        expressao_separada, expressao_separada_aux = separador_de_Parenteses(
            expressao)
        expressao_aux = ''.join(expressao_separada_aux[0])

        if '(' in expressao_aux:
            while '(' in expressao_aux:
                separada, separada_aux = separador_de_Parenteses(expressao_aux)
                expressao_if = ''.join(separada_aux[0])

                expressao_aux = expressao_if
                if '(' in expressao_if:
                    continue
                else:
                    resultado = resolver_expressao(
                        separar_expressao(expressao_if))

                    expressao = expressao.replace(
                        '('+expressao_if+')', resultado)

                    cont += 1
        else:
            resultado = resolver_expressao(separar_expressao(expressao_aux))

            expressao = expressao.replace('('+expressao_aux+')', resultado)

            cont += 1

    return expressao


def separar_expressao(expressao):
    """
    Função que faz uma separação de sinais e valores da expressão que é uma string
    e retorna a expressão separada em formato de lista, se necessario faz alguns modificações
    na expressão original para evitar erros de cálculo.

    Args:
        expressão (str): Expressão matemática.

    Returns:
        list: Expressão separada por valores e sinais.
    """

    expressao_separado = []
    numero = ''
    ultimo_c = ''

    for i, c in enumerate(expressao):
        if i == 0:
            if c in ['-', '+'] or c.isdigit():
                numero += c
            elif c in ['√']:
                expressao_separado.append(c)
            else:
                raise ValueError
            ultimo_c = c

        elif c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or c in ['.']:
            if ultimo_c == '!':
                expressao_separado.append('*')
            numero += c
            ultimo_c = c

        elif c in ['+', '-', '*', '/', '%', '!', '√', '^']:

            if numero != '':
                expressao_separado.append(numero)
                numero = ''

            if c in ['-'] and ultimo_c in ['/', '*', '^', '√']:
                numero += c

            elif c in ['-'] and ultimo_c in ['+']:
                expressao_separado.pop()
                expressao_separado.append(c)

            elif c in '-' and ultimo_c in ['-']:
                expressao_separado.pop()
                expressao_separado.append('+')

            elif c in ['√'] and ultimo_c == '!':
                expressao_separado.append('*')
                expressao_separado.append(c)

            else:
                expressao_separado.append(c)

        ultimo_c = c

    if numero != '':
        expressao_separado.append(numero)

    return expressao_separado


def resolver_sinais_com_prioridade(expressao):
    """
    Função que resolve na ordem de prioridade os sinais de uma expressão.
    Retorna a mesma expressão com com todos os sinais que tem prioridade da 
    subtração e adição respondidos.

    Args:
        expressão (list): Expressão matemática.

    Returns:
        list: Expressão com os sinais de prioridade resolvidos.
    """

    fatorial_sinal, tier1, tier2 = verificar_existencia_sinais(expressao)

    if fatorial_sinal:
        while '!' in expressao:
            onde = expressao.index('!')
            valor, sinal = expressao[onde-1], expressao[onde]
            expressao.pop(onde-1)
            expressao.pop(onde-1)
            resultado = fatorial(valor)
            expressao.insert(onde-1, resultado)

    if tier1:
        cont = 0
        while '√' in expressao or '%' in expressao or '^' in expressao:
            c = expressao[cont]

            if c == '√':
                onde = expressao.index('√')
                valor, sinal = expressao[onde+1], expressao[onde]
                expressao.pop(onde+1)
                expressao.pop(onde)
                resultado = raiz_quadrada(valor)
                expressao.insert(onde, resultado)
                cont = 0

            elif c == '%':
                onde = expressao.index('%')
                valor1, sinal = expressao[onde-1], expressao[onde]
                try:
                    valor2 = float(expressao[onde+1])
                    expressao.pop(onde-1)
                    expressao.pop(onde-1)
                    expressao.pop(onde-1)
                    resultado = porcentagem(valor1, valor2)
                    expressao.insert(onde-1, resultado)
                except:
                    expressao.pop(onde-1)
                    expressao.pop(onde-1)
                    resultado = str(float(valor1)/100)
                    expressao.insert(onde-1, resultado)
                cont = 0

            elif c == '^':
                onde = expressao.index('^')
                valor1, sinal, valor2 = expressao[onde -
                                                  1], expressao[onde], expressao[onde + 1]
                expressao.pop(onde - 1)
                expressao.pop(onde)
                expressao.pop(onde - 1)
                resultado = potencia(valor1, valor2)
                expressao.insert(onde - 1, resultado)
                cont = 0

            cont += 1

    if tier2:
        cont = 0
        while '*' in expressao or '/' in expressao:
            c = expressao[cont]

            if c == '*':
                onde = expressao.index('*')
                valor1, sinal, valor2 = expressao[onde -
                                                  1], expressao[onde], expressao[onde+1]
                expressao.pop(onde-1)
                expressao.pop(onde)
                expressao.pop(onde-1)
                resultado = calcular_dois_valores(valor1, sinal, valor2)
                expressao.insert(onde-1, resultado)
                cont = 0

            elif c == '/':
                onde = expressao.index('/')
                valor1, sinal, valor2 = expressao[onde -
                                                  1], expressao[onde], expressao[onde+1]
                expressao.pop(onde-1)
                expressao.pop(onde)
                expressao.pop(onde-1)
                resultado = calcular_dois_valores(valor1, sinal, valor2)
                expressao.insert(onde-1, resultado)
                cont = 0

            cont += 1

    return expressao


def calcular_dois_valores(valor1, sinal, valor2):
    """
    Função que faz o cálculo de operações basicas de dois valores, recebe um valor,
    um sinal e um segundo valor e retorna o resultado.

    Args:
        valor1 (str): número.
        sinal (str): sinal mátematico basico
        valor2 (str): número.

    Returns:
        str: Resultado do calculo matématico.
    """

    if sinal == '+':
        return str(float(valor1) + float(valor2))
    if sinal == '-':
        return str(float(valor1) - float(valor2))
    if sinal == '*':
        return str(float(valor1) * float(valor2))
    if sinal == '/':
        return str(float(valor1) / float(valor2))


def potencia(valor1, valor2):
    """
    Função responsável por fazer o cálculo de potência, recebe dois valores e
    retorna o resultado.

    Args:
        valor1 (str): número.
        valor2 (str): número.

    Returns:
        str: Resultado da potencia entre o valor1 e valor2.
    """

    return str(eval(f'{valor1}**{valor2}'))


def raiz_quadrada(valor):
    """
    Função responsável por fazer o cálculo de raiz quadrada,recebe um valor e 
    retorna a raiz quadrada do mesmo.

    Args:
        valor (str): número.

    Returns:
        str: Resultado da raiz quadrada do valor.
    """

    return str(sqrt(float(valor)))


def fatorial(valor):
    """
    Função responsável por fazer o cálculo de fatorial de um número
    faz a verificação se o número recebido é negativo para manter o sinal
    e retorna o fatorial do número com sinal negativo se necessario.

    Args:
        valor (str): número.

    Returns:
        str: Resultado do fatorial de valor.
    """

    valor = int(valor)

    negativo = False
    if valor < 0:
        valor *= -1
        negativo = True

    for i in range(valor-1, 0, -1):
        valor *= i

    if negativo:
        valor *= -1

    return str(valor)


def porcentagem(porcentagem, valor):
    """
    Função que recebe dois valores o primeiro sendo a porcentagem e outro um número
    que vai ser feito o calculo da porcentagem dele, retorna o valor dessa porcentagem.

    Args:
        porcentagem (str): número
        valor (str): número.

    Returns:
        str: Resultado da porcentagem do número.
    """

    return str((float(porcentagem) * float(valor)) / 100)


def verificar_se_inteiro(numero):
    """
    Função resposável por fazer uma verificação se o número sem a virgula
    possa ser representado sem ela sem alterar seu valor ele retorna o mesmo sem a virgula
    caso não retorna o número sem modificar nada.

    Args:
        valor (str): número.

    Returns:
        str: número sem os valores após a virgula ou número sem modificação
    """
    
    if '.' in numero:
        parte_decimal = numero.split('.')[1]
        if float(parte_decimal) != 0:
            return numero
        else:
            return str(int(float(numero)))
    else:
        return numero
