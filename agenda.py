import sys
from datetime import date

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
DESENHAR = 'g'


class Atividade:
    def __init__(self, data, hora, prioridade, descricao, contexto, projeto):
        self.data = data
        self.hora = hora
        self.prioridade = prioridade
        self.descricao = descricao
        self.contexto = contexto
        self.projeto = projeto


def converter(atividade):
    texto = ''
    if atividade.data != '':
        texto += atividade.data + ' '
    if atividade.hora != '':
        texto += atividade.hora + ' '
    if atividade.prioridade != '':
        texto += atividade.prioridade + ' '
    if atividade.descricao != '':
        texto += atividade.descricao
    if atividade.contexto != '':
        texto += ' ' + atividade.contexto
    if atividade.projeto != '':
        texto += ' ' + atividade.projeto
    return texto


# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor):
    print(cor + texto + RESET)


# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z,
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais podem ser implementados como uma tupla, dicionário  ou objeto. A função
# recebe esse item através do parâmetro extras.
#
# extras tem como elementos data, hora, prioridade, contexto, projeto
#
def adicionar(atividade, arquivo):
    if atividade.descricao == '':
        print('A descrição está vazia!')
        return False
    novaAtividade = converter(atividade)
    try:
        arquivoTODO = open(arquivo, 'a')
        arquivoTODO.write(novaAtividade + '\n')
    except IOError as err:
        print('A escrita no arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    return True


# Valida a prioridade.
def prioridadeValida(prioridade):
    if len(prioridade) == 3:
        if prioridade[0] == '(' and prioridade[2] == ')':
            if soLetra(prioridade[1]):
                return True
    return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(hora):
    if len(hora) == 4 or soDigitos(hora):
        horas = int(hora[0:2])
        minutos = int(hora[2:4])
        if horas <= 23 or minutos <= 59:
            return True
    return False


# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto.
def dataValida(data):
    if len(data) == 8 and soDigitos(data):
        dia = int(data[0:2])
        mes = int(data[2:4])
        if 1 <= mes <= 12 and dia >= 1:
            if mes in [1, 3, 5, 7, 8, 10, 12] and dia <= 31:
                return True
            elif mes == 2 and dia <= 29:
                return True
            elif mes in [4, 6, 9, 11] and dia <= 30:
                return True
    return False


# Valida que o string do projeto está no formato correto.
def projetoValido(projeto):
    if len(projeto) >= 2 and projeto[0] == '+':
        return True
    return False


# Valida que o string do contexto está no formato correto.
def contextoValido(contexo):
    if len(contexo) >= 2 and contexo[0] == '@':
        return True
    return False


# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(texto):
    if type(texto) == str:
        for digito in texto:
            if '0' <= digito <= '9':
                return True
    return False


def soLetra(texto):
    if type(texto) == str:
        for letra in texto.upper():
            if 'A' <= letra <= 'Z':
                return True
    return False


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.
def organizar(linhas):
    atividades = []

    for texto in linhas:
        data = ''
        hora = ''
        prioridade = ''
        descricao = ''
        contexto = ''
        projeto = ''

        texto = texto.strip()  # remove espaços em branco e quebras de linha do começo e do fim
        tokens = texto.split()  # quebra o string em palavras

        # Processa os tokens um a um, verificando se são as partes da atividade.
        # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
        # na variável data e posteriormente removido a lista de tokens. Feito isso,
        # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
        # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
        # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
        # corresponde à descrição. É só transformar a lista de tokens em um string e
        # construir a tupla com as informações disponíveis.

        # TRATAR EXCEÇÕES
        if len(tokens) and dataValida(tokens[0]):
            data = tokens.pop(0)
        if len(tokens) and horaValida(tokens[0]):
            hora = tokens.pop(0)
        if len(tokens) and prioridadeValida(tokens[0]):
            prioridade = tokens.pop(0)
        if len(tokens) and projetoValido(tokens[-1]):
            projeto = tokens.pop(-1)
        if len(tokens) and contextoValido(tokens[-1]):
            contexto = tokens.pop(-1)
        if len(tokens) and ' '.join(tokens) != '':
            descricao = ' '.join(tokens)

        # A linha abaixo inclui em itens um objeto contendo as informações relativas aos compromissos
        # nas várias linhas do arquivo.
        # itens.append(...)
        atividades.append(Atividade(data, hora, prioridade, descricao, contexto, projeto))

    return atividades


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados).
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.
def listar(filtro=None):
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        linhas = list(arquivoTODO)
    except IOError as err:
        print('A leitura do arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    atividades = organizar(linhas)
    lista = atividades[:]
    ordenarPorDataHora(lista)
    lista = ordenarPorPrioridade(lista)
    for atividade in lista:
        texto = str(atividades.index(atividade) + 1) + " " + converter(atividade)
        if atividade.prioridade == '(A)':
            printCores(texto, RED + BOLD)
        elif atividade.prioridade == '(B)':
            printCores(texto, YELLOW)
        elif atividade.prioridade == '(C)':
            printCores(texto, CYAN)
        elif atividade.prioridade == '(D)':
            printCores(texto, GREEN)
        else:
            print(texto)
    return True

def compararData(atividade):
    if atividade.data != '':
        dia = int(atividade.data[0:2])
        mes = int(atividade.data[2:4])
        ano = int(atividade.data[4:8])
        return date(ano, mes, dia)
    else:
        return date(9999, 12, 31)
def compararHora(atividade):
    if atividade.hora != '':
        return atividade.hora
    else:
        return "9999"
def ordenarPorDataHora(atividades):
    atividades.sort(key=compararHora)
    atividades.sort(key=compararData)
    return atividades


def ordenarPorPrioridade(atividades):
    lista = []
    for atividade in atividades:
        if atividade.prioridade != '':
            lista.append(atividade)
    lista = sorted(lista, key=lambda atividade:atividade.prioridade)
    for atividade in atividades:
        if atividade.prioridade == '':
            lista.append(atividade)
    atividades = lista
    return atividades


def fazer(indice):
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        linhas = list(arquivoTODO)
    except IOError as err:
        print('A leitura do arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    atividadeFeita = organizar([linhas[indice - 1]])[0]
    if not adicionar(atividadeFeita, ARCHIVE_FILE) or not remover(indice):
        return False
    return True


def remover(indice):
    try:
        arquivoTODO = open(TODO_FILE, "r")
        linhas = list(arquivoTODO)
    except IOError as err:
        print('A leitura do arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    try:
        linhas.pop(indice - 1)
    except IndexError:
        print('A atividade não existe!')
        print('Dica: O indice deve está entre 1 e ' + str((len(linhas))))
        return False
    try:
        arquivoTODO = open(TODO_FILE, 'w')
        for i in range(0, len(linhas)):
            arquivoTODO.write(linhas[i])
    except IOError as err:
        print('A escrita no arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    return True


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'.
def priorizar(indice, prioridade):
    try:
        arquivoTODO = open(TODO_FILE, "r")
        linhas = list(arquivoTODO)
    except IOError as err:
        print('A leitura do arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    try:
        atividade = organizar([linhas[indice - 1]])[0]
        if prioridadeValida('(' + prioridade + ')'):
            atividade.prioridade = '(' + prioridade.upper() + ')'
        else:
            return False
        linhas[indice - 1] = converter(atividade) + '\n'
    except IndexError:
        print('A atividade não existe!')
        print('Dica: O indice deve está entre 1 e ' + str((len(linhas))))
        return False
    try:
        arquivoTODO = open(TODO_FILE, 'w')
        for i in range(0, len(linhas)):
            arquivoTODO.write(linhas[i])
    except IOError as err:
        print('A escrita no arquivo ' + TODO_FILE + ' não foi possivel!')
        print(err)
        return False
    finally:
        arquivoTODO.close()
    return True


def desenhar(dias):
    print('grafico em dias')
    return True


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.
def processarComandos(comandos):
    if comandos[1] == ADICIONAR:
        comandos.pop(0)  # remove 'agenda.py'
        comandos.pop(0)  # remove 'adicionar'
        atividade = organizar([' '.join(comandos)])[0]
        # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
        if adicionar(atividade, TODO_FILE):  # novos itens não têm prioridade
            print('A atividade foi adicionada!')
    elif comandos[1] == LISTAR:
        if len(comandos) == 3:
            listar(comandos[2])
        elif len(comandos) == 2:
            listar()
        else:
            print('O comando é invalido!')
            print('Dica 1: python3 agenda.py l')
            print('Dica 2: python3 agenda.py l A')
    elif comandos[1] == REMOVER:
        if len(comandos) != 3:
            print('O comando é invalido!')
            print('Dica: python3 agenda.py r 1')
        elif not soDigitos(comandos[2]):
            print('O comando é invalido!')
            print('Dica: O numero precisa ser maior que zero')
        elif remover(int(comandos[2])):
            print('A atividade foi removida!')
    elif comandos[1] == FAZER:
        if len(comandos) != 3:
            print('O comando é invalido!')
            print('Dica: python3 agenda.py f 1')
        elif not soDigitos(comandos[2]):
            print('O comando é invalido!')
            print('Dica: O numero precisa ser maior que zero')
        elif fazer(int(comandos[2])):
            print('A atividade foi feita!')
    elif comandos[1] == PRIORIZAR:
        if len(comandos) != 4:
            print('O comando é invalido!')
            print('Dica: python3 agenda.py p 1 A')
        elif not soDigitos(comandos[2]):
            print('O comando é invalido!')
            print('Dica: O numero precisa ser maior que zero')
        elif not soLetra(comandos[3]):
            print('O comando é invalido!')
            print('Dica: A prioridade precisa ser uma letra de A a Z')
        elif priorizar(int(comandos[2]), comandos[3]):
            print('A prioridade foi alterada!')
        elif comandos[1] == DESENHAR:
            if soDigitos(comandos[2]):
                if desenhar(int(comandos[2])):
                    print('O grafico foi desenhado!')
            else:
                print('O comando é invalido!')
                print('Dica: python3 agenda.py g 7')

    else:
        print('O comando é invalido!')


# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
