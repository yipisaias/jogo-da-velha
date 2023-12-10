from socket import socket, AF_INET, SOCK_STREAM
from tabuleiro import Tabuleiro
from jogada import jogada, revanche, msgVitoria, msgDerrota
from menu import menu


def cliente():
    # Cria o socket TCP/IP
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Conecta o socket na porta onde o servidor esta escutando
    conectou = False
    while not conectou:
        server_IP = input('IP do servidor (padrão: localhost): ') or "localhost"
        try:
            server_port = int(input('Porta (padrão: 5000): '))
        except ValueError:
            server_port = 5000
        server_address = (server_IP, server_port)
        print('Conectando ao servidor {} na porta {}'.format(
            server_address[0], server_address[1]))
        try:
            clientSocket.connect(server_address)
            conectou = True
        except:
            print("Falha ao estabelecer conexão com o servidor.\n")

    jogaRevanche = True
    while jogaRevanche:
        # Cria um tabuleiro de jogo vazio
        tabuleiro = Tabuleiro()
        tabuleiro.print()

        # Recebe quem comeca
        response = clientSocket.recv(1024).decode('utf-8')
        if response == "2":
            # Turno do cliente
            jogada(tabuleiro, 'o')

            tabuleiro.print()

            # Envia o tabuleiro para o adversario
            clientSocket.sendall(tabuleiro.save().encode('utf-8'))

        while tabuleiro.finish() == 0:
            print("Aguardando turno do adversário...")

            # Recebe a jogada do adversario
            data = clientSocket.recv(1024)
            if not data:
                print('Adversário se foi. :(')
                jogaRevanche = False
                print('Encerrando o cliente\n')
                clientSocket.close()
                break

            tabuleiro.restore(data.decode('utf-8'))

            print('O adversário jogou:')
            tabuleiro.print()

            # Verifica condicao de vitoria/derrota ou empate
            if tabuleiro.result(tabuleiro.finish(), msgDerrota, msgVitoria):
                rev = revanche()
                clientSocket.sendall('{}'.format(rev).encode('utf-8'))
                if rev:
                    print("Aguardando resposta do servidor...")
                    try:
                        res = clientSocket.recv(1024)
                        # Checa se a conexao do adversario foi terminada
                        if not eval(res.decode('utf-8')):
                            print('Adversário se foi. :(')
                            jogaRevanche = False
                            print('Encerrando o cliente\n')
                            clientSocket.close()
                        else:
                            print("Aguardando definição de quem começa...")
                    except:
                        print('Adversário se foi. :(')
                        jogaRevanche = False
                        print('Encerrando o cliente\n')
                        clientSocket.close()
                else:
                    jogaRevanche = False
                    print('Encerrando o cliente\n')
                    clientSocket.close()
                break

            # Turno do cliente
            jogada(tabuleiro, 'o')

            tabuleiro.print()
            print('------------------')

            # Envia o tabuleiro para o adversario
            clientSocket.sendall(tabuleiro.save().encode('utf-8'))

            # Verifica condicao de vitoria/derrota ou empate
            if tabuleiro.result(tabuleiro.finish(), msgDerrota, msgVitoria):
                rev = revanche()
                clientSocket.sendall('{}'.format(rev).encode('utf-8'))
                if rev:
                    print("Aguardando resposta do servidor...")
                    try:
                        res = clientSocket.recv(1024)
                        # Checa se a conexao do adversario foi terminada
                        if not eval(res.decode('utf-8')):
                            print('Adversário se foi. :(')
                            jogaRevanche = False
                            print('Encerrando o cliente\n')
                            clientSocket.close()
                        else:
                            print("Aguardando definição de quem começa...")
                    except:
                        print('Adversário se foi. :(')
                        jogaRevanche = False
                        print('Encerrando o cliente\n')
                        clientSocket.close()
                else:
                    jogaRevanche = False
                    print('Encerrando o cliente\n')
                    clientSocket.close()
                break


menu(cliente)
