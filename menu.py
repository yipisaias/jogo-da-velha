def menu(novoJogo):
    continuar = 1
    while continuar:
        continuar = int(input("1. Novo jogo \n" +
                              "0. Sair \n"))
        print()
        if continuar == 1:
            novoJogo()
        elif continuar == 0:
            print("Saindo...")
        else:
            print('Opção inválida. Tente novamente.')
