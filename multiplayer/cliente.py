import socket
import sys
from gamestate import GameState

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('Conectando ao servidor {} na porta {}'.format(
    server_address[0], server_address[1]))
sock.connect(server_address)

# Cria um tabuleiro de jogo vazio
board = GameState()

try:

    while True:
        print("Aguardando turno do adversário...")

        # Recebe a jogada do servidor
        data = sock.recv(1024)
        if data:
            board.restore(data.decode('utf-8'))

            print('O adversário jogou:')
            board.print()

            # Turno do cliente
            print('------------------')
            status = board.ganhou()
            if status == 1:
                print("Jogador 1 ganhou")
                nok = False
                break
            elif status == 2:
                print("Jogador 2 ganhou")
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
                    board.move(row, col, 'o')
                except:
                    nok = True
                    print('Linha ou coluna inválida. Tente novamente.')
            board.print()
            status = board.ganhou()
            if status == 1:
                print("Jogador 1 ganhou")
                board.print()
                break
            elif status == 2:
                print("Jogador 2 ganhou")
                board.print()
                break
            elif status == 9:
                print("Jogo empatou")
                board.print()
                nok = False
                break
            # Envia o tabuleiro para o servidor
            sock.sendall(board.save().encode('utf-8'))
        else:
            break
finally:
    print('Encerrando o cliente')
    sock.close()
