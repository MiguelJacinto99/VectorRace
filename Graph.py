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

    def parse(self):
        x = 0
        y = 0
        contadorID = 0
        with open("reta.txt") as f:
            for line in f:
                y = 0
                for grid in line:
                    # Só Para Garantir um Parse Correto.
                    if grid != 'x' and grid != '-' and grid != 'P' and grid != 'F' and not (grid.isnumeric()):
                        continue
                    n = Node()
                    n.id = contadorID
                    n.linha = x
                    n.coluna = y
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
        return

    def criaGrafo(self):
        linha = 0
        coluna = 0
        linhaBase = 0
        colunaBase = 0
        linhaCandidata = 0
        colunaCandidata = 0
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

    def procura_DFS(self, start=int, checkPointsCruzados=int, end=[], path=[], visited=set()):
        totalCheckPoints = len(self.checkPoints)
        path.append(start)
        visited.add(start)
        if checkPointsCruzados > totalCheckPoints:
            for final in end:
                if start == final:
                    print("Circuito Terminado No Nodo " + str(start) + "!")
                    return path
        if checkPointsCruzados <= totalCheckPoints:
            for checkPoint in self.checkPoints[checkPointsCruzados]:
                if start == checkPoint:
                    print("O CheckPoint Número " + str(checkPointsCruzados) + " Foi Cruzado no Nodo "
                          + str(start))
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
        queue.append(start)
        visited.add(start)
        while queue:
            primeiroDaFila = queue.pop(0)
            path.append(primeiroDaFila)
            if checkPointsCruzados > totalCheckPoints:
                for final in end:
                    if primeiroDaFila == final:
                        print("Circuito Terminado No Nodo " + str(primeiroDaFila) + "!")
                        return path
            if checkPointsCruzados <= totalCheckPoints:
                for checkPoint in self.checkPoints[checkPointsCruzados]:
                    if primeiroDaFila == checkPoint:
                        print("O CheckPoint Número " + str(checkPointsCruzados) + " Foi Cruzado no Nodo "
                              + str(primeiroDaFila))
                        checkPointsCruzados = checkPointsCruzados + 1
                        # Essencial!
                        visited.clear()
            for adjacent in self.graph[primeiroDaFila]:
                if adjacent not in visited:
                    visited.add(adjacent)
                    queue.append(adjacent)

        return None
