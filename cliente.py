from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro


def result(status):
    if status == 1:
        print("Seu adversário venceu!")
        return True
    elif status == 2:
        print("Parabéns! Você venceu!")
        return True
    elif status == 9:
        print("Jogo empatou")
        return True

    return False


def jogada(tabuleiro):
    nok = True
    while nok:
        row = int(input('Digite a linha:')) - 1
        col = int(input('Digite a coluna:')) - 1

        nok = False
        try:
            tabuleiro.move(row, col, 'o')

        except:
            nok = True
            print('Linha ou coluna inválida. Tente novamente.')


# Create a TCP/IP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('Conectando ao servidor {} na porta {}'.format(
    server_address[0], server_address[1]))
clientSocket.connect(server_address)

# Cria um tabuleiro de jogo vazio
tabuleiro = Tabuleiro()
tabuleiro.print()
try:
    response = clientSocket.recv(1024).decode('utf-8')
    if response == "2":
        # Turno do cliente
        jogada(tabuleiro)

        tabuleiro.print()

        # Envia o tabuleiro para o jogador
        clientSocket.sendall(tabuleiro.save().encode('utf-8'))

    while tabuleiro.finish() == 0:
        print("Aguardando turno do adversário...")

        # Recebe a jogada do servidor
        data = clientSocket.recv(1024)
        if data:
            tabuleiro.restore(data.decode('utf-8'))

            print('O adversário jogou:')
            tabuleiro.print()

            # Verifica condicao de vitoria/derrota ou empate
            if result(tabuleiro.finish()):
                break

            # Turno do cliente
            jogada(tabuleiro)

            tabuleiro.print()
            print('------------------')

            # Envia o tabuleiro para o servidor
            clientSocket.sendall(tabuleiro.save().encode('utf-8'))

            # Verifica condicao de vitoria/derrota ou empate
            if result(tabuleiro.finish()):
                break

        else:
            break

finally:
    print('Encerrando o cliente')
    clientSocket.close()
