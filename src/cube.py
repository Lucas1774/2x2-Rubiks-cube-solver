SOLVED_STATE = (0, 3, 6, 9, 12, 15, 18, 21)
STICKER_FIXER = {}


def fillFixer():
    def stickerFixer(piece, rotation):
        if piece % 3 == 0:
            return piece + rotation
        elif piece % 3 == 1:
            return piece + 1 if rotation == 1 else piece - 1
        else:
            return piece - 2 if rotation == 1 else piece - 1

    for i in range(24):
        for j in range(1, 3):
            STICKER_FIXER[(i, j)] = stickerFixer(i, j)


class Cube:
    def __init__(self):
        self.state = SOLVED_STATE

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = [e for e in state]

    def getSolvedState(self):
        return SOLVED_STATE

    def isSolved(self):
        return self.state == list(SOLVED_STATE)

    def turn(self, layer):
        aux = [e for e in self.state]
        if layer == 0:
            aux[0] = self.state[3]
            aux[1] = self.state[0]
            aux[2] = self.state[1]
            aux[3] = self.state[2]
        elif layer == 1:
            aux[0] = STICKER_FIXER[self.state[1], 2]
            aux[4] = STICKER_FIXER[self.state[0], 1]
            aux[7] = STICKER_FIXER[self.state[4], 2]
            aux[1] = STICKER_FIXER[self.state[7], 1]
        else:
            aux[0] = STICKER_FIXER[self.state[4], 1]
            aux[3] = STICKER_FIXER[self.state[0], 2]
            aux[5] = STICKER_FIXER[self.state[3], 1]
            aux[4] = STICKER_FIXER[self.state[5], 2]
        self.state = [e for e in aux]

    # The next are a good enough approach to "can be solved in 1 / 2 moves"
    def hasAtLeast4AdjacentPiecesSolved(self):
        if self.state[4] == 12 and self.state[5] == 15 and self.state[7] == 21:
            return True, "D"
        if self.state[2] == 6 and self.state[3] == 9 and self.state[5] == 15:
            return True, "B"
        if self.state[1] == 3 and self.state[2] == 6 and self.state[7] == 21:
            return True, "L"
        return False

    def hasAtLeast2AdjacentPiecesSolved(self):
        if self.state[5] == 15:
            return True, "DBR"
        if self.state[2] == 6:
            return True, "UBL"
        if self.state[7] == 21:
            return True, "DFL"


fillFixer()
