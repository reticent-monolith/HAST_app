from src.hastmatrix import HASTMatrix
from src.child import Child

m = HASTMatrix()
c = Child(["Ben"], "Jones", "2011-05-23")
print(c.age)
print(m.getScore(c.age, 54 ))

# while True:
#     years = input("Years: ")
#     months = input("Months: ")
#     mark = input("Mark: ")
#     print("Result: " + m.getScore((int(years), int(months)), int(mark)))
#     print()
