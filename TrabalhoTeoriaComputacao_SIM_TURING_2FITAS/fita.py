# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

class Fita(object):
    MOVE_ESQUERDA = 'e'
    MOVE_DIREITA = 'd'
    IMOVEL = 'i'

    def __init__(self, delimitador):
        self.entradaParaFita = ""
        self.indice = -1
        self.delimitador = delimitador
        return

    # Escreve caractere no cabecote    
    def escreveNaFita(self, caractere):
        if(caractere == "*"):
            return
        
        if(self.indice >= 0):
            resultadoFita = self.entradaParaFita[:self.indice] + caractere + self.entradaParaFita[(self.indice + 1):]
        else:
            resultadoFita = caractere + self.entradaParaFita[0:]
            self.indice += 1
        self.entradaParaFita = resultadoFita
        return

    def caractereAtual(self):
        if((self.indice < 0) or (self.indice >= len(self.entradaParaFita))):
            return '_'

        return self.entradaParaFita[self.indice]

    # Ajusta o indice onde se encontra o cabecote da fita dependendo do movimento que fizer
    def moverFita(self, direcao):
        if(direcao == Fita.MOVE_DIREITA):
            self.indice += 1
        elif(direcao == Fita.MOVE_ESQUERDA):
            self.indice -= 1
        return

    def Imprime(self, bloco, estado, fita2):
        if(estado == "retorne"):
            estado = "rtrn"

        result = bloco + "." + estado + ": "
        resultadoFita = ""
        stringL = len(self.entradaParaFita)

        if(self.indice >= 0):
            # Fatiamento ":", pega o caracter entre um intervalo de valores da posicao de uma string 
            caracteSelecionado = self.entradaParaFita[self.indice:(self.indice + 1)]

            if(caracteSelecionado == ""):
                caracteSelecionado = "_"

            resultadoFita = self.entradaParaFita[:self.indice] + self.delimitador[0] + caracteSelecionado
            resultadoFita += self.delimitador[1] + self.entradaParaFita[(self.indice + 1):]

            if(caracteSelecionado == "_"):
                stringL += 1

            # 20 eh o tamanho da fita que sera permitido visualizar
            qtd = (20 - self.indice)

            # Precisa cortar o inicio da string
            if(qtd < 0):
                resultadoFita = resultadoFita[(self.indice - 20):]
            else:
                for i in range(0, qtd):
                    resultadoFita = '_' + resultadoFita

            qtd = 20 - stringL + self.indice

            # Precisa cortar o fim da string
            if(qtd < 0):
                resultadoFita = resultadoFita[:(-(stringL - 20 - self.indice))]
            # Precisa adicionar '_':
            else:
                for i in range(0, qtd):
                    resultadoFita = resultadoFita + '_'
        else:
            # Index menor que zero
            resultadoFita = self.entradaParaFita
            qtd = 20 + self.indice + 1

            for i in range(0, qtd):
                resultadoFita = '_' + resultadoFita

            indice = 0

            resultadoFita = resultadoFita[:qtd] + self.delimitador[0] + '_'
            resultadoFita += self.delimitador[1] + self.entradaParaFita

            qtd = 20 - stringL + self.indice

            # Precisa cortar o fim da string
            if(qtd < 0):
                resultadoFita = resultadoFita[:(-(stringL - 20 - self.indice))]
            # Precisa adicionar '_'
            else:
                for i in range(0, qtd):
                    resultadoFita = resultadoFita + '_'

        result += resultadoFita + " : " + fita2

        print(result)
        return
