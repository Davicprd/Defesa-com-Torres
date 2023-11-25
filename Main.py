from z3 import *


def TesteDimensões(String, r, s):
    if r == len(String) and s == len(String[0]):
        return
    else:
        print("As dimensões não coincidem.")
        exit()


def SubstituirContarT(String):
    contagemt = 0
    resultado = ""
    numerot = 0

    for linha in String:
        for caractere in linha:
            if caractere == "T":
                contagemt += 1
                resultado += str(contagemt)
                numerot += 1
            else:
                resultado += caractere
        resultado += "\n"

    return numerot, resultado


def VerificarAtacantes(String):
    contadork = 0
    contadorj = 0
    contadort = 0
    for linha in String:
        for caractere in linha:
            if caractere == "n":
                Solver.add(
                    Or(
                        AcharTHorizontal(String, contadork, contadorj, contadort),
                        AcharTVertical(String, contadork, contadorj),
                    )
                )
            contadorj += 1
        contadorj = 0
        contadork += 1


def VerificarFogoCruzado(String):
    contadork = 0
    contadorj = 0
    contadort = 0
    for linha in String:
        for caractere in linha:
            for i in range(1, TotalT + 1):
                if caractere == f"{i}":
                    Solver.add(
                        Not(
                            AcharTHorizontal(String, contadork, contadorj, contadort, i)
                        )
                    )
                    Solver.add(Not(AcharTVertical(String, contadork, contadorj, i)))
            contadorj += 1
        contadorj = 0
        contadork += 1


def FormarMapaValorado(String):
    resultado = []
    MapaValorado = ""
    contagem = 1
    for w in range(0, TotalT):
        if (
            m[VarVer[w]] == False
            and m[VarHor[w]] == True
            or (m[VarVer[w]] == False and m[VarHor[w]] == None)
        ):
            resultado.append(1)
        elif (
            m[VarVer[w]] == False
            and m[VarHor[w]] == False
            or (m[VarVer[w]] == None and m[VarHor[w]] == True)
        ):
            resultado.append(2)
        elif (
            m[VarVer[w]] == True
            and m[VarHor[w]] == False
            or (m[VarVer[w]] == True and m[VarHor[w]] == None)
        ):
            resultado.append(3)
        elif (
            m[VarVer[w]] == True
            and m[VarHor[w]] == True
            or (m[VarVer[w]] == None and m[VarHor[w]] == True)
        ):
            resultado.append(4)
    for linha in String:
        for caractere in linha:
            if caractere == f"{contagem}":
                MapaValorado += str(resultado[contagem - 1])
                contagem += 1
            else:
                MapaValorado += caractere
        MapaValorado += "\n"
    return MapaValorado


def AcharTHorizontal(String, contadork, contadorj, contadort, index=0):
    contador = 0
    castelo = False
    fogoCruzado = False
    for caractere in String[contadork]:
        for f in range(1, TotalT + 1):
            if caractere == f"{f}" and int(caractere) != index:
                if contadorj < contadort:
                    i = contador
                    while i != contadorj:
                        if String[contadork][i] == "#":
                            castelo = True
                        elif (
                            String[contadork][i].isdecimal()
                            and int(String[contadork][i]) != f
                            and index == 0
                        ):
                            fogoCruzado = True
                        i -= 1
                    if castelo == False and fogoCruzado == False:
                        return VarHor[f - 1]
                    else:
                        castelo = False
                        fogoCruzado = False
                        continue
                else:
                    for k in range(contador, contadorj):
                        if String[contadork][k] == "#":
                            castelo = True
                        elif (
                            String[contadork][k].isdecimal()
                            and int(String[contadork][k]) != f
                            and index == 0
                        ):
                            fogoCruzado = True
                    if castelo == False and fogoCruzado == False:
                        return Not(VarHor[f - 1])
                    else:
                        fogoCruzado = False
                        castelo = False
                        continue
        contador += 1
        contadort += 1
    contadort = 0
    return False


def AcharTVertical(String, contadork, contadorj, index=0):
    castelo = False
    fogoCruzado = False
    for i in range(0, r):
        for l in range(1, TotalT + 1):
            if String[i][contadorj] == f"{l}" and int(String[i][contadorj]) != index:
                if contadork < i:
                    for k in range(contadork, i):
                        if String[k][contadorj] == "#":
                            castelo = True
                        elif (
                            (String[k][contadorj].isdecimal())
                            and int(String[k][contadorj]) != l
                            and index == 0
                        ):
                            fogoCruzado = True
                    if castelo == False and fogoCruzado == False:
                        return VarVer[l - 1]
                    else:
                        fogoCruzado = False
                        castelo = False
                        continue
                else:
                    for k in range(i, contadork):
                        if String[k][contadorj] == "#":
                            castelo = True
                        elif (
                            (String[k][contadorj].isdecimal())
                            and int(String[k][contadorj]) != l
                            and index == 0
                        ):
                            fogoCruzado = True
                    if castelo == False and fogoCruzado == False:
                        return Not(VarVer[l - 1])
                    else:
                        fogoCruzado = False
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
TotalT, mapa = SubstituirContarT(mapa)

mapa = mapa.split("\n")
mapa = mapa[0:r]

Solver = Solver()
VarHor = [Bool("t" + str(i) + "e") for i in range(1, TotalT + 1)]
VarVer = [Bool("t" + str(i) + "c") for i in range(1, TotalT + 1)]

VerificarAtacantes(mapa)
VerificarFogoCruzado(mapa)

if Solver.check() == sat:
    m = Solver.model()
else:
    print("Fórmula Insatisfatível")

print(FormarMapaValorado(mapa))
