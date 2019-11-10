# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

from fita import Fita
from time import sleep
from acao import Acao
from bloco import Bloco
from transicao import Transicao
from blocoTransicao import BlocoTransicao

class MT(object):
    # Configuração Padrao, Constante
    MODO_RESUME        = 0
    MODO_VERBOSE       = 1
    MAX_STEPS          = 500
    DELIMITADOR    = ['(', ')']

    def __init__(self, config):
        self.blocos      = []
        # Tirar esse comentario abaixo para rodar o teste.mt (Nao precisa)
        """
        self.alfabeto = ['.', '#', ' ', '_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                         'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0',
                         '1', '2', '3', '4', '5', '6', '7', '8', '9']"""
        self.alfabeto    = ['*', '_', ' ', '#', '.']
        self.modo        = config[0]
        self.passos      = config[1]
        self.delimitador = config[2]
        self.fita        = Fita(self.delimitador)
        self.fita2       = "_"
        self.posFita2    = None     # Para salvar a posicao copiada da fita1
        # Variaveis para execucao:
        self.inicio            = False
        self.estadoAnterior    = None
        self.blocoAtual        = None   # Bloco a ser processado
        self.stack             = []     # Para chamada de blocos

        #Adiciona os caracteres do alfabeto de "A"..."Z"
        for c in range(65, 91):
            self.alfabeto.append(chr(c))

        #Adiciona os caracteres do alfabeto de "a"..."z"
        for c in range(97, 123):
            self.alfabeto.append(chr(c))

        #Adiciona os caracteres do alfabeto de "0"..."9"
        for c in range(48, 58):
            self.alfabeto.append(chr(c))
        return

    # Verifica se a entrada é valida e carrega para o cabeçote
    def verificaEntrada(self, entrada):
        for c in entrada:
            if(c in self.alfabeto):
                continue
            else:
                print("> A entrada possui simbolos invalidos.")
                return True

        self.fita.entradaParaFita = entrada
        return False

    # Adiciona uma nova transicao entre estado para acao
    def addAcao(self, partida, reserv, destino, nomeDoBloco):
        blocoLocal = self.pegaOBloco(nomeDoBloco)
        blocoLocal.addEstado(partida)
        blocoLocal.addEstado(destino)

        novaAcao = Acao(partida, reserv, destino)
        blocoLocal.addAcao(novaAcao)

    # Adiciona uma nova transicao entre blocos para o bloco
    def addBlocoTransicao(self, inicial, retornoBloco, nomeDoBloco, destino):
        blocoLocal = self.pegaOBloco(nomeDoBloco)
        destinoBloco = self.pegaOBloco(destino)

        # Se o bloco alvo ainda nao foi criado cria um novo bloco
        if(destinoBloco == None):
            destinoBloco = self.addBlocoMT(destino, "###")

        blocoLocal.addEstado(inicial)
        blocoLocal.addEstado(retornoBloco)

        novaBlocoTransi = BlocoTransicao(inicial, retornoBloco, blocoLocal, destinoBloco)
        blocoLocal.addBlocoTransicao(novaBlocoTransi)
        return
    
    # Adiciona uma nova transicao entre estados para o bloco
    def addTransicao(self, segFita, partida, destino, simboloAtual, simboloNovo, movimento, nomeDoBloco, pause):
        blocoLocal = self.pegaOBloco(nomeDoBloco)

        # Adiciona simbolo no alfabeto do simulador da maquina
        if(simboloAtual not in self.alfabeto):
            self.alfabeto.append(simboloAtual)

        blocoLocal.addEstado(partida)
        blocoLocal.addEstado(destino)
        blocoLocal.addnoAlfabeto(simboloAtual)
        blocoLocal.addoutAlfabeto(simboloNovo)

        movement = ""

        if(movimento == 'e'):
            movement = Fita.MOVE_ESQUERDA
        elif(movimento == 'd'):
            movement = Fita.MOVE_DIREITA
        else:
            movement = Fita.IMOVEL

        novaTrans = Transicao(segFita, partida, destino, simboloAtual, simboloNovo, movement, pause)
        blocoLocal.addTransicao(novaTrans)
        return

    def pegaOBloco(self, nome):
        for b in self.blocos:
            if(b.nome == nome):
                return b

        return None

    def existeBloco(self, nome):
        for b in self.blocos:
            if b.nome == nome:
                return True

        return False

    # Novo bloco de execucao para maquina
    def addBlocoMT(self, nomeDoBloco, estadoInicial):
        # Se existir apenas retorna o bloco da lista de blocos
        if self.existeBloco(nomeDoBloco):
            oBloco = self.pegaOBloco(nomeDoBloco)
            oBloco.inicial = estadoInicial
            oBloco.estadoAtual = estadoInicial
            return oBloco
            
        # Cria novo bloco
        novoBloco = Bloco(nomeDoBloco)
        novoBloco.inicial = estadoInicial
        novoBloco.estadoAtual = estadoInicial

        self.blocos.append(novoBloco)
        return novoBloco

    # Execucao de apenas um passo do simulador da maquina de Turing
    def executaPassos(self):
        # Inicio do cabeçote
        if(self.fita.indice == -1) and (self.inicio == False):
            self.fita.moverFita(Fita.MOVE_DIREITA)

            if(self.modo == MT.MODO_VERBOSE):
                self.fita.Imprime(self.blocoAtual.nome, self.blocoAtual.estadoAtual, self.fita2)

            self.inicio = True
            return 0

        # Imprime o cabecote
        if(self.modo == MT.MODO_VERBOSE):
            self.fita.Imprime(self.blocoAtual.nome, self.blocoAtual.estadoAtual, self.fita2)


        verb = 1
        resu = 2
        # Executa a transicao no bloco
        if(self.modo == MT.MODO_VERBOSE):
            novo = self.blocoAtual.passosBloco(self.fita, self.fita2, self.posFita2, self.stack,verb)
        else:
            novo = self.blocoAtual.passosBloco(self.fita, self.fita2, self.posFita2, self.stack,resu)

        # novo = self.blocoAtual.passosBloco(self.fita, self.fita2, self.posFita2, self.stack)
        self.estadoAnterior = self.blocoAtual.estadoAtual

        # Determina o novo bloco
        if(novo == None): # Nao levou a lugar algum
            # Verifica se ha algum bloco para retornar
            if(len(self.stack) == 0):
                print("\n> Nao existem mais transicoes possiveis.")
                return 1
            else:
                # Retorna ate o bloco que o chamou no estado
                (block, state) = self.stack.pop()
                self.blocoAtual = block
                self.blocoAtual.estadoAtual = state
        # Parar a execucao
        elif(novo == "pare"):
            return 1
        # Pausar a execucao
        elif(novo == "pause"):
            print("\n> Execucao pausada.")
            return 2
        elif(type(novo) is list):
            if(len(novo) == 2):
                self.fita2 = novo[0]
                self.posFita2 = novo[1]
            else:
                self.blocoAtual = novo[0]
                self.fita2 = novo[1]
                self.posFita2 = novo[2]
        else:
            # Atualiza o bloco atual
            self.blocoAtual = novo

        return 0

    def execucao(self):
        # Determina o bloco de inicio da maquina, bloco 'main'
        if(self.blocoAtual == None):
            main = self.pegaOBloco("............main")

            # Se não tiver o bloco main, ERROR
            if(main == None):
                print("\n> Bloco 'main' nao especificado.")
                return False

            self.blocoAtual = main

        stop = False

        # Executa
        for i in range(1, self.passos + 1):
            # Realiza um passo
            stop = self.executaPassos()

            # Terminate ou pause
            if((stop == 1) or (stop == 2)):
                break
            # Excedeu limite de passos
            elif(i == self.passos):
                stop = 2 # Pause
            # Execucao verbose, passo a passo
            if(self.modo == MT.MODO_VERBOSE):
                sleep(0.05)

        # Execucao resume, apenas o fim
        if(self.modo == MT.MODO_RESUME):
            self.fita.Imprime(self.blocoAtual.nome, self.estadoAnterior, self.fita2)

        # Se houver uma pausa, informe ao simturing.py
        if(stop == 2):
            return True

        return False
 
    def setarConfiguracoes(self, config):
        self.modo  = config[0]
        self.passos = config[1]
        self.fita.delimitador = config[2]
        return
