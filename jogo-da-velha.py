# Baseado em: https://www.pythonprogressivo.net/2018/10/Como-Criar-Jogo-Velha-Python.html

def exibe(tabuleiro):
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0:
                print(" _ ", end=' ')
            elif tabuleiro[i][j] == 1:
                print(" X ", end=' ')
            elif tabuleiro[i][j] == -1:
                print(" O ", end=' ')

        print()


def ganhou(tabuleiro):
    # checando linhas
    for i in range(3):
        soma = tabuleiro[i][0] + tabuleiro[i][1] + tabuleiro[i][2]
        if soma == 3 or soma == -3:
            return 1

     # checando colunas
    for i in range(3):
        soma = tabuleiro[0][i] + tabuleiro[1][i] + tabuleiro[2][i]
        if soma == 3 or soma == -3:
            return 1

    # checando diagonais
    diagonal1 = tabuleiro[0][0] + tabuleiro[1][1] + tabuleiro[2][2]
    diagonal2 = tabuleiro[0][2] + tabuleiro[1][1] + tabuleiro[2][0]
    if diagonal1 == 3 or diagonal1 == -3 or diagonal2 == 3 or diagonal2 == -3:
        return 1

    return 0


def jogo():
    """
    tabuleiro = [ [0,0,0],
                  [0,0,0],
                  [0,0,0] ]
    """
    tabuleiro = [[0 for i in range(3)] for j in range(3)]
    jogada = 0

    while ganhou(tabuleiro) == 0:
        print("\nJogador ", jogada % 2 + 1)
        exibe(tabuleiro)
        linha = int(input("\nLinha :"))
        coluna = int(input("Coluna:"))

        if tabuleiro[linha - 1][coluna - 1] == 0:
            if(jogada % 2 + 1) == 1:
                tabuleiro[linha - 1][coluna - 1] = 1
            else:
                tabuleiro[linha - 1][coluna - 1] = -1
        else:
            print("Nao esta vazio")
            jogada -= 1

        if ganhou(tabuleiro):
            print("Jogador ", jogada %
                  2 + 1, " ganhou apos ", jogada + 1, " rodadas\n")

        jogada += 1

        # Verifica empate
        if jogada == 9 and ganhou(tabuleiro) == 0:
            print("\nEmpate\n")
            break


def menu():
    continuar = 1
    while continuar:
        continuar = int(input("0. Sair \n" +
                              "1. Novo Jogo\n"))
        if continuar:
            jogo()
        else:
            print("Saindo...")


menu()
