import time
import random
import os
import pickle
from cube import Cube

MOVE_KEY = {0 : 'U', 1 : 'F', 2 : 'R', 'U' : 0, 'F' : 1, 'R' : 2}
ITERATOR_KEY = {0 : ' ', 1 : '2', 2 : '\'', ' ' : 0, '2' : 1, '\'' : 2}
SCRAMBLE_LENGTH = 15
DICT = {}
DICTPATH = 'src/dictionary.pickle'

def generateScramble(l):
    aux = ""
    moveSeed = random.randint(0,2)
    for i in range (l):
        moveSeed = (moveSeed + random.randint(0,1) + 1) % 3
        iteratorSeed = random.randint(0,2)
        aux = aux + MOVE_KEY[moveSeed] + ITERATOR_KEY[iteratorSeed] + " "
    return aux

def getScramble():
    if ask("Mode?\n" + "1 - Autogenerate\n" + "2 - Paste") == "2":
        scramble = ask("Input scramble")
    else:
        scramble = generateScramble(SCRAMBLE_LENGTH)
    print("scramble: " + ' '.join(scramble.split()))
    return scramble
    
def mix(cube, scramble):
    aux = scramble.split()
    for move in aux:
        if len(move) == 1:
            move += ' '
        for j in range(ITERATOR_KEY[move[1]] + 1):
            cube.turn(MOVE_KEY[move[0]])
                                
def solveDFS(state):
    def search(state, solution, depth, last, visited):
        aux = Cube()
        for i in range(3):
            if last != i:
                aux.setState(state)
                for j in range(3):
                    aux.turn(i)
                    if not tuple(aux.getState()) in visited:
                        if aux.isSolved():
                            print ("solution: " + ' '.join((solution + MOVE_KEY[i] + ITERATOR_KEY[j]).split()))
                            print ("visited states the last iteration: " + str(len(visited)))
                            return True
                        visited.add(tuple(aux.getState()))
                        if depth != 1:
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

def solveBFS(state, mode):
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
                        if mode == '1':
                            if aux.isSolved():
                                print ("solution: " + ' '.join((auxState[0] + MOVE_KEY[j] + ITERATOR_KEY[k]).split()))
                                print ("visited states: " + str(len(visited)))
                                return
                            if not tuple(aux.getState()) in visited:
                                visited.add(tuple(aux.getState()))
                                if depth < 9 or (depth == 9 and aux.hasAtLeast2AdjacentPiecesSolved()) or (depth == 10 and aux.hasAtLeast4AdjacentPiecesSolved()):
                                    next.append([auxState[0] + MOVE_KEY[j] + ITERATOR_KEY[k] + " ", aux.getState()])
                        else:
                            if not tuple(aux.getState()) in DICT:
                                DICT[tuple(aux.getState())]= auxState[0] + MOVE_KEY[j] + ITERATOR_KEY[k] + " "
                                next.append([auxState[0] + MOVE_KEY[j] + ITERATOR_KEY[k] + " ", aux.getState()])

def solveDirect(state):
    global DICT
    def inverseSequence(sequence):
        inverses = {"U": "U'", "U'": "U", "U2" : "U2", "F": "F'", "F'": "F", "F2" : "F2", "R": "R'", "R'": "R", "R2" : "R2"}
        moves = sequence.split()
        return ' '.join([inverses[move] for move in reversed(moves)])
    if len(DICT) == 0:
        if not os.path.exists(DICTPATH):
            print("Filling dictionary")
            solveBFS(Cube().getSolvedState(), '2')
            print("Saving dictionary to " + DICTPATH)
            with open(DICTPATH, 'wb') as f:
                pickle.dump(DICT, f)
        else:
            print("Filling dictionary from " + DICTPATH)
            with open(DICTPATH, 'rb') as f:
                DICT = pickle.load(f)
    print("solution: " + inverseSequence(DICT[tuple(state)]))

def solve(state):
    o = ask("Mode?\n" + "1 - Direct\n" + "2 - BFS\n" + "3 - DFS")
    sTime = time.time()
    if o == '2':
        solveBFS(state, '1')
    elif o == '3':
        solveDFS(state)
    else:
        solveDirect(state)
    print("Time elapsed: {:.3f} seconds".format(time.time()-sTime))

def ask (s):
    print(s)
    return input()

if __name__ == '__main__':
    o = 'Y'
    while o != 'n':
        cube = Cube()
        scramble = getScramble()
        mix (cube, scramble)
        solve(cube.getState())
        o = ask("Again?  [Y/n]")