# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

class BlocoTransicao(object):

    def __init__(self, estadoInicial, retornoBloco, blocoPartida, blocoDestino):
        self.estadoInicial = estadoInicial
        self.retornoBloco = retornoBloco
        self.blocoPartida = blocoPartida
        self.blocoDestino = blocoDestino
        return

    def equals(self, transicao):
        if ((self.estadoInicial == transicao.estadoInicial) and
                (self.retornoBloco == transicao.retornoBloco) and
                (self.blocoPartida.name == transicao.blocoPartida.name) and
                (self.blocoDestino.name == transicao.blocoDestino.name)):
            return True
        return False
