from z3 import *


def TestDimensions(String, r, s):
    if r == len(String) and s == len(String[0]):
        return
    else:
        print("Dimensions do not match.")
        exit()


def ReplaceCountT(String):
    count_t = 0
    result = ""
    number_t = 0

    for line in String:
        for char in line:
            if char == "T":
                count_t += 1
                result += str(count_t)
                number_t += 1
            else:
                result += char
        result += "\n"

    return number_t, result


def CheckAttackers(String):
    count_k = 0
    count_j = 0
    count_t = 0
    for line in String:
        for char in line:
            if char == "n":
                Solver.add(
                    Or(
                        FindHorizontalT(String, count_k, count_j, count_t),
                        FindVerticalT(String, count_k, count_j),
                    )
                )
            count_j += 1
        count_j = 0
        count_k += 1


def CheckCrossFire(String):
    count_k = 0
    count_j = 0
    count_t = 0
    for line in String:
        for char in line:
            for i in range(1, TotalT + 1):
                if char == f"{i}":
                    Solver.add(
                        Not(
                            FindHorizontalT(String, count_k, count_j, count_t, i)
                        )
                    )
                    Solver.add(Not(FindVerticalT(String, count_k, count_j, i)))
            count_j += 1
        count_j = 0
        count_k += 1


def FormValuedMap(String):
    result = []
    valuedMap = ""
    count = 1
    for w in range(0, TotalT):
        if (
            m[VarVer[w]] == False
            and m[VarHor[w]] == True
            or (m[VarVer[w]] == False and m[VarHor[w]] == None)
        ):
            result.append(1)
        elif (
            m[VarVer[w]] == False
            and m[VarHor[w]] == False
            or (m[VarVer[w]] == None and m[VarHor[w]] == True)
        ):
            result.append(2)
        elif (
            m[VarVer[w]] == True
            and m[VarHor[w]] == False
            or (m[VarVer[w]] == True and m[VarHor[w]] == None)
        ):
            result.append(3)
        elif (
            m[VarVer[w]] == True
            and m[VarHor[w]] == True
            or (m[VarVer[w]] == None and m[VarHor[w]] == True)
        ):
            result.append(4)
    for line in String:
        for char in line:
            if char == f"{count}":
                valuedMap += str(result[count - 1])
                count += 1
            else:
                valuedMap += char
        valuedMap += "\n"
    return valuedMap


def FindHorizontalT(String, count_k, count_j, count_t, index=0):
    count = 0
    castle = False
    crossFire = False
    for char in String[count_k]:
        for f in range(1, TotalT + 1):
            if char == f"{f}" and int(char) != index:
                if count_j < count_t:
                    i = count
                    while i != count_j:
                        if String[count_k][i] == "#":
                            castle = True
                        elif (
                            String[count_k][i].isdecimal()
                            and int(String[count_k][i]) != f
                            and index == 0
                        ):
                            crossFire = True
                        i -= 1
                    if castle == False and crossFire == False:
                        return VarHor[f - 1]
                    else:
                        castle = False
                        crossFire = False
                        continue
                else:
                    for k in range(count, count_j):
                        if String[count_k][k] == "#":
                            castle = True
                        elif (
                            String[count_k][k].isdecimal()
                            and int(String[count_k][k]) != f
                            and index == 0
                        ):
                            crossFire = True
                    if castle == False and crossFire == False:
                        return Not(VarHor[f - 1])
                    else:
                        crossFire = False
                        castle = False
                        continue
        count += 1
        count_t += 1
    count_t = 0
    return False


def FindVerticalT(String, count_k, count_j, index=0):
    castle = False
    crossFire = False
    for i in range(0, r):
        for l in range(1, TotalT + 1):
            if String[i][count_j] == f"{l}" and int(String[i][count_j]) != index:
                if count_k < i:
                    for k in range(count_k, i):
                        if String[k][count_j] == "#":
                            castle = True
                        elif (
                            (String[k][count_j].isdecimal())
                            and int(String[k][count_j]) != l
                            and index == 0
                        ):
                            crossFire = True
                    if castle == False and crossFire == False:
                        return VarVer[l - 1]
                    else:
                        crossFire = False
                        castle = False
                        continue
                else:
                    for k in range(i, count_k):
                        if String[k][count_j] == "#":
                            castle = True
                        elif (
                            (String[k][count_j].isdecimal())
                            and int(String[k][count_j]) != l
                            and index == 0
                        ):
                            crossFire = True
                    if castle == False and crossFire == False:
                        return Not(VarVer[l - 1])
                    else:
                        crossFire = False
                        castle = False
                        continue
    return False


input_string = """9 8
n.Tnnnnn
nnnnnnTn
nTnnnnnn
nnnnTnnn
Tnnnnnnn
..#nnTnn
nnnnnnnT
nnnTn.n.
.nTnnnnn"""

lines = input_string.strip().split("\n")
dimensions = list(map(int, lines[0].split()))
r, s = dimensions[0], dimensions[1]
map_data = lines[1:]

TestDimensions(map_data, r, s)
TotalT, map_data = ReplaceCountT(map_data)

map_data = map_data.split("\n")
map_data = map_data[0:r]

Solver = Solver()
VarHor = [Bool("t" + str(i) + "e") for i in range(1, TotalT + 1)]
VarVer = [Bool("t" + str(i) + "c") for i in range(1, TotalT + 1)]

CheckAttackers(map_data)
CheckCrossFire(map_data)

if Solver.check() == sat:
    m = Solver.model()
else:
    print("Unsatisfiable formula")

print(FormValuedMap(map_data))