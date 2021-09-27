def menu(jogo):
    continuar = 1
    while continuar:
        continuar = int(input("1. Novo jogo \n" +
                              "0. Sair \n"))
        print()
        if continuar:
            jogo()
        else:
            print("Saindo...")
