msgVitoria = "Parabéns! Você venceu!"
msgDerrota = "Seu adversário venceu!"


def jogada(tabuleiro, simbolo):
    nok = True
    while nok:
        row = int(input('Digite a linha:')) - 1
        col = int(input('Digite a coluna:')) - 1

        nok = False
        try:
            tabuleiro.move(row, col, simbolo)

        except:
            nok = True
            print('Linha ou coluna inválida. Tente novamente.')
