from socket import socket, AF_INET, SOCK_STREAM
from gamestate import GameState

# Cria o socket TCP/IP
sock = socket(AF_INET, SOCK_STREAM)

# Faz o bind no endereco e porta
server_address = ('localhost', 5000)
sock.bind(server_address)

# Fica ouvindo por conexoes
sock.listen(1)

while True:

    print('Aguardando a conexao do adversário')
    connection, client_address = sock.accept()

    try:
        print('Adversário chegou! :)')

        # Cria um tabuleiro de jogo vazio
        board = GameState()

        """
        # Faz uma jogada aleatoria
        board.moveRandom('o')
        print('Eu joguei:')
        board.print()
        """

        # Turno do servidor
        print('------------------')
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

        # Envia o tabuleiro para o jogador
        connection.sendall(board.save().encode('utf-8'))

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
            board.restore(data.decode('utf-8'))

            print('O adversário jogou:')
            board.print()

            print('------------------')
            status = board.ganhou()
            if status == 1:
                print("Jogador x ganhou")
                board.print()
                print('Encerrando o cliente')
                nok = False
            elif status == 2:
                print("Jogador o ganhou")
                board.print()
                print('Encerrando o cliente')
                nok = False
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
            status = board.ganhou()
            if status == 1:
                print("Jogador x ganhou")
                board.print()
                print('Encerrando o cliente')
                break
            elif status == 2:
                print("Jogador o ganhou")
                board.print()
                print('Encerrando o cliente')
                break

            # Envia o tabuleiro para o jogador
            connection.sendall(board.save().encode('utf-8'))

    finally:
        # Clean up the connection
        connection.close()
