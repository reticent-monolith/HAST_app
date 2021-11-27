import csv
import pprint

def lPad(n: int) -> list[str]:
    return (n*'<60,').split(',')[:-1]

def hPad(n: int) -> list[str]:
    return (n*'>140,').split(',')[:-1]

def parseToTuple(string: str) -> tuple[int, int]:
    string = string.rstrip(')').lstrip('(')
    lower, upper = tuple(string.split("), ("))
    lower = tuple([int(n) for n in lower.split(", ")])  # I wish you could pass by reference to loops...
    upper = tuple([int(n) for n in upper.split(", ")])
    output = ((lower[0], lower[1]),(upper[0], upper[1]))
    return output


with open("./HAST_MATRIX.csv") as file:
    r = csv.DictReader(file)
    standardizedScoreMatrix = {parseToTuple(k):[] for k in r.fieldnames}
    for row in r:
        for k,v in row.items():
            standardizedScoreMatrix[parseToTuple(k)].append(v)

spellingAge = [  # Might need a more complex structure, can't remember the sheet...
    (5, 0),
]

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

def getSpellingAge(mark: int) -> tuple[int, int]:
    return (8, 5)