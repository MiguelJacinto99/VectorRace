import math

from Carro import Carro
from Node import Node


class Graph:
    # Construtor da Classe
    def __init__(self, directed=True):
        self.nodes = []  # Lista de Nodos do Graph.
        self.partida = -1
        self.chegadas = []
        self.checkPoints = {}
        self.directed = directed  # Se o Graph é ou não Direcionado.
        self.graph = {}  # Dicionário Para Armazenar as Arestas (Não Pesadas)
        self.tamanhoCircuitoAtual = tuple()
        self.h = {}  # Dicionário Para Armazenar Heurísticas.

    def __str__(self):
        out = ""
        for key in self.graph.keys():
            out = out + "ID NODE: " + str(key) + ". ID DOS NODES ADJACENTES: "
            for value in self.graph[key]:
                out = out + str(value) + " "
            out = out + "\n"
        out = out + "ID NODO PARTIDA: " + str(self.partida) + "\n"
        out = out + "ID NODOS CHEGADA: "
        for i in self.chegadas:
            out = out + str(i) + " "
        out = out + "\n"
        out = out + "ID NODOS CHECKPOINT: " + "\n"
        for key in self.checkPoints.keys():
            out = out + "ID NODOS CHECKPOINT NÚMERO " + str(key) + ": "
            for value in self.checkPoints[key]:
                out = out + str(value) + " "
            out = out + "\n"
        out = out + "\n"
        return out

    def parse(self, file):
        x = 0
        y = 0
        contadorID = 0
        t = tuple()
        with open(file) as f:
            for line in f:
                y = 0
                for grid in line:
                    # Só Para Garantir um Parse Correto.
                    if grid != 'x' and grid != '-' and grid != 'P' and grid != 'F' and grid != 'I' and not (grid.isnumeric()):
                        continue
                    n = Node()
                    n.id = contadorID
                    n.linha = x
                    n.coluna = y
                    if grid == 'I':
                        n.type = 'x'
                    else:
                        n.type = grid
                    self.nodes.append(n)
                    if grid == 'P':
                        self.partida = n.id
                    if grid == 'F':
                        self.chegadas.append(n.id)
                    if grid.isnumeric():
                        # Verifica Se Já Foi Inicializada a Lista Correspondente a Essa Key (int(grid))
                        if int(grid) not in self.checkPoints.keys():
                            self.checkPoints[int(grid)] = []
                            self.checkPoints[int(grid)].append(n.id)
                        else:
                            self.checkPoints[int(grid)].append(n.id)
                    y = y + 1
                    contadorID = contadorID + 1
                x = x + 1
        # Ordena o Dicionário de CheckPoints Pela Key.
        self.checkPoints = {key: value for key, value in
                            sorted(self.checkPoints.items(), key=lambda item: int(item[0]))}
        t = (x - 1, y - 1)
        self.tamanhoCircuitoAtual = t
        return

    def drawPath(self, path=[], fileToRead="", fileToWrite=""):
        x = 0
        y = 0
        data = []
        with open(fileToRead, 'r') as originalFile:
            for line in originalFile:
                data.append(line)
        for linha, coluna, velocidadeLinha, velocidadeColuna in path:
            x = 0
            for line in data:
                if x == linha:
                    data[x] = self.replace_char_at_index(line, coluna, 'A')
                x = x + 1
        with open(fileToWrite, 'w+') as newFile:
            newFile.writelines(data)
        return

    def quadradosParaTravar(self, velocidade):
        resultado = 0
        while velocidade > 0:
            resultado = resultado + velocidade
            velocidade = velocidade - 1
        return resultado

    def limiteVelocidade(self, carro=Carro):
        novoCarro = Carro()
        linhaAtual = carro.linha
        colunaAtual = carro.coluna
        novoCarro.linha = carro.linha
        novoCarro.coluna = carro.coluna
        novoCarro.velocidadeLinha = carro.velocidadeLinha
        novoCarro.velocidadeColuna = carro.velocidadeColuna
        novoCarro.listaMovimentos = []
        movimentosPossiveis = self.movimentosPossiveis(carro)
        t = tuple()
        for idNode, velocidadeLinha, velocidadeColuna in movimentosPossiveis:
            directionLinha = self.nodes[idNode].linha - linhaAtual
            directionColuna = self.nodes[idNode].coluna - colunaAtual
            movimentoRacional = self.jogadaValida(linhaAtual, colunaAtual, velocidadeLinha,
                                                  velocidadeColuna, directionLinha, directionColuna)
            if movimentoRacional and self.nodes[idNode].type != 'x':
                t = idNode, velocidadeLinha, velocidadeColuna
                novoCarro.listaMovimentos.append(t)
        return novoCarro

    def jogadaValida(self, linha, coluna, velocidadeLinha, velocidadeColuna, directionLinhas, directionColunas):
        iterator = 0
        conditionLinha = False
        # Lista Dos Caracteres Seguinte Numa Determinada Direção.
        typeSeguinte = []
        t = tuple()
        if directionLinhas > 0 and directionColunas > 0:
            for idNode in self.nodes:
                if idNode.linha > linha and idNode.coluna == coluna:
                    # Precisamos de Guardar a Linha Para Ordenar.
                    t = (idNode.linha, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Linhas.
            typeSeguinte.sort()
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeLinha))
            for linhaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        conditionLinha = True
                    else:
                        return False
                else:
                    iterator = iterator + 1
            typeSeguinte = []
            iterator = 0
            for idNode in self.nodes:
                if idNode.linha == linha and idNode.coluna > coluna:
                    # Precisamos de Guardar a Coluna Para Ordenar.
                    t = (idNode.coluna, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Colunas.
            typeSeguinte.sort()
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeColuna))
            for colunaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        if conditionLinha:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas > 0 and directionColunas < 0:
            for idNode in self.nodes:
                if idNode.linha > linha and idNode.coluna == coluna:
                    # Precisamos de Guardar a Linha Para Ordenar.
                    t = (idNode.linha, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Linhas.
            typeSeguinte.sort()
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeLinha))
            for linhaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        conditionLinha = True
                    else:
                        return False
                else:
                    iterator = iterator + 1
            typeSeguinte = []
            iterator = 0
            for idNode in self.nodes:
                if idNode.linha == linha and idNode.coluna < coluna:
                    # Precisamos de Guardar a Coluna Para Ordenar.
                    t = (idNode.coluna, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Colunas.
            typeSeguinte.sort(reverse=True)
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeColuna))
            for colunaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        if conditionLinha:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas < 0 and directionColunas > 0:
            for idNode in self.nodes:
                if idNode.linha < linha and idNode.coluna == coluna:
                    # Precisamos de Guardar a Linha Para Ordenar.
                    t = (idNode.linha, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Linhas.
            typeSeguinte.sort(reverse=True)
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeLinha))
            for linhaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        conditionLinha = True
                    else:
                        return False
                else:
                    iterator = iterator + 1
            typeSeguinte = []
            iterator = 0
            for idNode in self.nodes:
                if idNode.linha == linha and idNode.coluna > coluna:
                    # Precisamos de Guardar a Coluna Para Ordenar.
                    t = (idNode.coluna, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Colunas.
            typeSeguinte.sort()
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeColuna))
            for colunaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        if conditionLinha:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas < 0 and directionColunas < 0:
            for idNode in self.nodes:
                if idNode.linha < linha and idNode.coluna == coluna:
                    # Precisamos de Guardar a Linha Para Ordenar.
                    t = (idNode.linha, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Linhas.
            typeSeguinte.sort(reverse=True)
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeLinha))
            for linhaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        conditionLinha = True
                    else:
                        return False
                else:
                    iterator = iterator + 1
            typeSeguinte = []
            iterator = 0
            for idNode in self.nodes:
                if idNode.linha == linha and idNode.coluna < coluna:
                    # Precisamos de Guardar a Coluna Para Ordenar.
                    t = (idNode.coluna, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Colunas.
            typeSeguinte.sort(reverse=True)
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeColuna))
            for colunaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        if conditionLinha:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas > 0 and directionColunas == 0:
            for idNode in self.nodes:
                if idNode.linha > linha and idNode.coluna == coluna:
                    # Precisamos de Guardar a Linha Para Ordenar.
                    t = (idNode.linha, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Linhas.
            typeSeguinte.sort()
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeLinha))
            for linhaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        return True
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas < 0 and directionColunas == 0:
            for idNode in self.nodes:
                if idNode.linha < linha and idNode.coluna == coluna:
                    # Precisamos de Guardar a Linha Para Ordenar.
                    t = (idNode.linha, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Linhas.
            typeSeguinte.sort(reverse=True)
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeLinha))
            for linhaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        return True
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas == 0 and directionColunas > 0:
            for idNode in self.nodes:
                if idNode.linha == linha and idNode.coluna > coluna:
                    # Precisamos de Guardar a Coluna Para Ordenar.
                    t = (idNode.coluna, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Colunas.
            typeSeguinte.sort()
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeColuna))
            for colunaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        return True
                    else:
                        return False
                else:
                    iterator = iterator + 1
        # --------------------------------------------------------------------------
        if directionLinhas == 0 and directionColunas < 0:
            for idNode in self.nodes:
                if idNode.linha == linha and idNode.coluna < coluna:
                    # Precisamos de Guardar a Coluna Para Ordenar.
                    t = (idNode.coluna, idNode.type)
                    typeSeguinte.append(t)
            # Ordenar a Lista de Tuplos Pelo Primeiro Item. Neste Caso, Pelas Colunas.
            typeSeguinte.sort(reverse=True)
            velocidadeLimite = self.quadradosParaTravar(abs(velocidadeColuna))
            for colunaCandidata, typeCandidato in typeSeguinte:
                if typeCandidato == 'x':
                    if iterator >= velocidadeLimite:
                        return True
                    else:
                        return False
                else:
                    iterator = iterator + 1
        else:
            return True

    def heuristicaCheckPoint(self):
        contadorCheckPoint = 1
        numeroCheckPoint = len(self.checkPoints)
        listaFinais = self.chegadas
        for idNode in self.nodes:
            linhaOrigem = idNode.linha
            colunaOrigem = idNode.coluna
            while contadorCheckPoint <= numeroCheckPoint:
                # Utilizamos a Distância ao Primeiro CheckPoint Dessa Lista de CheckPoints
                listaCheckPoint = self.checkPoints[contadorCheckPoint].copy()
                linhaDestino = self.nodes[listaCheckPoint[0]].linha
                colunaDestino = self.nodes[listaCheckPoint[0]].coluna
                distReal = math.sqrt((math.pow(linhaDestino - linhaOrigem, 2)) +
                                     (math.pow(colunaDestino - colunaOrigem, 2)))
                self.nodes[idNode.id].h1.append(distReal)
                contadorCheckPoint = contadorCheckPoint + 1
            contadorCheckPoint = 1
            # Da Mesma Forma Utilizamos a Distância à Primeira Chegada Dessa Lista de Chegadas
            linhaDestino = self.nodes[listaFinais[0]].linha
            colunaDestino = self.nodes[listaFinais[0]].coluna
            distReal = math.sqrt((math.pow(linhaDestino - linhaOrigem, 2)) +
                                 (math.pow(colunaDestino - colunaOrigem, 2)))
            self.nodes[idNode.id].h1.append(distReal)
        return

    def criaGrafo(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for node in self.nodes:
            self.graph[node.id] = set()
            linha = node.linha
            coluna = node.coluna
            for x, y in directions:
                linhaBase = linha + x
                colunaBase = coluna + y
                for nodeCandidato in self.nodes:
                    if nodeCandidato.type != 'x':
                        linhaCandidata = nodeCandidato.linha
                        colunaCandidata = nodeCandidato.coluna
                        if linhaBase == linhaCandidata and colunaBase == colunaCandidata:
                            self.graph[node.id].add(nodeCandidato.id)
        return

    def movimentosPossiveis(self, carro=Carro):
        tamanhoCircuitoLinhas, tamanhoCircuitoColunas = self.tamanhoCircuitoAtual
        movimentosPossiveis = []
        t = tuple()
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in directions:
            novaVelocidadeLinha = carro.velocidadeLinha + x
            novaVelocidadeColuna = carro.velocidadeColuna + y
            novaLinha = carro.linha + novaVelocidadeLinha
            novaColuna = carro.coluna + novaVelocidadeColuna
            if 0 <= novaLinha <= tamanhoCircuitoLinhas and 0 <= novaColuna <= tamanhoCircuitoColunas:
                for node in self.nodes:
                    if novaLinha == node.linha and novaColuna == node.coluna:
                        t = (node.id, novaVelocidadeLinha, novaVelocidadeColuna)
                        movimentosPossiveis.append(t)
        # Devolve Uma Lista Com o Seguinte Formato:
        # (idNode, velocidadeNaLinha, velocidadeNaColuna)
        # Todos os idNode Existem
        return movimentosPossiveis

    def limiteSeguro(self, carro=Carro):
        novoCarro = Carro()
        linhaAtual = carro.linha
        colunaAtual = carro.coluna
        novoCarro.linha = carro.linha
        novoCarro.coluna = carro.coluna
        novoCarro.velocidadeLinha = carro.velocidadeLinha
        novoCarro.velocidadeColuna = carro.velocidadeColuna
        novoCarro.listaMovimentos = []
        movimentosSeguros = self.movimentosSeguros(carro)
        t = tuple()
        for idNode, velocidadeLinha, velocidadeColuna in movimentosSeguros:
            directionLinha = self.nodes[idNode].linha - linhaAtual
            directionColuna = self.nodes[idNode].coluna - colunaAtual
            movimentoRacional = self.jogadaValida(linhaAtual, colunaAtual, velocidadeLinha,
                                                  velocidadeColuna, directionLinha, directionColuna)
            if movimentoRacional and self.nodes[idNode].type != 'x':
                t = idNode, velocidadeLinha, velocidadeColuna
                novoCarro.listaMovimentos.append(t)
        return novoCarro

    def movimentosSeguros(self, carro=Carro):
        tamanhoCircuitoLinhas, tamanhoCircuitoColunas = self.tamanhoCircuitoAtual
        movimentosSeguros = []
        t = tuple()
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in directions:
            novaVelocidadeLinha = carro.velocidadeLinha + x
            novaVelocidadeColuna = carro.velocidadeColuna + y
            novaLinha = carro.linha + novaVelocidadeLinha
            novaColuna = carro.coluna + novaVelocidadeColuna
            if (abs(novaVelocidadeLinha) <= 3) and (abs(novaVelocidadeColuna) <= 3):
                if 0 <= novaLinha <= tamanhoCircuitoLinhas and 0 <= novaColuna <= tamanhoCircuitoColunas:
                    for node in self.nodes:
                        if novaLinha == node.linha and novaColuna == node.coluna:
                            t = (node.id, novaVelocidadeLinha, novaVelocidadeColuna)
                            movimentosSeguros.append(t)
        # Devolve Uma Lista Com o Seguinte Formato:
        # (idNode, velocidadeNaLinha, velocidadeNaColuna)
        # Todos os idNode Existem
        return movimentosSeguros

    def procura_DFS(self, start=int, checkPointsCruzados=int, end=[], path=[], visited=set()):
        totalCheckPoints = len(self.checkPoints)
        path.append(start)
        visited.add(start)
        if checkPointsCruzados > totalCheckPoints:
            for final in end:
                if start == final:
                    print("CIRCUITO TERMINADO NO NODO " + str(start) + "!")
                    return path
        if checkPointsCruzados <= totalCheckPoints:
            for checkPoint in self.checkPoints[checkPointsCruzados]:
                if start == checkPoint:
                    print("O CHECKPOINT NÚMERO " + str(checkPointsCruzados) + " FOI CRUZADO NO NODO "
                          + str(start) + "!")
                    checkPointsCruzados = checkPointsCruzados + 1
                    # Essencial!
                    visited.clear()
        for adjacent in self.graph[start]:
            if adjacent not in visited:
                resultado = self.procura_DFS(adjacent, checkPointsCruzados, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()
        return None

    def procura_BFS(self, start=int, end=[], queue=[], visited=set()):
        checkPointsCruzados = 1
        totalCheckPoints = len(self.checkPoints)
        path = []
        parents = {start: start}
        queue.append(start)
        visited.add(start)
        while queue:
            primeiroDaFila = queue.pop(0)
            path.append(primeiroDaFila)
            if checkPointsCruzados > totalCheckPoints:
                for final in end:
                    if primeiroDaFila == final:
                        print("CIRCUITO TERMINADO NO NODO " + str(primeiroDaFila) + "!")
                        return path
            if checkPointsCruzados <= totalCheckPoints:
                for checkPoint in self.checkPoints[checkPointsCruzados]:
                    if primeiroDaFila == checkPoint:
                        print("O CHECKPOINT NÚMERO " + str(checkPointsCruzados) + " FOI CRUZADO NO NODO "
                              + str(primeiroDaFila) + "!")
                        checkPointsCruzados = checkPointsCruzados + 1
                        # Essencial!
                        visited.clear()
            for adjacent in self.graph[primeiroDaFila]:
                if adjacent not in visited:
                    parents[adjacent] = primeiroDaFila
                    queue.append(adjacent)
                    visited.add(adjacent)
        return None

    def criaTuple(self, path=[]):
        i = 1
        t = tuple()
        linha = self.nodes[path[0]].linha
        coluna = self.nodes[path[0]].coluna
        velocidadeLinha = 0
        velocidadeColuna = 0
        t = linha, coluna, velocidadeLinha, velocidadeColuna
        novoPath = [t]
        while i < len(path):
            linha = self.nodes[path[i]].linha
            coluna = self.nodes[path[i]].coluna
            velocidadeLinha = self.nodes[path[i]].linha - self.nodes[path[i - 1]].linha
            velocidadeColuna = self.nodes[path[i]].coluna - self.nodes[path[i - 1]].coluna
            t = linha, coluna, velocidadeLinha, velocidadeColuna
            novoPath.append(t)
            i = i + 1
        return novoPath

    def cruzouNodesImportantes(self, linhaOrigem, colunaOrigem, linhaDestino, colunaDestino, ID=int):
        listaFinais = []
        listaCheckPoint = []
        t = tuple()
        if ID == -1:
            for final in self.chegadas:
                linhaFinal = self.nodes[final].linha
                colunaFinal = self.nodes[final].coluna
                t = (linhaFinal, colunaFinal)
                listaFinais.append(t)
            for linhaFinal, colunaFinal in listaFinais:
                if linhaOrigem > linhaDestino and colunaOrigem > colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator >= linhaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            linhaIterator = linhaIterator - 1
                    linhaIterator = linhaOrigem
                    while colunaIterator >= colunaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            colunaIterator = colunaIterator - 1
                if linhaOrigem > linhaDestino and colunaOrigem < colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator >= linhaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            linhaIterator = linhaIterator - 1
                    linhaIterator = linhaOrigem
                    while colunaIterator <= colunaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            colunaIterator = colunaIterator + 1
                if linhaOrigem < linhaDestino and colunaOrigem > colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator <= linhaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            linhaIterator = linhaIterator + 1
                    linhaIterator = linhaOrigem
                    while colunaIterator >= colunaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            colunaIterator = colunaIterator - 1
                if linhaOrigem < linhaDestino and colunaOrigem < colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator <= linhaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            linhaIterator = linhaIterator + 1
                    linhaIterator = linhaOrigem
                    while colunaIterator <= colunaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            colunaIterator = colunaIterator + 1
                if linhaOrigem > linhaDestino and colunaOrigem == colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator >= linhaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            linhaIterator = linhaIterator - 1
                if linhaOrigem < linhaDestino and colunaOrigem == colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator <= linhaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            linhaIterator = linhaIterator + 1
                if linhaOrigem == linhaDestino and colunaOrigem > colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while colunaIterator >= colunaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            colunaIterator = colunaIterator - 1
                if linhaOrigem == linhaDestino and colunaOrigem < colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while colunaIterator <= colunaDestino:
                        if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                            return True
                        else:
                            colunaIterator = colunaIterator + 1
        else:
            checkPoints = self.checkPoints[int(ID)]
            for idCheckPoint in checkPoints:
                linhaFinal = self.nodes[idCheckPoint].linha
                colunaFinal = self.nodes[idCheckPoint].coluna
                t = (linhaFinal, colunaFinal)
                listaCheckPoint.append(t)
            for linhaCheckPoint, colunaCheckPoint in listaCheckPoint:
                if linhaOrigem > linhaDestino and colunaOrigem > colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator >= linhaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            linhaIterator = linhaIterator - 1
                    linhaIterator = linhaOrigem
                    while colunaIterator >= colunaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            colunaIterator = colunaIterator - 1
                if linhaOrigem > linhaDestino and colunaOrigem < colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator >= linhaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            linhaIterator = linhaIterator - 1
                    linhaIterator = linhaOrigem
                    while colunaIterator <= colunaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            colunaIterator = colunaIterator + 1
                if linhaOrigem < linhaDestino and colunaOrigem > colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator <= linhaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            linhaIterator = linhaIterator + 1
                    linhaIterator = linhaOrigem
                    while colunaIterator >= colunaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            colunaIterator = colunaIterator - 1
                if linhaOrigem < linhaDestino and colunaOrigem < colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator <= linhaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            linhaIterator = linhaIterator + 1
                    linhaIterator = linhaOrigem
                    while colunaIterator <= colunaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            colunaIterator = colunaIterator + 1
                if linhaOrigem > linhaDestino and colunaOrigem == colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator >= linhaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            linhaIterator = linhaIterator - 1
                if linhaOrigem < linhaDestino and colunaOrigem == colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while linhaIterator <= linhaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            linhaIterator = linhaIterator + 1
                if linhaOrigem == linhaDestino and colunaOrigem > colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while colunaIterator >= colunaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            colunaIterator = colunaIterator - 1
                if linhaOrigem == linhaDestino and colunaOrigem < colunaDestino:
                    linhaIterator = linhaOrigem
                    colunaIterator = colunaOrigem
                    while colunaIterator <= colunaDestino:
                        if linhaIterator == linhaCheckPoint and colunaIterator == colunaCheckPoint:
                            return True
                        else:
                            colunaIterator = colunaIterator + 1

    def cruzouCruzes(self, linhaOrigem, colunaOrigem, linhaDestino, colunaDestino):
        listaFinais = []
        listaCruzes = self.colecionaCruzes()
        for idNode in listaCruzes:
            linhaFinal = self.nodes[idNode].linha
            colunaFinal = self.nodes[idNode].coluna
            t = (linhaFinal, colunaFinal)
            listaFinais.append(t)
        for linhaFinal, colunaFinal in listaFinais:
            if linhaOrigem > linhaDestino and colunaOrigem > colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while linhaIterator >= linhaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        linhaIterator = linhaIterator - 1
                linhaIterator = linhaOrigem
                while colunaIterator >= colunaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        colunaIterator = colunaIterator - 1
            if linhaOrigem > linhaDestino and colunaOrigem < colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while linhaIterator >= linhaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        linhaIterator = linhaIterator - 1
                linhaIterator = linhaOrigem
                while colunaIterator <= colunaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        colunaIterator = colunaIterator + 1
            if linhaOrigem < linhaDestino and colunaOrigem > colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while linhaIterator <= linhaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        linhaIterator = linhaIterator + 1
                linhaIterator = linhaOrigem
                while colunaIterator >= colunaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        colunaIterator = colunaIterator - 1
            if linhaOrigem < linhaDestino and colunaOrigem < colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while linhaIterator <= linhaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        linhaIterator = linhaIterator + 1
                linhaIterator = linhaOrigem
                while colunaIterator <= colunaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        colunaIterator = colunaIterator + 1
            if linhaOrigem > linhaDestino and colunaOrigem == colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while linhaIterator >= linhaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        linhaIterator = linhaIterator - 1
            if linhaOrigem < linhaDestino and colunaOrigem == colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while linhaIterator <= linhaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        linhaIterator = linhaIterator + 1
            if linhaOrigem == linhaDestino and colunaOrigem > colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while colunaIterator >= colunaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        colunaIterator = colunaIterator - 1
            if linhaOrigem == linhaDestino and colunaOrigem < colunaDestino:
                linhaIterator = linhaOrigem
                colunaIterator = colunaOrigem
                while colunaIterator <= colunaDestino:
                    if linhaIterator == linhaFinal and colunaIterator == colunaFinal:
                        return True
                    else:
                        colunaIterator = colunaIterator + 1

    def colecionaCruzes(self):
        cruzes = []
        for node in self.nodes:
            if node.type == 'x':
                cruzes.append(node.id)
        return cruzes

    def aestrela(self):
        checkPointsCruzados = 1
        totalCheckPoints = len(self.checkPoints)
        listaDistCheckPoint = []
        carro = Carro()
        carro.linha = self.nodes[self.partida].linha
        carro.coluna = self.nodes[self.partida].coluna
        carro.velocidadeLinha = 0
        carro.velocidadeColuna = 0
        t = tuple()
        t = self.nodes[self.partida].linha, self.nodes[self.partida].coluna, 0, 0
        outroT = tuple()
        parents = {t: t}
        path = [t]
        visited = set()
        visited.add(self.partida)
        existeCaminho = True
        while checkPointsCruzados <= totalCheckPoints:
            linhaAtual = carro.linha
            colunaAtual = carro.coluna
            velocidadeLinhaAtual = carro.velocidadeLinha
            velocidadeColunaAtual = carro.velocidadeColuna
            carro = self.limiteVelocidade(carro)
            listaDistCheckPoint = []
            t = ()
            for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                if idNode not in visited:
                    listaDistCheckPoint.append(t)
            if len(listaDistCheckPoint) == 0:
                for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                    t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                    if idNode in visited:
                        visited.remove(idNode)
                        listaDistCheckPoint.append(t)
                    else:
                        listaDistCheckPoint.append(t)
            listaDistCheckPoint.sort()
            distH, idNode, velocidadeLinhaTemp, velocidadeColunaTemp = listaDistCheckPoint[0]
            visited.add(idNode)
            carro.linha = self.nodes[idNode].linha
            carro.coluna = self.nodes[idNode].coluna
            carro.velocidadeLinha = velocidadeLinhaTemp
            carro.velocidadeColuna = velocidadeColunaTemp
            carro.listaMovimentos = []
            t = ()
            t = linhaAtual, colunaAtual, velocidadeLinhaAtual, velocidadeColunaAtual
            outroT = carro.linha, carro.coluna, carro.velocidadeLinha, carro.velocidadeColuna
            parents[outroT] = t
            path.append(outroT)
            if self.cruzouNodesImportantes(linhaAtual, colunaAtual, carro.linha, carro.coluna, checkPointsCruzados):
                checkPointsCruzados = checkPointsCruzados + 1
                visited.clear()
                print("O CHECKPOINT NÚMERO " + str((checkPointsCruzados) - 1) + " FOI CRUZADO NO NODO "
                                              + str(idNode) + "!")
        # Os CheckPoints Foram Todos Cruzados. Pode Finalizar.
        while existeCaminho:
            linhaAtual = carro.linha
            colunaAtual = carro.coluna
            velocidadeLinhaAtual = carro.velocidadeLinha
            velocidadeColunaAtual = carro.velocidadeColuna
            carro = self.limiteVelocidade(carro)
            listaDistCheckPoint = []
            t = ()
            for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                if idNode not in visited:
                    listaDistCheckPoint.append(t)
            if len(listaDistCheckPoint) == 0:
                for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                    t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                    if idNode in visited:
                        visited.remove(idNode)
                        listaDistCheckPoint.append(t)
                    else:
                        listaDistCheckPoint.append(t)
            listaDistCheckPoint.sort()
            distH, idNode, velocidadeLinhaTemp, velocidadeColunaTemp = listaDistCheckPoint[0]
            visited.add(idNode)
            carro.linha = self.nodes[idNode].linha
            carro.coluna = self.nodes[idNode].coluna
            carro.velocidadeLinha = velocidadeLinhaTemp
            carro.velocidadeColuna = velocidadeColunaTemp
            t = ()
            t = linhaAtual, colunaAtual, velocidadeLinhaAtual, velocidadeColunaAtual
            outroT = carro.linha, carro.coluna, carro.velocidadeLinha, carro.velocidadeColuna
            parents[outroT] = t
            path.append(outroT)
            if self.cruzouNodesImportantes(linhaAtual, colunaAtual, carro.linha, carro.coluna, -1):
                print("CIRCUITO TERMINADO NO NODO " + str(idNode) + "!")
                return path
        return None

    def seguro(self):
        checkPointsCruzados = 1
        totalCheckPoints = len(self.checkPoints)
        listaDistCheckPoint = []
        carro = Carro()
        carro.linha = self.nodes[self.partida].linha
        carro.coluna = self.nodes[self.partida].coluna
        carro.velocidadeLinha = 0
        carro.velocidadeColuna = 0
        t = tuple()
        t = self.nodes[self.partida].linha, self.nodes[self.partida].coluna, 0, 0
        outroT = tuple()
        parents = {t: t}
        path = [t]
        visited = set()
        visited.add(self.partida)
        existeCaminho = True
        while checkPointsCruzados <= totalCheckPoints:
            linhaAtual = carro.linha
            colunaAtual = carro.coluna
            velocidadeLinhaAtual = carro.velocidadeLinha
            velocidadeColunaAtual = carro.velocidadeColuna
            carro = self.limiteSeguro(carro)
            listaDistCheckPoint = []
            t = ()
            for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                if idNode not in visited:
                    listaDistCheckPoint.append(t)
            if len(listaDistCheckPoint) == 0:
                for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                    t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                    if idNode in visited:
                        visited.remove(idNode)
                        listaDistCheckPoint.append(t)
                    else:
                        listaDistCheckPoint.append(t)
            listaDistCheckPoint.sort()
            distH, idNode, velocidadeLinhaTemp, velocidadeColunaTemp = listaDistCheckPoint[0]
            visited.add(idNode)
            carro.linha = self.nodes[idNode].linha
            carro.coluna = self.nodes[idNode].coluna
            carro.velocidadeLinha = velocidadeLinhaTemp
            carro.velocidadeColuna = velocidadeColunaTemp
            carro.listaMovimentos = []
            t = ()
            t = linhaAtual, colunaAtual, velocidadeLinhaAtual, velocidadeColunaAtual
            outroT = carro.linha, carro.coluna, carro.velocidadeLinha, carro.velocidadeColuna
            parents[outroT] = t
            path.append(outroT)
            if self.cruzouNodesImportantes(linhaAtual, colunaAtual, carro.linha, carro.coluna, checkPointsCruzados):
                checkPointsCruzados = checkPointsCruzados + 1
                visited.clear()
                print("O CHECKPOINT NÚMERO " + str((checkPointsCruzados) - 1) + " FOI CRUZADO NO NODO "
                      + str(idNode) + "!")
        # Os CheckPoints Foram Todos Cruzados. Pode Finalizar.
        while existeCaminho:
            linhaAtual = carro.linha
            colunaAtual = carro.coluna
            velocidadeLinhaAtual = carro.velocidadeLinha
            velocidadeColunaAtual = carro.velocidadeColuna
            carro = self.limiteSeguro(carro)
            listaDistCheckPoint = []
            t = ()
            for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                if idNode not in visited:
                    listaDistCheckPoint.append(t)
            if len(listaDistCheckPoint) == 0:
                for idNode, velocidadeLinha, velocidadeColuna in carro.listaMovimentos:
                    t = self.nodes[idNode].h1[checkPointsCruzados - 1], idNode, velocidadeLinha, velocidadeColuna
                    if idNode in visited:
                        visited.remove(idNode)
                        listaDistCheckPoint.append(t)
                    else:
                        listaDistCheckPoint.append(t)
            listaDistCheckPoint.sort()
            distH, idNode, velocidadeLinhaTemp, velocidadeColunaTemp = listaDistCheckPoint[0]
            visited.add(idNode)
            carro.linha = self.nodes[idNode].linha
            carro.coluna = self.nodes[idNode].coluna
            carro.velocidadeLinha = velocidadeLinhaTemp
            carro.velocidadeColuna = velocidadeColunaTemp
            t = ()
            t = linhaAtual, colunaAtual, velocidadeLinhaAtual, velocidadeColunaAtual
            outroT = carro.linha, carro.coluna, carro.velocidadeLinha, carro.velocidadeColuna
            parents[outroT] = t
            path.append(outroT)
            if self.cruzouNodesImportantes(linhaAtual, colunaAtual, carro.linha, carro.coluna, -1):
                print("CIRCUITO TERMINADO NO NODO " + str(idNode) + "!")
                return path
        return None

    def replace_char_at_index(self, org_str, index, replacement):
        new_str = org_str
        if index < len(org_str):
            new_str = org_str[0:index] + replacement + org_str[index + 1:]
        return new_str
