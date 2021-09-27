from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro
from jogada import jogada, msgVitoria, msgDerrota
from menu import menu


def quemComeca():
    print("Qual jogador começa?")
    print("1. Eu")
    print("2. Meu adversário")
    player = str(input())
    while player != "1" and player != "2":
        print('Opção inválida. Tente novamente.')
        player = str(input())
    print()
    servidor(player)


def servidor(player):
    # Cria o socket TCP/IP
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Faz o bind no endereco e porta
    server_address = ('localhost', 5000)
    serverSocket.bind(server_address)

    # Fica ouvindo por conexoes
    serverSocket.listen(1)

    stop = False
    while not stop:
        print('Aguardando a conexão do adversário')
        connection, client_address = serverSocket.accept()

        try:
            print('Adversário chegou! :)')

            # Cria um tabuleiro de jogo vazio
            tabuleiro = Tabuleiro()

            print('------------------')
            tabuleiro.print()

            # Envia para o cliente qual jogador comeca
            connection.sendall(''.join(player).encode('utf-8'))

            if player == "1":
                # Turno do servidor
                jogada(tabuleiro, 'x')

                tabuleiro.print()

                # Envia o tabuleiro e qual player comeca para o jogador
                connection.sendall(tabuleiro.save().encode('utf-8'))

            # Processa em loop
            while tabuleiro.finish() == 0:
                print("Aguardando turno do adversário...")

                # Recebe a jogada do jogador
                data = connection.recv(1024)

                # Checa se a conexao do jogador foi terminada
                if not data:
                    print('Adversário se foi. :(')
                    break

                # Converte para string e restaura no tabuleiro
                tabuleiro.restore(data.decode('utf-8'))

                print('O adversário jogou:')
                tabuleiro.print()

                # Verifica condicao de vitoria/derrota ou empate
                if tabuleiro.result(tabuleiro.finish(), msgVitoria, msgDerrota):
                    print('Encerrando o cliente\n')
                    stop = True
                    break

                jogada(tabuleiro, 'x')

                tabuleiro.print()
                print('------------------')

                # Envia o tabuleiro para o jogador
                connection.sendall(tabuleiro.save().encode('utf-8'))

                # Verifica condicao de vitoria/derrota ou empate
                if tabuleiro.result(tabuleiro.finish(), msgVitoria, msgDerrota):
                    print('Encerrando o cliente\n')
                    stop = True
                    break

        finally:
            # Clean up the connection
            connection.close()


menu(quemComeca)
