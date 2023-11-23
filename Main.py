from z3 import *

def TesteDimensões(mapa, r, s):
    if r == len(mapa) and s == len(mapa[0]):
        print("As dimensões coincidem.")
    else:
        print("As dimensões não coincidem.")
        exit()


def SubstituirContarT(string):
    contagem_t = 0
    resultado = ""
    numero_t = 0

    for linha in string:
        for caractere in linha:
            if caractere == "T":
                contagem_t += 1
                resultado += str(contagem_t)
                numero_t += 1
            else:
                resultado += caractere
        resultado += "\n"

    return numero_t, resultado


def AcharTHorizontal(string, contadork, contadorj, contadort):
    contador = 0
    castelo = False
    for caractere in string[contadork]:
        for i in range(1, total_t + 1):
            if caractere == f"{i}":
                print(caractere)
                if contadorj < contadort:
                    for i in range (contador,contadorj):
                        print(string[contadork][contador])
                        if string[contadork][contador] == "#":
                            print("Castelo")
                            castelo = True
                    if castelo == False:
                        print("atirar esquerda")
                    else:
                        castelo = False
                        continue
                else:
                    for k in range(0, contadorj):
                        if string[contadork][k] == "#":
                            print("Castelo")
                            castelo = True
                    if castelo == False:
                        print("atirar direita")
                    else:
                        castelo = False
                        continue
        contador += 1
        contadort += 1
    contadort = 0
    return False


def AcharTVertical(string, contadork, contadorj):
    castelo = False
    for i in range(0, r):
        for l in range(1, total_t + 1):
            if string[i][contadorj] == f"{l}":
                print(string[i][contadorj])
                if contadork < i:
                    for k in range(contadork, i):
                        if string[k][contadorj] == "#":
                            print("Castelo")
                            castelo = True
                    if castelo == False:
                        print("atirar pra cima")
                    else:
                        castelo = False
                        continue
                else:
                    for k in range(i, contadork):
                        if string[k][contadorj] == "#":
                            print("Castelo")
                            castelo = True
                    if castelo == False:
                        print("atirar pra baixo")
                    else:
                        castelo = False
                        continue
    return False


def FazerFormulas(string):
    contadork = 0
    contadorj = 0
    contadort = 0
    for linha in string:
        print(linha)
    for linha in string:
        for caractere in linha:
            if caractere == "n":
                print(caractere)
                AcharTHorizontal(string, contadork, contadorj, contadort)
                AcharTVertical(string, contadork, contadorj)
            contadorj += 1
        contadorj = 0
        contadork += 1


entrada = """9 13
.............
...........n.
.n.T..nnnn#..
.............
.T#n..n....T.
.............
.n.T..T....n.
.............
......n......"""

linhas = entrada.strip().split("\n")
dimensoes = list(map(int, linhas[0].split()))
r, s = dimensoes[0], dimensoes[1]
mapa = linhas[1:]
TesteDimensões(mapa, r, s)
print(mapa)

total_t, mapa = SubstituirContarT(mapa)

VarHor = [Bool("t" + str(i) + "e") for i in range(1, total_t + 1)]
VarVer = [Bool("t" + str(i) + "c") for i in range(1, total_t + 1)]

mapa = mapa.split("\n")
mapa = mapa[0:r]
print(mapa)

FazerFormulas(mapa)
