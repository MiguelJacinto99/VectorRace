import time

from Carro import Carro
from Graph import Graph

g = Graph()
c = Carro()

g.parse()
g.criaGrafo()
print(g)
print("Circuito Criado!")
print()

# Algoritmo DFS
print("Algoritmo DFS:")
print()
begin = time.time()
caminhoDFS = g.procura_DFS(g.partida, 1, g.chegadas, path=[], visited=set())
end = time.time()
print("O Caminho Encontrado é Constituído Por " + str(len(caminhoDFS)) + " Nodos!")
print("Caminho: " + str(caminhoDFS))
print("O Algoritmo DFS Demorou Cerca de " + str(end - begin) + " Segundos!")
print()

# Algoritmo BFS
print("Algoritmo BFS:")
print()
begin = time.time()
caminhoBFS = g.procura_BFS(g.partida, g.chegadas, queue=[], visited=set())
end = time.time()
print("O Caminho Encontrado é Constituído Por " + str(len(caminhoBFS)) + " Nodos!")
print("Caminho: " + str(caminhoBFS))
print("O Algoritmo BFS Demorou Cerca de " + str(end - begin) + " Segundos!")

