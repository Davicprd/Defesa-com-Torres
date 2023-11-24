from z3 import *


def TesteDimensões(mapa, r, s):
    if r == len(mapa) and s == len(mapa[0]):
        return
    else:
        print("As dimensões não coincidem.")
        exit()


def SubstituirContarT(string):
    contagemt = 0
    resultado = ""
    numerot = 0

    for linha in string:
        for caractere in linha:
            if caractere == "T":
                contagemt += 1
                resultado += str(contagemt)
                numerot += 1
            else:
                resultado += caractere
        resultado += "\n"

    return numerot, resultado


def VerificarAtacantes(string):
    contadork = 0
    contadorj = 0
    contadort = 0
    for linha in string:
        for caractere in linha:
            if caractere == "n":
                Solver.add(
                    Or(
                        AcharTHorizontal(string, contadork, contadorj, contadort),
                        AcharTVertical(string, contadork, contadorj),
                    )
                )
            contadorj += 1
        contadorj = 0
        contadork += 1


def VerificarFogoCrusado(string):
    contadork = 0
    contadorj = 0
    contadort = 0
    for linha in string:
        for caractere in linha:
            for i in range(1, total_t + 1):
                if caractere == f"{i}":
                    Solver.add(
                        Not(
                            AcharTHorizontal(string, contadork, contadorj, contadort, i)
                        )
                    )
                    Solver.add(Not(AcharTVertical(string, contadork, contadorj, i)))
            contadorj += 1
        contadorj = 0
        contadork += 1


def AcharTHorizontal(string, contadork, contadorj, contadort, index=0):
    contador = 0
    castelo = False
    fogocrusado = False
    for caractere in string[contadork]:
        for f in range(1, total_t + 1):
            if caractere == f"{f}" and int(caractere) != index:
                if contadorj < contadort:
                    i = contador
                    while i != contadorj:
                        if string[contadork][i] == "#":
                            castelo = True
                        elif (
                            string[contadork][i].isdecimal()
                            and int(string[contadork][i]) != f
                        ):
                            fogocrusado = True
                        i -= 1
                    if castelo == False and fogocrusado == False:
                        return VarHor[f - 1]
                    else:
                        castelo = False
                        fogocrusado = False
                        continue
                else:
                    for k in range(contador, contadorj):
                        if string[contadork][k] == "#":
                            castelo = True
                        elif (
                            string[contadork][k].isdecimal()
                            and int(string[contadork][k]) != f
                        ):
                            fogocrusado = True
                    if castelo == False and fogocrusado == False:
                        return Not(VarHor[f - 1])
                    else:
                        fogocrusado = False
                        castelo = False
                        continue
        contador += 1
        contadort += 1
    contadort = 0
    return False


def AcharTVertical(string, contadork, contadorj, index=0):
    castelo = False
    fogocrusado = False
    for i in range(0, r):
        for l in range(1, total_t + 1):
            if string[i][contadorj] == f"{l}" and int(string[i][contadorj]) != index:
                if contadork < i:
                    for k in range(contadork, i):
                        if string[k][contadorj] == "#":
                            castelo = True
                        elif (string[k][contadorj].isdecimal()) and int(
                            string[k][contadorj]
                        ) != l:
                            fogocrusado = True
                    if castelo == False and fogocrusado == False:
                        return VarVer[l - 1]
                    else:
                        fogocrusado = False
                        castelo = False
                        continue
                else:
                    for k in range(i, contadork):
                        if string[k][contadorj] == "#":
                            castelo = True
                        elif (string[k][contadorj].isdecimal()) and int(
                            string[k][contadorj]
                        ) != l:
                            fogocrusado = True
                    if castelo == False and fogocrusado == False:
                        return Not(VarVer[l - 1])
                    else:
                        fogocrusado = False
                        castelo = False
                        continue
    return False


entrada = """9 8
n.Tnnnnn
nnnnnnTn
nTnnnnnn
nnnnTnnn
Tnnnnnnn
..#nnTnn
nnnnnnnT
nnnTn.n.
.nTnnnnn"""

linhas = entrada.strip().split("\n")
dimensoes = list(map(int, linhas[0].split()))
r, s = dimensoes[0], dimensoes[1]
mapa = linhas[1:]

TesteDimensões(mapa, r, s)
total_t, mapa = SubstituirContarT(mapa)

mapa = mapa.split("\n")
mapa = mapa[0:r]

Solver = Solver()
VarHor = [Bool("t" + str(i) + "e") for i in range(1, total_t + 1)]
VarVer = [Bool("t" + str(i) + "c") for i in range(1, total_t + 1)]

VerificarAtacantes(mapa)
VerificarFogoCrusado(mapa)

print(Solver.assertions())

if Solver.check() == sat:
    print(Solver.model())
    print("Fórmula Satisfatível")
else:
    print("Fórmula Insatisfatível")
