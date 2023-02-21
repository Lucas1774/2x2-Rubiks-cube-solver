import time
import random
from cube import Cube

MOVE_KEY = {0 : 'U', 1 : 'F', 2 : 'R', 'U' : 0, 'F' : 1, 'R' : 2}
ITERATOR_KEY = {0 : ' ', 1 : '2', 2 : '\'', ' ' : 0, '2' : 1, '\'' : 2}
SCRAMBLE_LENGTH = 15

def generateScramble(l):
    aux = ""
    moveSeed = random.randint(0,2)
    for i in range (l):
        moveSeed = (moveSeed + random.randint(0,1) + 1) % 3
        iteratorSeed = random.randint(0,2)
        aux = aux + MOVE_KEY[moveSeed] + ITERATOR_KEY[iteratorSeed] + " "
    return aux

def mix(cube, scramble):
    for i in range(SCRAMBLE_LENGTH):
        move = (scramble[3 * i : 3 * i + 2])
        for j in range(ITERATOR_KEY[move[1]] + 1):
            cube.turn(MOVE_KEY[move[0]])

def solveBFS(state):
    visited = set(tuple(state))
    aux = Cube()
    next = [("", state)]
    for depth in range(1, 12):
        print("depth: " + str(depth))
        current = list(next)
        next = list([])
        for i in range(len(current)):
            auxState = current[i]
            last = MOVE_KEY[auxState[0][-3]] if auxState[0] else -1
            for j in range(3):
                if last != j:
                    aux.setState(auxState[1])
                    for k in range(3):
                        aux.turn(j)
                        if aux.isSolved():
                            print ("solution: " + auxState[0] + MOVE_KEY[j] + ITERATOR_KEY[k])
                            print ("visited states: " + str(len(visited)))
                            return
                        if not tuple(aux.getState()) in visited:
                            visited.add(tuple(aux.getState()))
                            next.append([auxState[0] + MOVE_KEY[j] + ITERATOR_KEY[k] + " ", aux.getState()])

def solveIDS(state):
    def search(state, solution, depth, last, visited):
        aux = Cube()
        for i in range(3):
            if last != i:
                aux.setState(state)
                for j in range(3):
                    aux.turn(i)
                    if not tuple(aux.getState()) in visited:
                        if aux.isSolved():
                            print ("solution: " + solution + MOVE_KEY[i] + ITERATOR_KEY[j])
                            print ("visited states the last iteration: " + str(len(visited)))
                            return True
                        visited.add(tuple(aux.getState()))
                        if depth != 0:
                            if search(aux.getState(), solution + MOVE_KEY[i] + ITERATOR_KEY[j]+ " ", depth - 1, i, visited):
                                return True
        return False
    
    found = False
    depth = 1
    while not found:
        visited = set(tuple(state))
        print("depth: " + str(depth))
        found = search(state, "", depth, -1, visited)
        depth += 1

def solve(state):
    if ask("Mode?\n" + "1 - DFS\n" + "2 - BFS") == "2":
        sTime = time.time()
        solveBFS(state)
    else:
        sTime = time.time()
        solveIDS(state)
    print("Time elapsed: {:.2f} seconds".format(time.time()-sTime))

def getScramble():
    if ask("Mode?\n" + "1 - Autogenerate\n" + "2 - Paste") == "2":
        return ask("Input scramble")
    else:
        return generateScramble(SCRAMBLE_LENGTH)

def ask (s):
    print(s)
    return input()

if __name__ == '__main__':
    cube = Cube()
    scramble = getScramble()
    print("scramble: " + scramble)
    mix (cube, scramble)
    solve(cube.getState())