from socket import socket, AF_INET, SOCK_STREAM
import sys
from tabuleiro import Tabuleiro

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

    while True:
        print("Aguardando turno do adversário...")

        # Recebe a jogada do servidor
        data = clientSocket.recv(1024)
        if data:
            tabuleiro.restore(data.decode('utf-8'))

            print('O adversário jogou:')
            tabuleiro.print()

            # Turno do cliente
            print('------------------')
            status = tabuleiro.winner()
            if status == 1:
                print("Seu adversário venceu!")
                nok = False
                break
            elif status == 2:
                print("Parabéns! Você venceu!")
                nok = False
                break
            elif status == 9:
                print("Jogo empatou")
                nok = False
                break
            else:
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
            tabuleiro.print()
            status = tabuleiro.winner()
            if status == 1:
                tabuleiro.print()
                print("Seu adversário venceu!")
                break
            elif status == 2:
                tabuleiro.print()
                print("Parabéns! Você venceu!")
                break
            elif status == 9:
                tabuleiro.print()
                print("Jogo empatou")
                nok = False
                break
            # Envia o tabuleiro para o servidor
            clientSocket.sendall(tabuleiro.save().encode('utf-8'))
        else:
            break
finally:
    print('Encerrando o cliente')
    clientSocket.close()
