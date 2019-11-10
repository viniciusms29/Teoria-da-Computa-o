# -*- coding: utf-8 -*-

"""
@author: Vinicius Morais
@author: Vinicius Araujo
"""

from pathlib import Path
from MaquinaTuring import MT

class AnalisadorIO:

    def __init__(self, data):
        self.data = data
        self.entradaArq = None
        self.mt = None

    def formatarEstados(self, estado):
        if estado == "retorne":
            return "retorne"
        elif estado == "pare":
            return "pare"

        try:
            strEst = str(int(estado))

            # Completa com 0 respeitando o tamanho de 4 caracteres
            for i in range(0, (4 - len(strEst))):
                strEst = "0" + strEst
            
            return strEst
        except ValueError:
            print("> (" + estado + "). Nome de estado invalido.")

        return

    def formatarBloco(self, nome):
        # Desenha os "." respeitando o tamanho de 16 caracteres
        for i in range(0, (16 - len(nome))):
            nome = "." + nome

        return nome

    def verificaSimboloSegundaFita(self, simbolo):
        # Verifica se o simbolo atual tem tamanho maior que 1, se for, eh simbolo da segunda fita
        if(len(simbolo) > 1):
            # Tem que estar entre colchetes
            if((simbolo[0] == "[") and (simbolo[2] == "]")):
                return simbolo[1]
            else:
                print("> (" + simbolo + "). Simbolo invalido.")
                sys.exit()

        return None
    
    def adicionaBloco(self, maquina, linha):
        nome = self.formatarBloco(linha[1])
        inicial = self.formatarEstados(linha[2])
        maquina.addBlocoMT(nome, inicial)
        return nome

    def adicionarTransicao(self, maquina, linha, bloco):
        # Tratamento normal
        if(linha[2] == "--"):
            partida = self.formatarEstados(linha[0])

            simbAux = self.verificaSimboloSegundaFita(linha[1])

            if(simbAux != None):
                simboloAtual = simbAux
                segFita = True
            else: 
                simboloAtual = linha[1]
                segFita = False

            simboloNovo = linha[3]
            movimento = linha[4]
            destino = self.formatarEstados(linha[5])

            pause = False

            """
                Se houver mais informacoes do que as esperadas, verifica se nao eh o sinal de break "!"
                se for, ele para a execucao, se nao, ele realiza a execucao
            """
            if(len(linha) > 6):
                pare = linha[6]

                if pare == "!":
                    pause = True

            maquina.addTransicao(segFita, partida, destino, simboloAtual, simboloNovo, movimento, bloco, pause)

        # Trata as palavras reservadas: copiar e colar
        elif((linha[1] == "copiar") or (linha[1] == "colar")):
            partida = self.formatarEstados(linha[0])
            reserv  = linha[1] 
            destino = self.formatarEstados(linha[2])

            maquina.addAcao(partida, reserv, destino, bloco)
        # Trata transicao de blocos
        else:
            partida = self.formatarEstados(linha[0])
            destino = self.formatarBloco(linha[1])
            retornoBloco = self.formatarEstados(linha[2])
            maquina.addBlocoTransicao(partida, retornoBloco, bloco, destino)
        return

    # Pega o arquivo que foi passado por linha de comando, o interpreta criando os blocos, estados, alfabeto e transições
    def AnalisadorArqEntrada(self, maquina):
        blocoAtual = ""

        try:
            with open(self.entradaArq) as file:
                for fileLinha in file:
                    # Pega os elementos da linha
                    linha = fileLinha.split()

                    # Ignora linha vazia ou comentario
                    if (len(linha) == 0) or (linha[0] == ';') or (linha[0][0] == ';'):
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
            print("\n\t(*) Erro ao abrir o arquivo.\n")

    """ 
        Função que recebe toda a linha digitada no terminal, e retorna um array com o modo de execucao,
        numero de steps e o delimitador, ou None se ocorrer algo errado no que foi digitado
    """
    def AnalisaEntradaConf(self):
        # Precisa de pelo menos o nome do programa e arquivo
        if len(self.data) < 2:
            aviso = "\n\t(*) Comando(s) nao reconhcido(s). Entrada incorreta."
            aviso += "\n(*) --help para mais informacoes sobre como realizar a entrada."

            print(aviso)
            return None

        # Verifica se o usuario pediu pelo help
        if(self.data[1] == "--help"):
            info = "A sintaxe deve ser: simturing.py <opcao> <arquivo>\n"
            info += "<arquivo> nome do arquivo, padrão (*.mt).\n<opcao> podem ser:\n"
            info += "\t• -resume (ou -r), executa o programa ate o fim em modo silencioso.\n"
            info += "\t• -verbose (ou -v), executa o programa ate o fim mostrando o resultado "
            info += "passo a passo da execucao.\n\t• -step <n> (ou -s <n>), mostra o resultado "
            info += "passo a passo de n computacoes.\n\t• -head <delimitadores> (ou -h <delimitadores>) "
            info += "para modificar os dois caracteres delimitadores esquerdo e direito."

            print(info)
            return None

        # Verifica existencia do arquivo
        self.entradaArq = self.data[len(self.data) - 1]
        filepath = Path(self.entradaArq)

        if filepath.is_file() == False:
            aviso = "\n\t(*) Arquivo nao encontrado. Arquivo de entrada invalido."
            aviso += "\n(*) Verifique se o arquivo encontra-se no diretorio informado ou"
            aviso += " se o nome do arquivo foi informado corretamente."

            print(aviso)
            return None

        """
            Se a entrada for valida no terminal, define uma lista de configuracao padrao de como o 
            simulador devera funcionar caso o usuario entre com apenas o nome do arquivo
        """
        configuracao = [MT.MODO_RESUME, MT.MAX_STEPS, MT.DELIMITADOR]

        # Verifica os argumentos
        achouCabecote = False
        achouPassos = False

        # Verifica as opcoes escolhidas pela entrada valida no terminal, altera as opcoes padroes
        if ((self.data[1] == "-resume") or (self.data[1] == "-r")):
            configuracao[0] = MT.MODO_RESUME
        elif((self.data[1] == "-verbose") or (self.data[1] == "-v")):
            configuracao[0] = MT.MODO_VERBOSE
        elif((self.data[1] == "-head") or (self.data[1] == "-h")):
            achouCabecote = True
        elif((self.data[1] == "-step") or (self.data[1] == "-s")):
            achouPassos = True

        # Conforme a entrada de cima, realiza a verificacao abaixo
        if(achouCabecote):
            # Verifica se foi realizada a entrada de dois simbolos, um para delimitar a esquerda e a direita
            delim = self.verifacaCabecote(self.data[2])

            if(delim == None):
                aviso = "\n\t(*) Os delimitadores "+ self.data[2] +" sao invalidos."

                print(aviso)
                return None

            configuracao[2] = delim
            achouCabecote = False
        elif(achouPassos):
            configuracao[2] = int(self.data[2])
            achouPassos = False
        return configuracao

    def verifacaCabecote(self, delimit):
        # Delimitador so pode ter dois caracteres
        if(len(delimit) != 2):
            return None

        return [delimit[0], delimit[1]]
    
    # Função que permite reconfigurar a maquina depois de executar a quantidade de passos definidos, ou somente continuar a execução
    def reconfigurar(self, iniConfig):
        aviso = "\n(*) Foi alcançado o limete de passo."
        aviso += "\n(*) Aperte enter para continuar ou configure a maquina para executar das formas seguinte."
        aviso += "\n\n\t• -v ou -verbose\n"
        aviso += "\n\t• -r ou -resume\n"
        aviso += "\n\t• -s # ou -step #\n"
        aviso += "\n\t• -h '[]' ou -head '[]'\n"
        print(aviso)
        
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
