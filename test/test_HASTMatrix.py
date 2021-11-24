import pytest
from models.hastmatrix import HASTMatrix
from models.child import Child

hm = HASTMatrix()

def test_correctInput():
    child = Child([""], "", "2015-06-07")
    expected = "107" 
    actual = hm.getScore(child.age, 23)
    assert actual == expected