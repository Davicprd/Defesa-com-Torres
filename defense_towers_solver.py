from z3 import *


def TestDimensions(String, r, s):
    """
    Checks if the dimensions of the map match the given parameters.

    Args:
    - String: The map layout as a list of strings.
    - r: The expected number of rows.
    - s: The expected number of columns.

    Returns:
    - None
    """

    if r == len(String) and s == len(String[0]):
        return
    else:
        print("Dimensions do not match.")
        exit()


def ReplaceCountT(String):
    """
    Replaces towers ('T') in the map with sequential numbers.

    Args:
    - String: The map layout as a list of strings.

    Returns:
    - total_t: The total number of towers.
    - result: The map layout with towers replaced by numbers.
    """

    # count_t = 0
    result = ""
    total_t = 0

    for row in String:
        for char in row:
            if char == "T":
                # count_t += 1
                total_t += 1
                result += str(total_t)
            else:
                result += char
        result += "\n"

    return total_t, result


def CheckAttackers(String):
    """
    Adds constraints to the Z3 solver based on attacker positions in the map.

    Args:
    - String: The map layout as a list of strings.

    Returns:
    - None
    """

    row_index = 0
    col_index = 0
    tower_row = 0
    for row in String:
        for char in row:
            if char == "n":
                Solver.add(
                    Or(
                        FindHorizontalT(String, row_index, col_index, tower_row),
                        FindVerticalT(String, row_index, col_index),
                    )
                )
            col_index += 1
        col_index = 0
        row_index += 1


def CheckCrossFire(String):
    """
    Adds constraints to the Z3 solver to avoid crossfire among cannons.

    Args:
    - String: The map layout as a list of strings.

    Returns:
    - None
    """
    
    row_index = 0
    col_index = 0
    tower_row = 0
    for row in String:
        for char in row:
            for i in range(1, TotalT + 1):
                if char == f"{i}":
                    Solver.add(
                        Not(
                            FindHorizontalT(String, row_index, col_index, tower_row, i)
                        )
                    )
                    Solver.add(Not(FindVerticalT(String, row_index, col_index, i)))
            col_index += 1
        col_index = 0
        row_index += 1


def FormValuedMap(String):
    """
    Creates the final map with cannon orientations based on the solver's solution.

    Args:
    - String: The map layout as a list of strings.

    Returns:
    - Map with cannon orientations.
    """

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
    for row in String:
        for char in row:
            if char == f"{count}":
                valuedMap += str(result[count - 1])
                count += 1
            else:
                valuedMap += char
        valuedMap += "\n"
    return valuedMap


def FindHorizontalT(String, row_index, col_index, tower_row, index=0):
    """
    Checks for horizontal obstacles (castle or crossfire) for a particular cannon.

    Args:
    - String: The map layout as a list of strings.
    - row_index: Index of the row in the map.
    - col_index: Index of the column in the map.
    - tower_row: Total number of towers in the map.
    - index: Index of the cannon (default: 0).

    Returns:
    - Boolean value representing constraints for the solver.
    """

    count = 0
    castle = False
    crossFire = False
    for char in String[row_index]:
        for f in range(1, TotalT + 1):
            if char == f"{f}" and int(char) != index:
                if col_index < tower_row:
                    i = count
                    while i != col_index:
                        if String[row_index][i] == "#":
                            castle = True
                        elif (
                            String[row_index][i].isdecimal()
                            and int(String[row_index][i]) != f
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
                    for k in range(count, col_index):
                        if String[row_index][k] == "#":
                            castle = True
                        elif (
                            String[row_index][k].isdecimal()
                            and int(String[row_index][k]) != f
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
        tower_row += 1
    tower_row = 0
    return False


def FindVerticalT(String, row_index, col_index, index=0):
    """
    Checks for vertical obstacles (castle or crossfire) for a particular cannon.

    Args:
    - String: The map layout as a list of strings.
    - row_index: Index of the row in the map.
    - col_index: Index of the column in the map.
    - total_towers: Total number of towers in the map.
    - index: Index of the cannon (default: 0).

    Returns:
    - Boolean value representing constraints for the solver.
    """
    
    castle = False
    crossFire = False
    for i in range(0, r):
        for l in range(1, TotalT + 1):
            if String[i][col_index] == f"{l}" and int(String[i][col_index]) != index:
                if row_index < i:
                    for k in range(row_index, i):
                        if String[k][col_index] == "#":
                            castle = True
                        elif (
                            (String[k][col_index].isdecimal())
                            and int(String[k][col_index]) != l
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
                    for k in range(i, row_index):
                        if String[k][col_index] == "#":
                            castle = True
                        elif (
                            (String[k][col_index].isdecimal())
                            and int(String[k][col_index]) != l
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


# Test Case 1
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

rows = input_string.strip().split("\n")
dimensions = list(map(int, rows[0].split()))
r, s = dimensions[0], dimensions[1]
map_data = rows[1:]

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

# Test Case 2
additional_input = """6 7
..nT...
Tnn..T.
..T....
n......
T....Tn
..n...."""

additional_rows = additional_input.strip().split("\n")
additional_dimensions = list(map(int, additional_rows[0].split()))
additional_r, additional_s = additional_dimensions[0], additional_dimensions[1]
additional_map_data = additional_rows[1:]

TestDimensions(additional_map_data, additional_r, additional_s)
TotalT, additional_map_data = ReplaceCountT(additional_map_data)

additional_map_data = additional_map_data.split("\n")
additional_map_data = additional_map_data[0:additional_r]

Solver = Solver()
VarHor = [Bool("t" + str(i) + "e") for i in range(1, TotalT + 1)]
VarVer = [Bool("t" + str(i) + "c") for i in range(1, TotalT + 1)]

CheckAttackers(additional_map_data)
CheckCrossFire(additional_map_data)

if Solver.check() == sat:
    m = Solver.model()
else:
    print("Unsatisfiable formula")

print(FormValuedMap(additional_map_data))
