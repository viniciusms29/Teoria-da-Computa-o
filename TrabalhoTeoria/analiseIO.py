# -*- coding: utf-8 -*-
"""

@author: Vinícius
"""
from pathlib import Path
from MaquinaTuring import MT


class AnalisadorIO:

    def __init__(self, data):
        self.data = data
        self.entradaArq = None
        self.mt = None
    # Função que recebe toda a linha digitada no terminal, e retorna um array com o modo de execucao, numero de steps
    # e o delimitador, ou None se ocorrer algo errado no que foi digitado
    def AnalisaEntradaConf(self):
        # Precisa de pelo menos o nome do programa e arquivo
        if len(self.data) < 2:
            print("\n> Entrada no terminal incorreta")
            return None
        # Verifica existencia do arquivo
        self.entradaArq = self.data[len(self.data) - 1]
        filepath = Path(self.entradaArq)
        if filepath.is_file() == False:
            print("\n> Arquivo de entrada invalido.")
            return None

        # Cria a array de configuração, o que será retornado se o que foi digitado do terminal estiver correto
        configuracao = [MT.MODO_RESUME, MT.MAX_STEPS, MT.DELIMITADOR]
        # Verifica os argumentos
        achouCabecote = False
        achouPassos = False
        for i in range(1, len(self.data) - 1):
            argumento = self.data[i]
            if (((argumento == "-resume") or (argumento == "-r")) and (achouCabecote == False) and (
                    achouPassos == False)):
                configuracao[0] = MT.MODO_RESUME
            elif (((argumento == "-verbose") or (argumento == "-v")) and (achouCabecote == False) and (
                    achouPassos == False)):
                configuracao[0] = MT.MODO_VERBOSE
            elif (((argumento == "-head") or (argumento == "-h")) and (achouCabecote == False) and (
                    achouPassos == False)):
                achouCabecote = True
            elif (((argumento == "-step") or (argumento == "-s")) and (achouCabecote == False) and (
                    achouPassos == False)):
                achouPassos = True
            elif achouPassos:
                configuracao[1] = int(argumento)
                achouPassos = False
            elif achouCabecote:
                delim = self.verifacaCabecote(argumento)
                if (delim == None):
                    print("\nDelimitador " + argumento + " invalido.")
                    return None

                configuracao[2] = delim
                achouCabecote = False

        return configuracao
    # Função que permite reconfigurar a maquina depois de executar a quantidade de passos definidos, ou somente continuar a execução
    def reconfigurar(self, iniConfig):
        print("\nFoi alcançado o limete de passo.\n"+
              "Aperte enter para continuar ou configure a maquina com para executar das formas seguinte.")
        print("-v ou -verbose\n" +
              "\n-r ou -resume\n" +
              "\n-s # ou -step #\n" +
              "\n-h '[]' ou -head '[]'\n")
        line = input("Configuração: ");
        print("")
        aLine = line.split()
        configuracao = [iniConfig[0], iniConfig[1], iniConfig[2]]
        achouPassos = False
        achouCabecote = False
        for i in range(0, len(aLine)):
            argumento = aLine[i]

            if (((argumento == "-resume") or (argumento == "-r")) and (achouCabecote == False) and (
                    achouPassos == False)):
                configuracao[0] = MT.MODO_RESUME
            elif (((argumento == "-verbose") or (argumento == "-v")) and (achouCabecote == False) and (
                    achouPassos == False)):
                configuracao[0] = MT.MODO_VERBOSE
            elif (((argumento == "-head") or (argumento == "-h")) and (achouCabecote == False) and (
                    achouPassos == False)):
                achouCabecote = True
            elif (((argumento == "-step") or (argumento == "-s")) and (achouCabecote == False) and (
                    achouPassos == False)):
                achouPassos = True
            elif achouPassos:
                configuracao[1] = int(argumento)
                achouPassos = False
            elif achouCabecote:
                delim = [argumento[1], argumento[2]]
                configuracao[2] = delim
                achouCabecote = False

        return configuracao
    # Pega o arquivo que foi passado por linha de comando, o interpreta criando os blocos, estados, alfabeto e transições
    def AnalisadorArqEntrada(self, maquina):
        blocoAtual = ""
        try:
            with open(self.entradaArq) as file:
                for fileLinha in file:
                    # Divide a linha
                    linha = fileLinha.split()
                    # Ignora Comentários ou linha vazia
                    if (len(linha) == 0) or (linha[0] == ';'):
                        continue
                    # Inicio de um novo bloco
                    elif linha[0] == 'bloco':
                        blocoAtual = self.adicionaBloco(maquina, linha)
                    # Fim do bloco
                    elif linha[0] == 'fim':
                        continue
                    # Detectou Transicao
                    else:
                        self.adicionarTransicao(maquina, linha, blocoAtual)
        except IOError:
            print("Erro ao abrir arquivo.\n")

    def verifacaCabecote(self, delimit):
        # Delimitador so pode ter dois caracteres
        if len(delimit) != 2:
            return None

        return [delimit[0], delimit[1]]

    def adicionaBloco(self, maquina, linha):
        nome = self.formatarBloco(linha[1])
        inicial = self.formatarEstados(linha[2])
        maquina.addBlocoMT(nome, inicial)
        return nome

    def adicionarTransicao(self, maquina, linha, bloco):
        if linha[2] == "--":
            partida = self.formatarEstados(linha[0])
            simboloAtual = linha[1]
            simboloNovo = linha[3]
            movimento = linha[4]
            destino = self.formatarEstados(linha[5])

            pause = False
            if len(linha) > 6:
                pare = linha[6]
                if pare == "!":
                    pause = True
            maquina.addTransicao(partida, destino, simboloAtual, simboloNovo, movimento, bloco, pause)
        else:
            inicial = self.formatarEstados(linha[0])
            destino = self.formatarBloco(linha[1])
            retornoBloco = self.formatarEstados(linha[2])
            maquina.addBlocoTransicao(inicial, retornoBloco, bloco, destino)
        return

    def formatarBloco(self, nome):
        for i in range(0, (16 - len(nome))):
            nome = "." + nome

        return nome

    def formatarEstados(self, estado):
        if estado == "retorne":
            return "retorne"
        elif estado == "pare":
            return "pare"

        try:
            strEst = str(int(estado))
            for i in range(0, (4 - len(strEst))):
                strEst = "0" + strEst
            
            return strEst
        except ValueError:
            print("> (" + estado + "). Nome de estado invalido.")

        return