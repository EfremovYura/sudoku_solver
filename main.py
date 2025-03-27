import sys
from collections import Counter
from itertools import chain, combinations
from operator import is_not


class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        """
        Modify board in-place.
        """
        self.add_hints(board)
        process_list = self.make_process_list(board)

        self.remove_known_values_from_hints(process_list)
        self.write_known_value_from_hints(process_list)
        self.check_unique_value_in_hints(process_list)
        self.remove_unique_pair_in_hints(process_list)

    def is_solved(self, board: list[list]) -> bool:
        filled_lines = [all(map(lambda x: isinstance(x, str) and x.isdigit(), arr)) for arr in board]

        return all(filled_lines)

    def is_solved_correctly(self, board: list[list]):
        for i, line in enumerate(board):
            if set('123456789').difference(set(line)):
                print(f'wrong line {i}: {line}')
                return False
        return True

    def add_hints(self, board: list[list]):
        """Replace (in-place) unknown values with hints (list of possible values)"""
        for line in board:
            for i in range(9):
                line[i] = list(map(str, range(1, 10))) if line[i] == '.' else line[i]

    def _is_hint(self, hint: list | str) -> bool:
        return isinstance(hint, list)

    def _remove_known_values_from_line(self, line: list[list | str]) -> None:
        for elem in line:
            if not self._is_hint(elem):
                continue

            known_values = [value for value in line if not self._is_hint(value)]

            for value in known_values:
                if value in elem:
                    elem.remove(value)

    def _write_known_value_from_hints_in_line(self, line: list[list | str]) -> None:
        for i, elem in enumerate(line):

            if not self._is_hint(elem):
                continue

            if len(elem) == 1:
                line[i] = elem[0]

    def _check_unique_value_in_hints_in_line(self, line: list[list | str]) -> None:
        for i, elem in enumerate(line):
            if not self._is_hint(elem):
                continue

            other_hints = [hint for hint in line if self._is_hint(hint) and hint is not elem]

            for n in elem:
                if all([(n not in other_hint) for other_hint in other_hints]):
                    line[i] = n

    def _remove_unique_pair_in_hints_in_line(self, line: list[list | str]):
        pair_hints = [hint for hint in line if self._is_hint(hint) and len(hint) == 2]

        for pair in pair_hints:
            pair_counter = 0
            for check_hint in pair_hints:
                if pair == check_hint:
                    pair_counter += 1

            if pair_counter == 2:
                for line_elem in line:
                    if not self._is_hint(line_elem):
                        continue

                    if line_elem == pair:
                        continue

                    for pair_elem in pair:
                        if pair_elem in line_elem:
                            line_elem.remove(pair_elem)

    def remove_known_values_from_hints(self, process_list: list[list]):
        for line in process_list:
            self._remove_known_values_from_line(line)

    def write_known_value_from_hints(self, process_list: list[list]):
        for line in process_list:
            self._write_known_value_from_hints_in_line(line)

    def check_unique_value_in_hints(self, process_list: list[list]):
        for line in process_list:
            self._check_unique_value_in_hints_in_line(line)

    def remove_unique_pair_in_hints(self, process_list: list[list]):
        for line in process_list:
            self._remove_unique_pair_in_hints_in_line(line)

    def make_process_list(self, board: list[list]) -> list[list]:
        process_list = []

        # add lines
        for line in board:
            process_list.append(line)

        # add columns
        for i in range(9):
            process_list.append([board[j][i] for j in range(9)])

        # add boxes
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box_part1 = board[i][j:j + 3]
                box_part2 = board[i + 1][j:j + 3]
                box_part3 = board[i + 2][j:j + 3]

                process_list.append(box_part1 + box_part2 + box_part3)
        return process_list

    def get_sub_box_indexes(self, elem_indx: int) -> list[int]:
        if elem_indx in range(0, 3):
            box_indexes = [0, 1, 2]
        elif elem_indx in range(3, 6):
            box_indexes = [3, 4, 5]
        elif elem_indx in range(6, 9):
            box_indexes = [6, 7, 8]

        return box_indexes


def main(board: list[list]):
    """"""

    solution = Solution()
    solution.solveSudoku(board)

    # solution.solveSudoku(board)
    print(solution.is_solved(board))
    if solution.is_solved(board):
        print(solution.is_solved_correctly(board))
    print(*board, sep='\n')


if __name__ == '__main__':
    board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
             ["6", ".", ".", "1", "9", "5", ".", ".", "."],
             [".", "9", "8", ".", ".", ".", ".", "6", "."],
             ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
             ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
             ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
             [".", "6", ".", ".", ".", ".", "2", "8", "."],
             [".", ".", ".", "4", "1", "9", ".", ".", "5"],
             [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

    # board = [["3", ".", ".", ".", ".", ".", ".", ".", "9"],
    #          [".", ".", ".", ".", "7", ".", "1", ".", "2"],
    #          [".", ".", ".", ".", ".", "9", "5", ".", "."],
    #          [".", "7", ".", ".", "5", ".", ".", ".", "."],
    #          ["1", ".", ".", "4", ".", ".", "6", "8", "."],
    #          [".", ".", "6", ".", ".", ".", ".", ".", "."],
    #          ["7", "1", ".", ".", "9", ".", ".", ".", "5"],
    #          [".", ".", ".", ".", ".", "3", "8", ".", "."],
    #          ["4", ".", ".", ".", ".", ".", ".", "2", "."]]
    #
    # board = [["9", ".", ".", "7", ".", "6", ".", ".", "."],
    #          [".", "1", ".", "4", "9", ".", ".", "2", "."],
    #          [".", "5", ".", "3", ".", ".", "9", ".", "."],
    #          [".", "7", ".", "1", "5", "4", ".", ".", "9"],
    #          ["4", ".", ".", ".", ".", ".", ".", "8", "1"],
    #          ["5", "6", ".", ".", ".", ".", ".", "7", "."],
    #          [".", "4", ".", ".", "6", ".", ".", ".", "."],
    #          [".", ".", "2", "5", ".", ".", ".", ".", "4"],
    #          [".", "9", "6", ".", ".", "2", ".", "5", "."]]
    #
    # board = [[".", ".", "9", "7", "4", "8", ".", ".", "."],
    #          ["7", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", "2", ".", "1", ".", "9", ".", ".", "."],
    #          [".", ".", "7", ".", ".", ".", "2", "4", "."],
    #          [".", "6", "4", ".", "1", ".", "5", "9", "."],
    #          [".", "9", "8", ".", ".", ".", "3", ".", "."],
    #          [".", ".", ".", "8", ".", "3", ".", "2", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", "6"],
    #          [".", ".", ".", "2", "7", "5", "9", ".", "."]]
    main(board)
