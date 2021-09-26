from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro

# Cria o socket TCP/IP
serverSocket = socket(AF_INET, SOCK_STREAM)

# Faz o bind no endereco e porta
server_address = ('localhost', 5000)
serverSocket.bind(server_address)

# Fica ouvindo por conexoes
serverSocket.listen(1)

while True:

    print('Aguardando a conexao do adversário')
    connection, client_address = serverSocket.accept()

    try:
        print('Adversário chegou! :)')

        # Cria um tabuleiro de jogo vazio
        tabuleiro = Tabuleiro()

        # Turno do servidor
        print('------------------')
        tabuleiro.print()
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

        tabuleiro.print()
        # Envia o tabuleiro para o jogador
        connection.sendall(tabuleiro.save().encode('utf-8'))

        # Processa em loop
        while True:
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

            print('------------------')
            status = tabuleiro.winner()
            if status == 1:
                print("Parabéns! Você venceu!")
                print('Encerrando o cliente')
                nok = False
            elif status == 2:
                print("Seu adversário venceu!")
                print('Encerrando o cliente')
                nok = False
            elif status == 9:
                print("Jogo empatou")
                print('Encerrando o cliente')
                nok = False
                break
            else:
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
            tabuleiro.print()
            status = tabuleiro.winner()
            if status == 1:
                connection.sendall(tabuleiro.save().encode('utf-8'))
                print("Parabéns! Você venceu!")
                print('Encerrando o cliente')
                break
            elif status == 2:
                connection.sendall(tabuleiro.save().encode('utf-8'))
                print("Seu adversário venceu!")
                print('Encerrando o cliente')
                break
            elif status == 9:
                connection.sendall(tabuleiro.save().encode('utf-8'))
                print("Jogo empatou")
                print('Encerrando o cliente')
                break

            # Envia o tabuleiro para o jogador
            connection.sendall(tabuleiro.save().encode('utf-8'))

    finally:
        # Clean up the connection
        connection.close()
