# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

from transicao import Transicao
from time import sleep


class Bloco(object):
    def __init__(self, nomeDoBloco):
        self.nome = nomeDoBloco
        self.inicial = None
        # Tirar esse comentario abaixo para rodar o teste.mt (Nao precisa)
        """
        self.noAlfabeto = ['.', '#', ' ', '_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                         'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0',
                         '1', '2', '3', '4', '5', '6', '7', '8', '9']"""
        self.noAlfabeto = ['*', '_', ' ', '#', '.']  # Pode ler da fita
        self.outAlfabeto = []  # Pode escrever na fita
        self.estados = []
        self.finais = []
        self.transicoes = []
        self.transicoesAcao = []
        self.blocoTransicao = []
        self.estadoAtual = None

        #Adiciona os caracteres do alfabeto de "A"..."Z"
        for c in range(65, 91):
            self.noAlfabeto.append(chr(c))

        #Adiciona os caracteres do alfabeto de "a"..."z"
        for c in range(97, 123):
            self.noAlfabeto.append(chr(c))

        #Adiciona os caracteres do alfabeto de "0"..."9"
        for c in range(48, 58):
            self.noAlfabeto.append(chr(c))
        return

    # Novo estado para a maquina
    def addEstado(self, estado):
        if(estado not in self.estados):
            self.estados.append(estado)

    # Adiciona no alfabeto que que pode ler da fita
    def addnoAlfabeto(self, simbolo):
        if(simbolo not in self.noAlfabeto):
            self.noAlfabeto.append(simbolo)

    def addAcao(self, trans):
        aux = False

        for t in self.transicoesAcao:
            if(t.equals(trans)):
                aux = True

        if(not aux):
            self.transicoesAcao.append(trans)

        return

    def addBlocoTransicao(self, trans):
        aux = False

        for t in self.blocoTransicao:
            if(t.equals(trans)):
                aux = True

        if(not aux):
            self.blocoTransicao.append(trans)

        return

    def addTransicao(self, trans):
        aux = False

        for t in self.transicoes:
            if(t.equals(trans)):
                aux = True

        if(not aux):
            self.transicoes.append(trans)
            
        return

    def passosBloco(self, fita, fita2, posFita2, stack, modoE):
        # Para parar a execução
        if(self.estadoAtual == "pare"):
            self.estadoAtual = self.inicial
            return "pare"
        # Retornar a execucao ao bloco anterior
        if(self.estadoAtual == "retorne"):
            self.estadoAtual = self.inicial
            return None

        caract = fita.caractereAtual()

        # Olha se o estado direciona para um novo estado
        for tr in self.transicoes:
            # Procura transicao valida para fita ou para a fita2
            if(tr.segFita):
                if((tr.partida == self.estadoAtual) and 
                    ((tr.simboloAtual == fita2) or (tr.simboloAtual == "*"))):
                    proximoEstado = tr.destino

                    # Se estado for "*" significa que nao muda de estado
                    if(proximoEstado != "*"):
                        self.estadoAtual = tr.destino

                    # Escreve o caractere na fita
                    fita.escreveNaFita(tr.simboloNovo)
                    # Move cabecote
                    fita.moverFita(tr.movimento)

                    # Se tiver exclamacao
                    if(tr.pause):
                        return "pause"

                    # Retorna o bloco atual (permanece no bloco)
                    return self
            else:
                if((tr.partida == self.estadoAtual) and 
                    ((tr.simboloAtual == caract) or (tr.simboloAtual == "*"))):
                    proximoEstado = tr.destino

                    # Se estado for "*" significa que nao muda de estado
                    if(proximoEstado != "*"):
                        self.estadoAtual = tr.destino

                    # Escreve o caractere na fita
                    fita.escreveNaFita(tr.simboloNovo)
                    # Move cabecote
                    fita.moverFita(tr.movimento)

                    # Se tiver exclamacao
                    if(tr.pause):
                        return "pause"

                    # Retorna o bloco atual (permanece no bloco)
                    return self

        # Olha se o estado direciona para uma acao para a segunda fita
        for trAcao in self.transicoesAcao:
            if(trAcao.partida == self.estadoAtual):
                proximoEstado = trAcao.destino

                # Se estado for "*" significa que nao muda de estado
                if(proximoEstado != "*"):
                    self.estadoAtual = trAcao.destino

                # Verifica qual a acao reservada vai ser realizada
                if(trAcao.reservada == "copiar"):
                    # copia da fita para fita2
                    infFita2 = []

                    infFita2.append(caract)
                    infFita2.append(fita.indice)
                    
                    return infFita2
                # Se nao foi a acao de copiar, realiza a de colar
                else:
                    if(fita.indice == posFita2):
                        listaAux = None
                        listaAux = list(fita.entradaParaFita)
                        listaAux[fita.indice] = fita2
                        fita.entradaParaFita = ''.join(listaAux)
                    else:
                        if(fita.indice > posFita2):
                            while (fita.indice != posFita2):
                                fita.moverFita(fita.MOVE_ESQUERDA)
                                if(modoE == 1):
                                    fita.Imprime(self.nome, self.estadoAtual, fita2)
                                    sleep(0.05)
                        else:
                            while (fita.indice != posFita2):
                                fita.moverFita(fita.MOVE_DIREITA)
                                if(modoE == 2):
                                    fita.Imprime(self.nome, self.estadoAtual, fita2)
                                    sleep(0.05)

                        listaAux = None
                        listaAux = list(fita.entradaParaFita)
                        listaAux[fita.indice] = fita2
                        fita.entradaParaFita = ''.join(listaAux)

                return self

        # Olha se o estado direciona para um novo bloco
        for trBloco in self.blocoTransicao:
            if(trBloco.estadoInicial == self.estadoAtual):
                # Empilha o bloco chamador e o estado de retorno
                stack.append((self, trBloco.retornoBloco))
                return trBloco.blocoDestino

        return None
    
    # Adiciona no alfabeto que pode escrever na fita
    def addoutAlfabeto(self, simbolo):
        if simbolo not in self.outAlfabeto:
            self.outAlfabeto.append(simbolo)
