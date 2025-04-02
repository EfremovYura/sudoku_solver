import pytest
from solution import Solution

solution = Solution()

test_lines = [
    ([['3', '5', '7', '8', '9'], ['3', '5'], '7', '9', '8', '6', '2', '4', '1'],
     [['3', '5'], ['3', '5'], '7', '9', '8', '6', '2', '4', '1'], True),
    (['9', ['1', '4', '5', '7', '9'], ['1', '5'], '8', '6', '3', ['1', '4', '7'], '2', ['4', '5']],
     ['9', ['1', '4', '5', '7'], ['1', '5'], '8', '6', '3', ['1', '4', '7'], '2', ['4', '5']], True),
    ([['3', '5'], ['3', '5'], '7', '9', '8', '6', '2', '4', '1'],
     [['3', '5'], ['3', '5'], '7', '9', '8', '6', '2', '4', '1'], False)
]


@pytest.mark.parametrize('check_line, result_line, is_updated', test_lines)
def test__remove_known_values_from_line(check_line, result_line, is_updated):
    updated = solution._remove_known_values_from_line(check_line)
    assert check_line == result_line
    assert updated == is_updated


test_lists = [
    ([['1', '2', '3', '4', '5', '6', '7', '8', ['7', '8', '9']]],
     [['1', '2', '3', '4', '5', '6', '7', '8', ['9']]], True),
    ([['1', '2', '3', '4', '5', '6', '7', '8', ['9']]],
     [['1', '2', '3', '4', '5', '6', '7', '8', ['9']]], False),
]


@pytest.mark.parametrize('check, result, is_updated', test_lists)
def test_remove_known_values_from_hints(check, result, is_updated):
    solution.process_list = check
    updated = solution.remove_known_values_from_hints(check)
    assert check == result
    assert updated == is_updated
