import datetime as dt

class Child:
    def __init__(
            self, 
            firstNames: list[str], 
            lastName: str, 
            dob: str, 
            score1: int=None, 
            score2: int=None, 
            _id: int=None, 
        ):
        self._id = _id
        self.dob = dob
        self.firstNames = firstNames
        self.lastName = lastName
        self.score1 = score1
        self.score2 = score2
        self.age = self.getAge(dob)

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

    
