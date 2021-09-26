import numpy as np
from random import *


class Tabuleiro:
    """
    Classe que representa o estado do jogo.
    """

    # -------------------------------------------------
    def __init__(self):
        """
        Construtor. Initializa o tabuleiro 3x3 vazio.
        """
        self.board = [[''] * 3 for n in range(3)]

    # -------------------------------------------------
    def save(self):
        """
        Salva os dados do tabuleiro para uma string.

        Gera uma string com as peças do tabuleiro separadas por
        ponto-e-vírgula (';'), de forma que o estado do jogo possa
        ser comunicado via socket.

        Retorno
        ----------
        data: str
            String de texto com os dados do tabuleiro separados por
            ponto-e-vírgula (';'), prontos para serem comunicados.     
        """
        return ';'.join([';'.join(x) for x in self.board])

    # -------------------------------------------------
    def restore(self, data):
        """
        Restaura os dados do tabuleiro a partir de uma string.

        Lê uma string com as peças do tabuleiro separadas por
        ponto-e-vírgula (';'), de forma que o estado do jogo possa ser
        comunicado via socket.

        Parâmetros
        ----------
        data: str
            String de texto com os dados do tabuleiro separados por um
            ponto-e-vírgula (';'), prontos para serem atualizados neste
            objeto.
        """
        self.board = np.reshape(data.split(';'), (3, 3)).tolist()

    # -------------------------------------------------
    def print(self):
        """
        Imprime o tabuleiro em um formato visual.
        """
        print("+---+---+---+")
        for row in self.board:
            print('|{}|{}|{}|'.format(row[0].center(
                3, ' '), row[1].center(3, ' '), row[2].center(3, ' ')))
            print("+---+---+---+")

    # -------------------------------------------------
    def finish(self):
        # checando linhas
        for i in range(3):
            if self.board[i][0] == 'x' and self.board[i][1] == 'x' and self.board[i][2] == 'x':
                return 1
            if self.board[i][0] == 'o' and self.board[i][1] == 'o' and self.board[i][2] == 'o':
                return 2

        # checando colunas
        for i in range(3):
            if self.board[0][i] == 'x' and self.board[1][i] == 'x' and self.board[2][i] == 'x':
                return 1
            if self.board[0][i] == 'o' and self.board[1][i] == 'o' and self.board[2][i] == 'o':
                return 2

        # checando diagonais
        if self.board[0][0] == 'x' and self.board[1][1] == 'x' and self.board[2][2] == 'x':
            return 1
        if self.board[0][2] == 'x' and self.board[1][1] == 'x' and self.board[2][0] == 'x':
            return 1
        if self.board[0][0] == 'o' and self.board[1][1] == 'o' and self.board[2][2] == 'o':
            return 2
        if self.board[0][2] == 'o' and self.board[1][1] == 'o' and self.board[2][0] == 'o':
            return 2

        soma = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'o' or self.board[i][j] == 'x':
                    soma = soma + 1
        if soma == 9:
            return 9
        else:
            return 0

    # -------------------------------------------------
    def move(self, row, col, piece):
        """
        Faz uma jogada no tabuleiro, nas posições dadas.

        Parâmetros
        ----------
        row: int
            Número da linha no tabuleiro, no intervalo [0,2].
        col: int
            Número da coluna no tabuleiro, no intervalo [0,2].
        piece: str
            Letra com o símbolo jogado, entre as opções 'o' e 'x'.        
        """

        # Valida os parâmetros de entrada
        if row < 0 or row > 2:
            raise RuntimeError('Número de linha inválido: {}'.format(row))
        if col < 0 or col > 2:
            raise RuntimeError('Número de coluna inválido: {}'.format(col))
        piece = piece.lower()
        if piece != 'x' and piece != 'o':
            raise RuntimeError('Peça inválida: {}'.format(piece))

        # Verifica se a posição jogada está vazia
        if self.board[row][col] != '':
            raise RuntimeError(
                'Posição do tabuleiro já preenchida: {}x{}'.format(row, col))

        # Faz a jogada
        self.board[row][col] = piece

    # -------------------------------------------------
    def moveRandom(self, piece):
        """
        Faz uma jogada aleatória no tabuleiro, em uma das posições vazias.

        Parâmetros
        ----------
        piece: str
            Letra com o símbolo jogado, entre as opções 'o' e 'x'.
        """

        # Cria uma lista com as posições vazias
        options = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    options.append((row, col))

        # Faz uma permutação aleatória nessa lista
        shuffle(options)

        # Faz a jogada na primeira posição da lista
        if len(options) > 0:
            row = options[0][0]
            col = options[0][1]
            self.move(row, col, piece)
