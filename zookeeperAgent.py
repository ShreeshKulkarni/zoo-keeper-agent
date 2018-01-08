import sys
from time import time
from copy import deepcopy
from random import randint, uniform
from math import exp, log

############################### Simulated Annealing code begin ###############################

def SAgetNext(current):
    '''Return a random next board.'''

    next = deepcopy(current)

    # Remove a random lizard
    idx = randint(0, len(next.lizardCells) - 1)
    i, j = next.lizardCells[idx]
    next.data[i][j] = 0
    next.emptyCells.append(next.lizardCells[idx])
    del next.lizardCells[idx]

    # Place it in a different empty position
    idx = randint(0, len(next.emptyCells) - 2)
    i, j = next.emptyCells[idx]
    next.data[i][j] = 1
    next.lizardCells.append(next.emptyCells[idx])
    del next.emptyCells[idx]
    
    # Find out conflicts in the new board
    next.numConflicts = getConflicts(next.data)

    return next


class SAnode:
    '''Define a node specific to Simulated Annealing.'''
    
    def __init__(self, data, numConflicts, emptyCells, lizardCells):
        self.data = data
        self.numConflicts = numConflicts
        self.emptyCells = emptyCells
        self.lizardCells = lizardCells


def getConflicts(matrix):
    '''Return number of conflicts with respect to lizard placements.'''
    
    count = 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                count += countConflicts(matrix, i, j)
    return count


def sa(matrix):
    '''Run Simulated Annealing on the given matrix.'''
    
    # Maintain lists to contain positions of empty cells, cells with lizards as tuples (i,j)
    emptyCells = []
    lizardCells = []
    placed = 0

    # place lizards randomly in valid positions
    for col in range(n):
        if placed < p:
            # store all empty cells
            emptyTemp = []
            for row in range(n):
                if matrix[row][col] == 0:
                    emptyTemp.append((row, col))
            # while empty cells exist on board
            while emptyTemp:
                idx = randint(0, len(emptyTemp)-1)
                i,j = emptyTemp[idx]
                if validCell(matrix, i, j):
                    # place a lizard
                    matrix[i][j] = 1
                    # update list of lizard positions
                    lizardCells.append(emptyTemp[idx])
                    placed += 1
                    break
                else:
                    # invalid cell, get rid of it
                    del emptyTemp[idx]

    # Lets add some more randomness - now in invalid positions - checking for random col in EACH row
    for i in range(n):
        if placed < p:
            emptyTemp = []
            for j in range(n):
                if matrix[i][j] == 0:
                    emptyTemp.append((i, j))
            if emptyTemp:
                idx = randint(0, len(emptyTemp)-1)
                i, j = emptyTemp[idx]
                matrix[i][j] = 1
                lizardCells.append(emptyTemp[idx])
                placed += 1

    if placed == 0: # all trees
        return False

    # find empty cells after placement
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                emptyCells.append((i, j))

    # You can only place lizards if there are enough spots
    if p > len(emptyCells)+len(lizardCells):
        return False

    # place remaining of p - placed lizards randomly
    for _ in range(p-placed):
        idx = randint(0, len(emptyCells)-1)
        i, j = emptyCells[idx]
        matrix[i][j] = 1
        lizardCells.append(emptyCells[idx])
        del emptyCells[idx]

    current = SAnode(matrix, getConflicts(matrix), emptyCells, lizardCells)
    # best case
    if current.numConflicts == 0:
        return current.data
    if len(current.emptyCells) == 0:    # when conflicts exist, and there is no empty cell to move to get a different config
        return False

    #next = SAnode(None, None, None, None)

    t = 1
    while True:
        t += 1
        # Temperature - initially high
        Temp = 5.0/log(t)

        # check timeout
        if (time()-start) > 300:
            return False

        next = SAgetNext(current)
        if next.numConflicts == 0:
            return next.data

        # change in entropy
        dE = next.numConflicts - current.numConflicts

        if dE < 0:  # accept next state
            current = deepcopy(next)
        elif dE > 0:
            prob = exp((-dE*1.0)/Temp)
            threshold = uniform(0, 1)

            if prob > threshold:
                # accepting with a probability
                current = deepcopy(next)


def countConflicts(matrix, row, col):
    '''Return number of lizard conflicts given a cell.'''
	
    count = 0
    # row left side
    for j in range(col - 1, -1, -1):
        if matrix[row][j] == 1:
            count += 1
            break
        elif matrix[row][j] == 2:
            break

    # row right side
    for j in range(col + 1, n):
        if matrix[row][j] == 1:
            count += 1
            break
        elif matrix[row][j] == 2:
            break

    # col upper side
    for i in range(row - 1, -1, -1):
        if matrix[i][col] == 1:
            count += 1
            break
        elif matrix[i][col] == 2:
            break

    # col downwards
    for i in range(row + 1, n):
        if matrix[i][col] == 1:
            count += 1
            break
        elif matrix[i][col] == 2:
            break

    # Upper diagonal on left side
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if matrix[i][j] == 1:
            count += 1
            break
        elif matrix[i][j] == 2:
            break

    # Upper diagonal on right side
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
        if matrix[i][j] == 1:
            count += 1
            break
        elif matrix[i][j] == 2:
            break

    # Lower diagonal on left side
    for i, j in zip(range(row + 1, n), range(col - 1, -1, -1)):
        if matrix[i][j] == 1:
            count += 1
            break
        elif matrix[i][j] == 2:
            break

    # Lower diagonal on right side
    for i, j in zip(range(row + 1, n), range(col + 1, n)):
        if matrix[i][j] == 1:
            count += 1
            break
        elif matrix[i][j] == 2:
            break

    return count

############################### Simulated Annealing code end ###############################

############################### Utilities begin ###########################################

def validCell(matrix, row, col):
    '''Check if lizard can be safely placed in the given cell'''

    if matrix[row][col] == 2:
        # tree already present
        return False

    # left side cells in same row
    for j in range(col, -1, -1):
        if matrix[row][j] == 1:
            return False
        if matrix[row][j] == 2:
            break

    # Upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if matrix[i][j] == 1:
            return False
        if matrix[i][j] == 2:
            break

    # Lower diagonal on left side
    for i, j in zip(range(row, n), range(col, -1, -1)):
        if matrix[i][j] == 1:
            return False
        if matrix[i][j] == 2:
            break

    return True


class config:
    def __init__(self, data, d, num):
        self.data = data
        self.level = d
        self.numLizards = num


def mark(matrix, row, col):
    '''Mark '3' in attacking positions of lizard at matrix[row][col]'''

    # row left side
    for j in range(col - 1, -1, -1):
        if matrix[row][j] == 0:
            matrix[row][j] = 3
        elif matrix[row][j] == 2:
            break

    # row right side
    for j in range(col + 1, n):
        if matrix[row][j] == 0:
            matrix[row][j] = 3
        elif matrix[row][j] == 2:
            break

    # col upper side
    for i in range(row - 1, -1, -1):
        if matrix[i][col] == 0:
            matrix[i][col] = 3
        elif matrix[i][col] == 2:
            break

    # col downwards
    for i in range(row + 1, n):
        if matrix[i][col] == 0:
            matrix[i][col] = 3
        elif matrix[i][col] == 2:
            break

    # Mark upper diagonal on left side
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if matrix[i][j] == 0:
            matrix[i][j] = 3
        elif matrix[i][j] == 2:
            break

    # Mark upper diagonal on right side
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
        if matrix[i][j] == 0:
            matrix[i][j] = 3
        elif matrix[i][j] == 2:
            break

    # Mark lower diagonal on left side
    for i, j in zip(range(row + 1, n), range(col - 1, -1, -1)):
        if matrix[i][j] == 0:
            matrix[i][j] = 3
        elif matrix[i][j] == 2:
            break

    # Mark lower diagonal on right side
    for i, j in zip(range(row + 1, n), range(col + 1, n)):
        if matrix[i][j] == 0:
            matrix[i][j] = 3
        elif matrix[i][j] == 2:
            break

############################### Utilities end ###############################

############################### BFS code begin ###############################

def pushAllConfigsBFS(conf):        # marking 3 implementation
    '''Push all possible lizard placements in next col.'''

    col = conf.level + 1

    for i in range(0, n):

        if conf.data[i][col] == 0:
            newData = deepcopy(conf.data)
            newData[i][col] = 1
            mark(newData, i, col)

            stack.append(config(newData, col, conf.numLizards+1))
            if stack[-1].numLizards == p:
                return stack[-1]
    return False


def BFStreeConfigs(conf):
    '''Push all possible lizard placements in next col for board with trees.'''

    for i in range(0, n):
        for j in range(0, n):
            if conf.data[i][j] == 0:
                newData = deepcopy(conf.data)
                newData[i][j] = 1
                mark(newData, i, j)

                stack.append(config(newData, None, conf.numLizards + 1))
                if stack[-1].numLizards == p:
                    return stack[-1]
    return False


def bfs():
    '''Run BFS.'''
	
    global stack
    while True:
        if (time()-start) > 300:
            return "FAIL"

        try:
            if stack[0].numLizards == p:
                return "OK"
        except IndexError:
            return "FAIL"

        if treeFound:
            optimalConf = BFStreeConfigs(stack[0])
        else:
            optimalConf = pushAllConfigsBFS(stack[0])

        if optimalConf:
            stack = [optimalConf] + stack
            return "OK"

        del stack[0]

############################### BFS code end ###############################

############################### DFS code begin ###############################

def pushAllConfigsDFS(conf):        # marking 3 implementation
    '''Push all possible lizard placements in next col.'''

    col = conf.level + 1

    count = 0
    for i in range(0, n):

        if conf.data[i][col] == 0:
            count += 1
            newData = deepcopy(conf.data)
            newData[i][col] = 1
            mark(newData, i, col)

            stack.append(config(newData, col, conf.numLizards+1))
    return count


def DFStreeConfigs(conf):
    '''Push all possible lizard placements in next col for board with trees.'''

    count = 0
    for i in range(0, n):
        for j in range(0, n):
            if conf.data[i][j] == 0:
                count += 1
                newData = deepcopy(conf.data)
                newData[i][j] = 1
                mark(newData, i, j)

                stack.append(config(newData, None, conf.numLizards + 1))
    return count


def dfs():
    '''Run DFS.'''

    while True:
        if (time()-start) > 300:
            return "FAIL"

        try:
            if stack[-1].numLizards == p:
                return "OK"
        except IndexError:
            return "FAIL"

        if treeFound:
            count = DFStreeConfigs(stack[-1])

            if count == 0:
                currentNumLizards = stack[-1].numLizards
                _ = stack.pop()

                try:
                    while stack[-1].numLizards < currentNumLizards:
                        currentNumLizards = stack[-1].numLizards
                        _ = stack.pop()

                except IndexError:
                    return "FAIL"

        else:
            count = pushAllConfigsDFS(stack[-1])

            if count == 0:
                currentLevel = stack[-1].level
                _ = stack.pop()

                try:
                    while stack[-1].level < currentLevel:
                        currentLevel = stack[-1].level
                        _ = stack.pop()

                except IndexError:
                    return "FAIL"

############################### DFS code end ###############################


if __name__ == '__main__':
    # global n, p, start, treeFound, stack
    start = time()
    treeFound = 0
    stack = []

    with open('input.txt', 'r') as f:
        alg = f.readline().strip()  # BFS, DFS or SA
        n = int(f.readline())    # n x n
        p = int(f.readline())    # lizards

        matrix = []
        for i in range(n):
            line = f.readline().strip()
            # matrix.append([int(x) for x in line])
            lst = []
            for x in line:
                x = int(x)
                lst.append(x)
                if x == 2:
                    treeFound += 1
            matrix.append(lst)

    print "Running ", alg, "..."

    # write default output
    with open("output.txt", 'w') as f:
        f.write("FAIL\n")

    if p == 0:  # no lizards to be placed
        with open("output.txt", 'w') as f:
            f.write("OK\n")
            for i in range(n):
                for j in range(n):
                    f.write(str(matrix[i][j]))
                f.write("\n")
            sys.exit()

    # Failure when trying to place more than n*n lizards on an nxn board
    if p > n*n:
        sys.exit()

    # In simple N-Queens case (without trees), a maximum of n lizards can be placed
    if not treeFound and p > n:
        sys.exit()

    # Failure when lizards to be placed are more than number of empty cells
    if treeFound and p > (n*n)-treeFound:
        sys.exit()

    if alg == "DFS":
        root = config(matrix, -1, 0)
        stack.append(root)

        if dfs() == "OK":
            with open("output.txt", 'w') as f:
                f.write("OK\n")
                for i in range(n):
                    for j in range(n):
                        # Reset unsafe cells
                        if stack[-1].data[i][j] == 3:
                            stack[-1].data[i][j] = 0
                        f.write(str(stack[-1].data[i][j]))
                    f.write("\n")

    elif alg == "BFS":
        root = config(matrix, -1, 0)
        stack.append(root)

        if bfs() == "OK":
            with open("output.txt", 'w') as f:
                f.write("OK\n")
                for i in range(n):
                    for j in range(n):
                        # Reset unsafe cells
                        if stack[0].data[i][j] == 3:
                            stack[0].data[i][j] = 0
                        f.write(str(stack[0].data[i][j]))
                    f.write("\n")

    elif alg == "SA":
        result = sa(matrix)
        if result:
            with open("output.txt", 'w') as f:
                f.write("OK\n")
                for i in range(n):
                    for j in range(n):
                        f.write(str(result[i][j]))
                    f.write("\n")

    # print "Total time",(time() - start) / 60.0
