from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro


def result(status):
    if status == 1:
        print("Parabéns! Você venceu!")
        return True
    elif status == 2:
        print("Seu adversário venceu!")
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
            tabuleiro.move(row, col, 'x')

        except:
            nok = True
            print('Linha ou coluna inválida. Tente novamente.')


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


def menu():
    continuar = 1
    while continuar:
        continuar = int(input("1. Novo jogo \n" +
                              "0. Sair \n"))
        print()
        if continuar:
            quemComeca()
        else:
            print("Saindo...")


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
        print('Aguardando a conexao do adversário')
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
                jogada(tabuleiro)

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
                if result(tabuleiro.finish()):
                    print('Encerrando o cliente\n')
                    stop = True
                    break

                jogada(tabuleiro)

                tabuleiro.print()
                print('------------------')

                # Envia o tabuleiro para o jogador
                connection.sendall(tabuleiro.save().encode('utf-8'))

                # Verifica condicao de vitoria/derrota ou empate
                if result(tabuleiro.finish()):
                    print('Encerrando o cliente\n')
                    stop = True
                    break

        finally:
            # Clean up the connection
            connection.close()


menu()
