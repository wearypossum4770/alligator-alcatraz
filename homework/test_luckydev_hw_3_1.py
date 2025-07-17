import pytest
from luckydev_hw_3_1 import calculate_wrapping_paper

@pytest.mark.parametrize("dimensions, expected", (
    ("3x5x6", "You will need 141cm of wrapping paper"),
    ("10x20x15", "You will need 1450cm of wrapping paper"),
))
def test_calculate_wrapping_paper(dimensions: str, expected: str):
    assert calculate_wrapping_paper(dimensions) == expected