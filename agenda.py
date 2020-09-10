import sys

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


class Compromisso:
    def __init__(self, descricao, prioridade, data,hora, contexto, projeto):
        self.descricao = descricao
        self.prioridade = prioridade
        self.data = data
        self.hora = hora
        self.contexto = contexto
        self.projeto = projeto
        return


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
def adicionar(compromissos):
    for i in range(len(compromissos)):
        if compromissos[i].descricao == '':
            print("A operação não foi realizada! A atividade não tem descrição!")
            return False
        novaAtividade = " ".join([compromissos[i].data,compromissos[i].hora,compromissos[i].prioridade,compromissos[i].descricao,compromissos[i].contexto,compromissos[i].projeto])
        novaAtividade = novaAtividade.strip()
        try:
            fp = open(TODO_FILE, 'a')
            fp.write(novaAtividade + "\n")
        except IOError as err:
            print("Não foi possível escrever para o arquivo " + TODO_FILE)
            print(err)
            return False
        finally:
            fp.close()
    return True

# Valida a prioridade.
def prioridadeValida(prioridade):
    if len(prioridade) == 3:
        if prioridade[0] == "(" and prioridade[2] == ")":
            if soLetra(prioridade[1]):
                return True
    return False

def soLetra(caractere):
    if type(caractere) != str:
        return False
    for letra in caractere.upper():
      if letra < 'A' or letra > 'Z':
          return False
    return True

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin):
    if len(horaMin) != 4 or not soDigitos(horaMin):
        return False
    else:
        horas = int(horaMin[0:2])
        minutos = int(horaMin[2:4])
        if horas > 23:
            return False
        if minutos > 59:
            return False
        return True


# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto.
def dataValida(data):
    if len(data) != 8 or not soDigitos(data):
        return False
    else:
      dia = int(data[0:2])
      mes = int(data[2:4])
      if mes in [1, 3, 5, 7, 8, 10, 12]:
          nDiasMes = 31
      elif mes in [4, 6, 9, 11]:
          nDiasMes = 30
      elif mes == 2:
          nDiasMes = 29
      else:
          return False
      if dia < 1 or dia > nDiasMes:
          return False
      return True

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
def soDigitos(numero):
    if type(numero) != str:
        return False
    for digito in numero:
        if digito < '0' or digito > '9':
            return False
    return True


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
    compromissos = []

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
        if len(tokens):
            descricao = " ".join(tokens)

        # A linha abaixo inclui em itens um objeto contendo as informações relativas aos compromissos
        # nas várias linhas do arquivo.
        # itens.append(...)
        compromissos.append(Compromisso(descricao,prioridade, data, hora,contexto, projeto))

    return compromissos


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados).
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.
def listar():
    linhas = []
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        for linha in arquivoTODO:
            linhas.append(linha)
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()
    return


def ordenarPorDataHora(itens):
    ################ COMPLETAR

    return itens


def ordenarPorPrioridade(itens):
    ################ COMPLETAR

    return itens


def fazer(num):
    ################ COMPLETAR

    return


def remover():
    ################ COMPLETAR

    return


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'.
def priorizar(num, prioridade):
    ################ COMPLETAR

    return


def desenhar(dias):
    ################ COMPLETAR

    return


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.
def processarComandos(comandos):
    print(comandos)
    if comandos[1] == ADICIONAR:
        comandos.pop(0)  # remove 'agenda.py'
        comandos.pop(0)  # remove 'adicionar'
        print(comandos)
        itemParaAdicionar = organizar([' '.join(comandos)])
        # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
        adicionar(itemParaAdicionar)  # novos itens não têm prioridade
    elif comandos[1] == LISTAR:
        if len(comandos) == 3:
            listar(comandos[2])
        elif len(comandos) == 2:
            listar()
        else:
            print("A operação não foi realizada! O comando é invalido!")
    elif comandos[1] == REMOVER:
        return

        ################ COMPLETAR

    elif comandos[1] == FAZER:
        return

        ################ COMPLETAR

    elif comandos[1] == PRIORIZAR:
        return

        ################ COMPLETAR

    else:
        print("Comando inválido.")


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