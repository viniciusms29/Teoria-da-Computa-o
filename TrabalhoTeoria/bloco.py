# -*- coding: utf-8 -*-
"""

@author: Vinícius Morais dos Santos - 0002864
"""
from transicao import Transicao


class Bloco(object):
    def __init__(self, nomeDoBloco):
        self.nome = nomeDoBloco
        self.inicial = None
        self.noAlfabeto = ['*', '_']  # Pode ler da fita
        self.outAlfabeto = []  # Pode escrever na fita
        self.estados = []
        self.finais = []
        self.transicoes = []
        self.blocoTransicao = []
        self.estadoAtual = None
        return

    def passosBloco(self, fita, stack):
        # Para parar a execução
        if self.estadoAtual == "pare":
            self.estadoAtual = self.inicial
            return "pare"
        # Retornar a execucao ao bloco anterior
        if self.estadoAtual == "retorne":
            self.estadoAtual = self.inicial
            return None

        caract = fita.caractereAtual()

        for tr in self.transicoes:
            # Procura transicao valida
            if (tr.partida == self.estadoAtual) and ((tr.simboloAtual == caract) or (tr.simboloAtual == "*")):
                # * significa que não muda de estado
                proximoEstado = tr.destino
                if proximoEstado != "*":
                    self.estadoAtual = tr.destino
                # Escreve o caractere na fita
                fita.escreveNaFita(tr.simboloNovo)
                # Move cabecote
                fita.moverFita(tr.movimento)
                # Se tiver exclamacao
                if tr.pause:
                    return "pause"
                # Retorna o bloco atual (permanece no bloco)
                return self
        # Olha se o estado se o estado direciona para um novo bloco
        for trBloco in self.blocoTransicao:
            if trBloco.estadoInicial == self.estadoAtual:
                # Empilha o bloco chamador e o estado de retorno
                stack.append((self, trBloco.retornoBloco))
                return trBloco.blocoDestino
        # Nao tem transição valida
        return None
    # Novo estado para a maquina
    def addEstado(self, estado):
        if estado not in self.estados:
            self.estados.append(estado)
    # Adiciona no alfabeto que que pode ler da fita
    def addnoAlfabeto(self, simbolo):
        if simbolo not in self.noAlfabeto:
            self.noAlfabeto.append(simbolo)
    # Adiciona no alfabeto que pode escrever na fita
    def addoutAlfabeto(self, simbolo):
        if simbolo not in self.outAlfabeto:
            self.outAlfabeto.append(simbolo)

    def addTransicao(self, trans):
        aux = False
        for t in self.transicoes:
            if t.equals(trans):
                aux = True

        if not aux:
            self.transicoes.append(trans)
        return

    def addBlocoTransicao(self, trans):
        aux = False
        for t in self.blocoTransicao:
            if t.equals(trans):
                aux = True

        if not aux:
            self.blocoTransicao.append(trans)
        return