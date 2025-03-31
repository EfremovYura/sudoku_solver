__version__ = '0.1'

from enum import unique
from itertools import combinations, groupby
from utils import show_details


class Solution:
    @show_details
    def solve_sudoku(self, board: list[list[str]]) -> list:
        """
        Modify board in-place.
        """
        self.add_hints(board)
        process_list = self.make_process_list(board)

        self.remove_known_values_from_hints(process_list)
        self.write_known_value_from_hints(process_list)

        self.check_unique_value_in_hints(process_list)
        self.remove_known_values_from_hints(process_list)
        self.write_known_value_from_hints(process_list)

        self.remove_unique_pair_in_hints(process_list)
        self.remove_known_values_from_hints(process_list)
        self.write_known_value_from_hints(process_list)

        self.remove_except_unique_pair_values_in_hints(process_list)
        self.remove_known_values_from_hints(process_list)
        self.write_known_value_from_hints(process_list)
        return board

    def is_solved(self, board: list[list]) -> bool:
        filled_lines = [all(map(lambda x: isinstance(x, str) and x.isdigit(), arr)) for arr in board]

        return all(filled_lines)

    @show_details
    def is_solved_correctly(self, board: list[list]) -> bool:
        for i, line in enumerate(board):
            if set('123456789').difference(set(line)):
                print(f'wrong line {i}: {line}')
                return False
        return True

    @show_details
    def add_hints(self, board: list[list]) -> list:
        """Replace (in-place) unknown values with hints (list of possible values)"""
        for line in board:
            for i in range(9):
                line[i] = list(map(str, range(1, 10))) if line[i] == '.' else line[i]
        return board

    def _is_hint(self, hint: list | str) -> bool:
        return isinstance(hint, list)

    @show_details
    def _remove_known_values_from_line(self, line: list[list | str]) -> list:
        for elem in line:
            if not self._is_hint(elem):
                continue

            known_values = [value for value in line if not self._is_hint(value)]

            for value in known_values:
                if value in elem:
                    elem.remove(value)
        return line

    @show_details
    def _write_known_value_from_hints_in_line(self, line: list[list | str]) -> list:
        for i, elem in enumerate(line):

            if not self._is_hint(elem):
                continue

            if len(elem) == 1:
                line[i] = elem[0]

        return line

    @show_details
    def _check_unique_value_in_hints_in_line(self, line: list[list | str]) -> list:
        for i, elem in enumerate(line):
            if not self._is_hint(elem):
                continue

            other_hints = [hint for hint in line if self._is_hint(hint) and hint is not elem]

            for n in elem:
                if all([(n not in other_hint) for other_hint in other_hints]):
                    line[i] = n
        return line

    @show_details
    def _remove_unique_pair_in_hints_in_line(self, line: list[list | str]) -> list:
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
        return line

    @show_details
    def _remove_except_unique_pair_values_in_hints_in_line(self, line: list[list | str]) -> list:
        hints: list[list] = [hint for hint in line if self._is_hint(hint)]

        posibility_indexes = {n: [] for n in '123456789'}
        for posibility in posibility_indexes:
            for i, hint in enumerate(hints):
                if posibility in hint:
                    posibility_indexes[posibility].append(i)

        pos_indexes_2 = [{pos: tuple(pos_indexes)} for pos, pos_indexes in posibility_indexes.items() if
                         len(pos_indexes) == 2]

        index_pos = {}
        for d in pos_indexes_2:
            for n, indexes in d.items():
                if not index_pos.get(indexes):
                    index_pos[indexes] = [n]
                else:
                    index_pos[indexes].append(n)

        for index_pair, value_pair in index_pos.items():
            if len(value_pair) != 2:
                continue
            for i in index_pair:
                for n in hints[i]:
                    if n in value_pair:
                        continue
                    hints[i].remove(n)
        return line

    @show_details
    def remove_known_values_from_hints(self, process_list: list[list]) -> list:
        for line in process_list:
            self._remove_known_values_from_line(line)
        return process_list

    @show_details
    def write_known_value_from_hints(self, process_list: list[list]) -> list:
        for line in process_list:
            self._write_known_value_from_hints_in_line(line)
        return process_list

    @show_details
    def check_unique_value_in_hints(self, process_list: list[list]) -> list:
        for line in process_list:
            self._check_unique_value_in_hints_in_line(line)
        return process_list

    @show_details
    def remove_unique_pair_in_hints(self, process_list: list[list]) -> list:
        for line in process_list:
            self._remove_unique_pair_in_hints_in_line(line)
        return process_list

    @show_details
    def remove_except_unique_pair_values_in_hints(self, process_list: list[list]) -> list:
        for line in process_list:
            self._remove_except_unique_pair_values_in_hints_in_line(line)
        return process_list

    @show_details
    def make_process_list(self, board: list[list]) -> list:
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
