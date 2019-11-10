# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

import sys
import MaquinaTuring
import analiseIO

def main():
    # Cabeçalho
    cabecalho = "\tSimulador de Maquina de Turing ver 1.0."
    cabecalho += "\n\tDesenvolvido como trabalho pratico para a disciplina de Teoria da Computacao."
    cabecalho += "\n\tVinicius Morais dos Santos, IFMG - 2019."
    cabecalho += "\n\tVinicius Alves de Araujo, IFMG - 2019.\n"

    print(cabecalho)

    # Interpreta os argumentos que foram passados pelo terminal
    entrada = analiseIO.AnalisadorIO(sys.argv)
    configuracao = entrada.AnalisaEntradaConf()

    # Se a entrada nao estiver correta, finaliza
    if(configuracao == None):
        sys.exit()

    # Cria o simulador da maquina de turing
    simulador = MaquinaTuring.MT(configuracao)

    entrada.AnalisadorArqEntrada(simulador)
    palavraInicial = input("Forneca a Palavra inicial: ")
    erro = simulador.verificaEntrada(palavraInicial)

    if erro:
        sys.exit()

    # Executa o simulador da maquina de Turing
    pausa = True

    while(pausa):
        pausa = simulador.execucao()
        
        if(pausa):
            configuracao = entrada.reconfigurar(configuracao)
            simulador.setarConfiguracoes(configuracao)

if (__name__ == "__main__"):
    main()
