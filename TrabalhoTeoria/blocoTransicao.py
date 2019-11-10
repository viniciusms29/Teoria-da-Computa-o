# -*- coding: utf-8 -*-
"""

@author: Vinícius Morais dos Santos - 0002864
"""


class BlocoTransicao(object):

    def __init__(self, estadoInicial, retornoBloco, blocoPartida, blocoDestino):
        self.estadoInicial = estadoInicial
        self.retornoBloco = retornoBloco
        self.blocoPartida = blocoPartida
        self.blocoDestino = blocoDestino
        return

    def equals(self, trans):
        if ((self.estadoInicial == trans.estadoInicial) and
                (self.retornoBloco == trans.retornoBloco) and
                (self.blocoPartida.name == trans.blocoPartida.name) and
                (self.blocoDestino.name == trans.blocoDestino.name)):
            return True
        return False
