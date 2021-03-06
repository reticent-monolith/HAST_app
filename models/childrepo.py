import sqlite3
from contextlib import closing
from models.child import Child

class ChildRepo:
    def __init__(self):
        self.conn = sqlite3.connect("./child.db")
        self._createTable()

# Public:
    def add(self, child: Child):
        childDict = self._serialize(child)
        with closing(self.conn.cursor()) as c:
            c.execute(
                "INSERT INTO child (firstNames, lastName, dateOfBirth) VALUES (?, ?, ?);",
                (childDict["firstNames"], childDict["lastName"], childDict["dob"])
            )
            self._commit()

    def update(self, id: int, child: Child):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "UPDATE child SET firstNames = ?, lastName = ?, dateOfBirth = ?, score1 = ?, spellingAge = ? WHERE id = ?",
                (
                    child.firstNames,
                    child.lastName, 
                    child.dob,
                    child.score1,
                    str(child.spellingAge) if child.spellingAge else None,
                    id
                )
            )
            self._commit()

    def delete(self, id):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "DELETE FROM child WHERE id = ?", (id,)
            )
        self._commit()

    def getAll(self) -> list[Child]:
        with closing(self.conn.cursor()) as c:
            children = c.execute(
                "SELECT * FROM child"
            ).fetchall()
        children = [self._deserialize(child) for child in children]
        return children

    def get(self, id: int) -> Child:
        with closing(self.conn.cursor()) as c:
            child = c.execute(
                "SELECT * FROM child WHERE id = ?",
                (id,)
            ).fetchone()
        return self._deserialize(child)

# Private:
    def _createTable(self):
        with closing(self.conn.cursor()) as c:
            c = self.conn.cursor()
            c.execute(
                "CREATE TABLE IF NOT EXISTS child (id INTEGER PRIMARY KEY, firstNames TEXT, lastName TEXT, dateOfBirth TEXT, score1 TEXT, spellingAge TEXT);"
            )
            self._commit()

    def _deserialize(self, data: tuple) -> Child:
        args = {
            "firstNames": data[1],
            "lastName": data[2],
            "dob": data[3],
            "_id": data[0],
            "score1": data[4],
            "spellingAge": data[5]
        }
        if data[5] != None:
            args["spellingAge"] = (
                int(data[5].strip('(').strip(')').split(',')[0].strip()),
                int(data[5].strip('(').strip(')').split(',')[1].strip()),
            )
        # Probably need to do something with the scores in here...
        child = Child(**args)
        return child
    
    def _serialize(self, child: Child) -> dict:
        serialized = {
            "firstNames": child.firstNames,
            "lastName": child.lastName,
            "dob": child.dob
        }
        return serialized

    def _commit(self):
        self.conn.commit()