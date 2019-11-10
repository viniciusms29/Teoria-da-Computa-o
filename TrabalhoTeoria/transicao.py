# -*- coding: utf-8 -*-
"""

@author: Vinícius Morais dos Santos - 0002864
"""

class Transicao(object):
    def __init__(self, partida, destino, simboloAtual, simboloNovo, movimento, pause):
        self.partida = partida
        self.destino = destino
        self.simboloAtual = simboloAtual
        self.simboloNovo = simboloNovo
        self.movimento = movimento
        self.pause = pause
        return

    def equals(self, transicao):
        if ((self.partida == transicao.partida) and
                (self.destino == transicao.destino) and
                (self.simboloAtual == transicao.simboloAtual) and
                (self.simboloNovo == transicao.simboloNovo) and
                (self.movimento == transicao.movimento)):
            return True
        return False
