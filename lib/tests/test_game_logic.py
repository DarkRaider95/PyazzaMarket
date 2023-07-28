from lib.gameLogic import *

def test_roll():
    for _ in range(10):
        dice = roll()
        assert len(dice) == 2
        assert 1 <= dice[0] <= 6
        assert 1 <= dice[1] <= 6

def test_is_double():
    assert is_double((1, 1)) is True
    assert is_double((2, 2)) is True
    assert is_double((3, 4)) is False
    assert is_double((6, 6)) is True
    assert is_double((5, 6)) is False