# -*- coding: utf-8 -*-
"""

@author: Vinícius
"""
import sys
import MaquinaTuring
import analiseIO

def main():
    # Cabeçalho
    print("Simulador de Maquina de Turing ver 1.0.")
    print("Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.")
    print("Vinícius Morais dos Santos, IFMG, 2018.\n")
    # Interpreta os argumentos que foram passados pelo terminal
    entrada = analiseIO.AnalisadorIO(sys.argv)
    configuracao = entrada.AnalisaEntradaConf()
    if (configuracao == None):
        sys.exit()
    # Cria a maquina de turing
    simulador = MaquinaTuring.MT(configuracao)
    entrada.AnalisadorArqEntrada(simulador)
    palavraInicial = input("Forneça a Palavra inicial: ")
    erro = simulador.verificaEntrada(palavraInicial)
    if erro:
        sys.exit()
    # Executa o simulador da maquina de Turing
    pausa = True
    while pausa:
        pausa = simulador.execucao()
        if pausa:
            configuracao = entrada.reconfigurar(configuracao)
            simulador.setarConfiguracoes(configuracao)

if (__name__ == "__main__"):
    main()