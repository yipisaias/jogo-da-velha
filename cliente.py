from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro
from jogada import jogada, msgVitoria, msgDerrota
from menu import menu


def cliente():
    # Create a TCP/IP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    conectou = False
    while not conectou:
        server_address = str(input('IP do servidor: '))
        server_address = (server_address, 5000)
        print('Conectando ao servidor {} na porta {}'.format(
            server_address[0], server_address[1]))
        try:
            clientSocket.connect(server_address)
            conectou = True
        except:
            print("Falha ao estabelecer conexão com o servidor.\n")

    # Cria um tabuleiro de jogo vazio
    tabuleiro = Tabuleiro()
    tabuleiro.print()
    try:
        response = clientSocket.recv(1024).decode('utf-8')
        if response == "2":
            # Turno do cliente
            jogada(tabuleiro, 'o')

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
                if tabuleiro.result(tabuleiro.finish(), msgDerrota, msgVitoria):
                    break

                # Turno do cliente
                jogada(tabuleiro, 'o')

                tabuleiro.print()
                print('------------------')

                # Envia o tabuleiro para o servidor
                clientSocket.sendall(tabuleiro.save().encode('utf-8'))

                # Verifica condicao de vitoria/derrota ou empate
                if tabuleiro.result(tabuleiro.finish(), msgDerrota, msgVitoria):
                    break

            else:
                break

    finally:
        print('Encerrando o cliente\n')
        clientSocket.close()


menu(cliente)
