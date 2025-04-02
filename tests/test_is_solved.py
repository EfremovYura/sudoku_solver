import pytest
from solution import Solution

solution = Solution()

test_data = [
    ([[['3'], ['5'], '7', '9', '8', '6', '2', '4', '1']], False),
    ([['3', '5', '7', '9', '8', '6', '2', '4', '1']], True),
    ([[['3'], ['5'], '7', '9', '8', '6', '2', '4', '1'],
      ['3', '5', '7', '9', '8', '6', '2', '4', '1']], False),
    ([['3', '5', '7', '9', '8', '6', '2', '4', '1'],
      ['3', '5', '7', '9', '8', '6', '2', '4', '1']], True),
]


@pytest.mark.parametrize('check, result', test_data)
def test_is_solved(check, result):
    assert solution.is_solved(check) == result
