# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

class Acao(object):
    def __init__(self, partida, reservada, destino):
        self.partida = partida
        self.reservada = reservada
        self.destino = destino
        return

    def equals(self, transicao):
        if((self.partida == transicao.partida) and
                (self.reservada == transicao.reservada) and
                (self.destino == transicao.destino)):
            return True
        return False
