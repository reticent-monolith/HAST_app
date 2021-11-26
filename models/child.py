import datetime as dt

class Child:
    def __init__(
            self, 
            firstNames: str, 
            lastName: str, 
            dob: str, 
            score1: str=None, 
            spellingAge: str=None, 
            _id: int=None, 
        ):
        self._id: int = _id
        self.dob: str = dob
        self.firstNames: str = firstNames
        self.lastName: str = lastName
        self.score1: str = score1
        self.age: tuple[int, int] = self.getAge(dob)
        self.spellingAge: str = spellingAge

    def getAge(self, dob: str) -> tuple[int,int]:
        today = dt.date.today()
        dob = dt.date.fromisoformat(dob)
        years = today.year - dob.year
        months = today.month - dob.month
        if today.day < dob.day:
            months -= 1
        if months < 0:
            years -= 1
            months = 12 + months
        return (years, months)

    
