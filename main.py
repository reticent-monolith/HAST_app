from src.hastmatrix import HASTMatrix
from src.child import Child

m = HASTMatrix()

while True:
    dob = input("Date of birth: ")
    try:
        c = Child(["test"], "child", dob)
    except ValueError as e:
        print("Bad date!")
        continue
    mark = int(input("Mark: "))
    if mark > 65 or mark < 0:
        print("Mark out of range (0 to 65)")
        continue
    print("Result: " + m.getScore(c.age, mark))
    print()
