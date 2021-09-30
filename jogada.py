from inputimeout import inputimeout, TimeoutOccurred


msgVitoria = "Parabéns! Você venceu!"
msgDerrota = "Seu adversário venceu!"
tempoJogada = 60
msgTimeout = "Jogada automática devido à demora."


def jogada(tabuleiro, simbolo):
    nok = True
    while nok:
        try:
            row = int(inputimeout(
                "Digite a linha (1 minuto para digitar):", tempoJogada)) - 1
        except TimeoutOccurred:
            print(msgTimeout)
            tabuleiro.moveRandom(simbolo)
            return
        try:
            col = int(inputimeout(
                "Digite a coluna (1 minuto para digitar):", tempoJogada)) - 1
        except TimeoutOccurred:
            print(msgTimeout)
            tabuleiro.moveRandom(simbolo)
            return

        nok = False
        try:
            tabuleiro.move(row, col, simbolo)

        except:
            nok = True
            print("Linha ou coluna inválida. Tente novamente.")
