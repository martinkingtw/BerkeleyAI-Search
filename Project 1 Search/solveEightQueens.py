import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if i == 100 or newNumberOfAttacks == 0:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray

    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999.
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks,
        the Column and Row of the new queen
        For exmaple:
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        #util.raiseNotDefined()
        squareArray = self.squareArray
        formerNumberOfAttacks = self.getNumberOfAttacks()
        if formerNumberOfAttacks == 0:
            return (self, formerNumberOfAttacks, -1, -1)
        costBoard = self.getCostBoard()
        minNumberOfAttacks = min([costBoard.squareArray[r][c] for r in range(0, 8) for c in range(0, 8)])
        candidates = [(r, c) for r in range(0, 8) for c in range(0, 8) if costBoard.squareArray[r][c] == minNumberOfAttacks]
        if minNumberOfAttacks <= formerNumberOfAttacks:
            newRow, newCol = random.choice(candidates)
            copyBoard = [row[:] for row in squareArray]
            betterBoard = Board(copyBoard)
            oldRow = [r for r in range(0, 8) if squareArray[r][newCol] == 1][0]
            betterBoard.squareArray[oldRow][newCol] = 0
            betterBoard.squareArray[newRow][newCol] = 1
            return (betterBoard, minNumberOfAttacks, newRow, newCol)
        else:
            return (self, formerNumberOfAttacks, -1, -1)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        #util.raiseNotDefined()
        squareArray = self.squareArray
        ans = 0
        for i in range(8):
            num = 0
            for j in range(8):
                if squareArray[i][j] == 1:
                    num += 1
            ans += (num*(num-1)//2)
        for i in range(8):
            num = 0
            for j in range(i, 8):
                if squareArray[j-i][7-j] == 1:
                    num += 1
            ans += (num*(num-1)//2)
        for i in range(1, 8):
            num = 0
            for j in range(i, 8):
                if squareArray[j][7-j+i] == 1:
                    num += 1
            ans += (num*(num-1)//2)
        for i in range(8):
            num = 0
            for j in range(i, 8):
                if squareArray[j-i][j] == 1:
                    num += 1
            ans += (num*(num-1)//2)
        for i in range(1, 8):
            num = 0
            for j in range(i, 8):
                if squareArray[j][j-i] == 1:
                    num += 1
            ans += (num*(num-1)//2)
        return ans


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
