TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

class Compromisso:
    def __init__(self, descricao, prioridade, data,hora, contexto, projeto):
        self.descricao = descricao
        self.prioridade = prioridade
        self.data = data
        self.hora = hora
        self.contexto = contexto
        self.projeto = projeto
        return

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
        compromissos = organizar(linhas)
    for i in range(len(compromissos)):
        print('listar compromisso', i, compromissos[i].data, compromissos[i].hora, compromissos[i].prioridade,
         compromissos[i].descricao, compromissos[i].contexto, compromissos[i].projeto)

    return

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

def projetoValido(projeto):
    if len(projeto) >= 2 and projeto[0] == '+':
        return True
    return False

def contextoValido(contexo):
    if len(contexo) >= 2 and contexo[0] == '@':
        return True
    return False

def soDigitos(numero):
    if type(numero) != str:
        return False
    for digito in numero:
        if digito < '0' or digito > '9':
            return False
    return True

def organizar(linhas):
    compromissos = []

    for texto in linhas:
        data = ''
        hora = ''
        prioridade = ''
        descricao = ''
        contexto = ''
        projeto = ''

        texto = texto.strip()
        tokens = texto.split()

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
            #print(tokens)
            descricao = " ".join(tokens)
            #print(descricao)

        compromissos.append(Compromisso(descricao,prioridade, data, hora,contexto, projeto))

    return compromissos

cont = True

while cont:
    #arg = ['23052017 1030 Reunião com Huguinho, Luizinho e Zezinho. @Skype +Pesquisa','(B) Terminar a especificação do projeto de IN1076. +IN1076']
    #compromissos = organizar(arg)
    #for i in range (len(compromissos)):
        #print('compromisso', i , compromissos[i].data , compromissos[i].hora , compromissos[i].prioridade , compromissos[i].descricao , compromissos[i].contexto , compromissos[i].projeto)
    #adicionar(compromissos)
    listar()
    cont = False