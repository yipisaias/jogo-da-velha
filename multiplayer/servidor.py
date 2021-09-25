import socket
from gamestate import GameState

# Cria o socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o bind no endereco e porta
server_address = ('localhost', 5000)
sock.bind(server_address)

# Fica ouvindo por conexoes
sock.listen(1)

while True:

    print('Aguardando a conexao do jogador')
    connection, client_address = sock.accept()

    try:
        print('Jogador chegou! :)')

        # Cria um tabuleiro de jogo vazio
        board = GameState()

        # Faz uma jogada aleatoria
        board.moveRandom('o')
        print('Eu joguei:')
        board.print()

        # Envia o tabuleiro para o jogador
        connection.sendall(board.save().encode('utf-8'))

        # Processa em loop
        while True:
            # Recebe a jogada do jogador
            data = connection.recv(1024)

            # Checa se a conexao do jogador foi terminada
            if not data:
                print('Jogador se foi. :(')
                break

            # Converte para string e restaura no tabuleiro
            board.restore(data.decode('utf-8'))

            print('O jogador jogou:')
            board.print()

            # Faz outra jogada aleatoria
            board.moveRandom('o')
            print('Eu joguei:')
            board.print()

            # Envia o tabuleiro para o jogador
            connection.sendall(board.save().encode('utf-8'))

    finally:
        # Clean up the connection
        connection.close()
