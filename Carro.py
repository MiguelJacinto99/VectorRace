class Carro:
    linha = int
    coluna = int
    velocidadeLinha = int
    velocidadeColuna = int
    # Lista de ID NODES Disponíveis Tendo em Conta os Atributos Anteriores e o Circuito.
    listaMovimentos = []

    def __init__(self):
        self.linha = 0
        self.coluna = 0
        self.velocidadeLinha = 0
        self.velocidadeColuna = 0
        self.listaMovimentos = []
