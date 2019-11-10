# -*- coding: utf-8 -*-
"""

@author: Vinícius
"""
from fita import Fita
from time import sleep
from bloco import Bloco
from transicao import Transicao
from blocoTransicao import BlocoTransicao

class MT(object):
    # Configuração Padrao, Constante
    MODO_RESUME        = 0
    MODO_VERBOSE       = 1
    MAX_STEPS          = 100
    DELIMITADOR    = ['(', ')']

    def __init__(self, config):
        self.blocos      = []
        self.alfabeto    = ['*', '_']
        self.modo        = config[0]
        self.passos      = config[1]
        self.delimitador = config[2]
        self.fita        = Fita(self.delimitador)
        # Variaveis para execucao:
        self.inicio            = False
        self.estadoAnterior    = None
        self.blocoAtual        = None   # Bloco a ser processado
        self.stack             = []     # Para chamada de blocos
        return

    def execucao(self):
        # Determina o bloco de inicio da maquina
        if(self.blocoAtual == None):
            main = self.pegaOBloco("............main")

            # Se não tiver o bloco main, ERROR
            if(main == None):
                print("\n> Bloco 'main' nao especificado.")
                return False
            self.blocoAtual = main
        # Executa
        stop = False
        for i in range(0, self.passos + 1):
            # Realiza um passo
            stop = self.executaPassos()
            # Terminate ou pause
            if(stop == 1) or (stop == 2):
                break
            # Excedeu limite de passos
            elif i == self.passos:
                stop = 2 # Pause
            # Execucao verbose, passoa a passo
            if self.modo == MT.MODO_VERBOSE:
                sleep(0.05)

        # Execucao resume, apenas o fim
        if self.modo == MT.MODO_RESUME:
            self.fita.Imprime(self.blocoAtual.nome, self.estadoAnterior)

        # Se houver uma pausa, informe ao simturing.py
        if stop == 2:
            return True

        return False
    # Execução de apenas um passo do simulador da maquina de Turing
    def executaPassos(self):
        # Inicio do cabeçote
        if(self.fita.indice == -1) and (self.inicio == False):
            self.fita.moverFita(Fita.MOVE_DIREITA)
            if self.modo == MT.MODO_VERBOSE:
                self.fita.Imprime(self.blocoAtual.nome, self.blocoAtual.estadoAtual)
            self.inicio = True
            return 0

        # Imprime o cabecote
        if self.modo == MT.MODO_VERBOSE:
            self.fita.Imprime(self.blocoAtual.nome, self.blocoAtual.estadoAtual)

        # Executa a transicao no bloco
        novo = self.blocoAtual.passosBloco(self.fita, self.stack)
        # Determina o novo bloco
        if(novo == None): # Nao levou a lugar algum
            # Verifica se ha algum bloco para retornar
            if len(self.stack) == 0:
                print("\n> Nao existem mais transicoes possiveis.")
                return 1
            else:
                # Retorna ate o bloco que o chamou no estado
                (block, state) = self.stack.pop()
                self.blocoAtual = block
                self.blocoAtual.estadoAtual = state
        # Parar a execucao
        elif novo == "pare":
            return 1
        # Pausar a execucao
        elif novo == "pause":
            print("\n> Execucao pausada.")
            return 2
        else:
            # Atualiza o bloco atual
            self.blocoAtual = novo
            
        self.estadoAnterior = self.blocoAtual.estadoAtual
        return 0
    # Verifica se a entrada é valida e carrega para o cabeçote
    def verificaEntrada(self, entrada):
        for c in entrada:
            if c in self.alfabeto:
                continue
            else:
                print("> A entrada possui simbolos invalidos.")
                return True

        self.fita.entradaParaFita = entrada
        return False
    
    # Novo bloco para maquina
    def addBlocoMT(self, nomeDoBloco, estadoInicial):
        if self.existeBloco(nomeDoBloco):
            oBloco = self.pegaOBloco(nomeDoBloco)
            oBloco.inicial = estadoInicial
            oBloco.estadoAtual = estadoInicial
            return
        # Cria novo bloco
        novoBloco = Bloco(nomeDoBloco)
        novoBloco.inicial = estadoInicial
        novoBloco.estadoAtual = estadoInicial

        self.blocos.append(novoBloco)
        return novoBloco

    def existeBloco(self, nome):
        for b in self.blocos:
            if b.nome == nome:
                return True
        return False

    def pegaOBloco(self, nome):
        for b in self.blocos:
            if b.nome == nome:
                return b

        return None
    # Adiciona uma nova transição entre blocos para o bloco
    def addBlocoTransicao(self, inicial, retornoBloco, nomeDoBloco, destino):
        blocoLocal = self.pegaOBloco(nomeDoBloco)
        destinoBloco = self.pegaOBloco(destino)

        # Se o bloco alvo ainda nao foi criado cria um novo bloco
        if(destinoBloco == None):
            destinoBloco = self.addBlocoMT(destino, "###")

        novaTransi = BlocoTransicao(inicial, retornoBloco, blocoLocal, destinoBloco)
        blocoLocal.addBlocoTransicao(novaTransi)
        return
    # Adiciona uma nova transição entre estados para o bloco
    def addTransicao(self, partida, destino, simboloAtual, simboloNovo, movimento, nomeDoBloco, pause):
        blocoLocal = self.pegaOBloco(nomeDoBloco)
        # Adiciona simbolo no alfabeto
        if simboloAtual not in self.alfabeto:
            self.alfabeto.append(simboloAtual)

        blocoLocal.addEstado(partida)
        blocoLocal.addEstado(destino)
        blocoLocal.addnoAlfabeto(simboloAtual)
        blocoLocal.addoutAlfabeto(simboloNovo)

        movement = ""
        if movimento == 'e':
            movement = Fita.MOVE_ESQUERDA
        elif movimento == 'd':
            movement = Fita.MOVE_DIREITA
        else:
            movement = Fita.IMOVEL

        novaTrans = Transicao(partida, destino, simboloAtual, simboloNovo, movement, pause)
        blocoLocal.addTransicao(novaTrans)
        return

    def setarConfiguracoes(self, config):
        self.modo  = config[0]
        self.passos = config[1]
        self.fita.delimitador = config[2]
        return