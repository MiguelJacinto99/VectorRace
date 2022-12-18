from Grid import Grid


class Node:
    id = int
    linha = int
    coluna = int
    type = Grid
    h1 = []

    def __init__(self):
        self.id = -1
        self.linha = 0
        self.coluna = 0
        self.type = None
        self.h1 = []

    def __str__(self):
        out = "Node: ID: " + str(self.id) + " Com Coordenadas: -> (" + str(self.linha) \
              + "," + str(self.coluna) + ') e Tipo: ' + str(self.type)
        return out

