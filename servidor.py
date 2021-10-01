from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro
from jogada import jogada, revanche, msgVitoria, msgDerrota
from menu import menu


def quemComeca():
    print("Qual jogador começa?")
    print("1. Eu")
    print("2. Meu adversário")
    player = input()
    while player != "1" and player != "2":
        print('\nOpção inválida. Tente novamente.')
        print("Qual jogador começa?")
        print("1. Eu")
        print("2. Meu adversário")
        player = input()
    print()
    return player


def servidor():
    player = quemComeca()

    # Cria o socket TCP/IP
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Faz o bind no endereco e porta para todos os enderecos IPv4 disponiveis no host
    server_address = ('', 5000)
    serverSocket.bind(server_address)

    # Fica ouvindo por conexoes
    serverSocket.listen(1)

    stopListen = False
    while not stopListen:
        print('Aguardando a conexão do adversário')
        connection, client_address = serverSocket.accept()

        print('Adversário chegou! :)')

        jogaRevanche = True
        while jogaRevanche:
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

                # Envia o tabuleiro para o adversario
                connection.sendall(tabuleiro.save().encode('utf-8'))

            # Processa em loop
            while tabuleiro.finish() == 0:
                print("Aguardando turno do adversário...")

                # Recebe a jogada do adversario
                data = connection.recv(1024)

                # Checa se a conexao do adversario foi terminada
                if not data:
                    print('Adversário se foi. :(')
                    stopListen = True
                    jogaRevanche = False
                    print('Encerrando a conexão\n')
                    connection.close()
                    break

                # Converte para string e restaura no tabuleiro
                tabuleiro.restore(data.decode('utf-8'))

                print('O adversário jogou:')
                tabuleiro.print()

                # Verifica condicao de vitoria/derrota ou empate
                if tabuleiro.result(tabuleiro.finish(), msgVitoria, msgDerrota):
                    rev = revanche()
                    connection.sendall('{}'.format(rev).encode('utf-8'))
                    if rev:
                        print("Aguardando resposta do adversário...")
                        try:
                            res = connection.recv(1024)
                            # Checa se a conexao do adversario foi terminada
                            if not eval(res.decode('utf-8')):
                                print('Adversário se foi. :(')
                                stopListen = True
                                jogaRevanche = False
                                print('Encerrando a conexão\n')
                                connection.close()
                            else:
                                player = quemComeca()
                        except:
                            print('Adversário se foi. :(')
                            stopListen = True
                            jogaRevanche = False
                            print('Encerrando a conexão\n')
                            connection.close()
                    else:
                        stopListen = True
                        jogaRevanche = False
                        print('Encerrando a conexão\n')
                        connection.close()
                    break

                jogada(tabuleiro, 'x')

                tabuleiro.print()
                print('------------------')

                # Envia o tabuleiro para o adversario
                connection.sendall(tabuleiro.save().encode('utf-8'))

                # Verifica condicao de vitoria/derrota ou empate
                if tabuleiro.result(tabuleiro.finish(), msgVitoria, msgDerrota):
                    rev = revanche()
                    connection.sendall('{}'.format(rev).encode('utf-8'))
                    if rev:
                        print("Aguardando resposta do adversário...")
                        try:
                            res = connection.recv(1024)
                            # Checa se a conexao do adversario foi terminada
                            if not eval(res.decode('utf-8')):
                                print('Adversário se foi. :(')
                                stopListen = True
                                jogaRevanche = False
                                print('Encerrando a conexão\n')
                                connection.close()
                            else:
                                player = quemComeca()
                        except:
                            print('Adversário se foi. :(')
                            stopListen = True
                            jogaRevanche = False
                            print('Encerrando a conexão\n')
                            connection.close()
                    else:
                        stopListen = True
                        jogaRevanche = False
                        print('Encerrando a conexão\n')
                        connection.close()
                    break


menu(servidor)
