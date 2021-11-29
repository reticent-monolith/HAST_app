import csv
import pprint

def lPad(n: int) -> list[str]:
    return (n*'<60,').split(',')[:-1]

def hPad(n: int) -> list[str]:
    return (n*'>140,').split(',')[:-1]

def parseToTuple(string: str) -> tuple[int, int]:
    """Takes a string rep of an int tuple - (<int>, <int>) - and returns a tuple."""
    print(string)
    for ch in '(', ')', ' ':
        string = string.replace(ch, '')
    string = string.split(',')
    print(string)
    return (int(string[0]),int(string[1]))

def parseToDoubleTuple(string: str) -> tuple[tuple[int, int], tuple[int, int]]:
    for ch in '(',')',' ':
        string = string.replace(ch, '')
    string = string.split(',')
    return ((int(string[0]),int(string[1]))),(int(string[2]),int(string[3]))


with open("./HAST_MATRIX.csv") as file:
    r = csv.DictReader(file)
    standardizedScoreMatrix = {parseToDoubleTuple(k):[] for k in r.fieldnames}
    for row in r:
        for k,v in row.items():
            standardizedScoreMatrix[parseToDoubleTuple(k)].append(v)

with open("./HAST_AGES.csv") as file:
    spellingAge = []
    for line in file.readlines():
        line = line.strip('\n').split(',')
        spellingAge.append(
            (int(line[0]), int(line[1]))
        )
    
def getSpellingAge(mark: int) -> tuple[int, int]:
    if mark < 0:
        raise Exception(f"[{mark}] is an invalid mark for the test")
    try:
        age= spellingAge[mark]
        return age
    except IndexError:
        raise Exception(f"[{mark}] is an invalid mark for the test")

def getScore(age: tuple[int, int], mark: int) -> str:
    """Age is a tuple of the child's age (years (5-59),0-indexed months).
    Score is the score from the test.
    Returns the string score from the matrix, from '<60' to '>140'."""
    # find the correct key in the scores dictionary
    if mark < 0:
        raise Exception(f"[{mark}] is an invalid mark for the test")
    scores = None
    found = False
    for ageKey, scoresList in standardizedScoreMatrix.items():
        lower, upper = ageKey
        if lower[0] == age[0] and age[1] in range(lower[1], upper[1]+1):
            scores = scoresList
            break
    try:
        score = str(scores[mark])
        return score 
    except IndexError:
        raise Exception(f"[{mark}] is an invalid mark for the test")
