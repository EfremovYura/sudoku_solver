__version__ = '0.1'

from copy import deepcopy


class SudokuSolved(Exception):
    pass


class SudokuFailed(Exception):
    pass


class SudokuNeedUpdate(Exception):
    pass


class SudokuTooLong(Exception):
    pass


class Solution:
    def __init__(self):
        self.process_list = []

    def solve_sudoku(self, board: list[list[str]], n_estimators: int = 100000) -> list:
        """
        Modify board in-place.
        """
        self.add_hints(board)
        self.process_list = self.make_process_list(board)

        i = 0
        while not self.is_solved(self.process_list):
            i += 1
            if i >= n_estimators:
                print('TooLong')
                raise SudokuTooLong(f'{n_estimators=} limit reached')
            print(i)

            try:
                self.process_without_gues(self.process_list)

                self.gues(self.process_list)

            except SudokuSolved as e:
                print('success')
                raise e
            except SudokuFailed as e:
                print(f'failed {e}')
                raise e
            except SudokuNeedUpdate:
                continue

        return board

    def check_state(self, process_list: list[list]) -> None | Exception:
        if err := self.contain_errors(process_list):
            raise SudokuFailed(f'errors in {err}')

        if self.is_solved(process_list) and self.is_solved_correctly(process_list):
            raise SudokuSolved

    def process_without_gues(self, process_list: list[list]) -> None:
        updated = True
        while updated:
            pipline = [
                self.remove_known_values_from_hints,
                self.write_known_value_from_hints,
                self.check_unique_value_in_hints,
                self.remove_unique_pair_in_hints,
                self.remove_except_unique_pair_values_in_hints
            ]
            for func in pipline:
                print(f'{func.__name__}')
                updated = func(process_list)
                if updated:
                    self.check_state(process_list)
                    break
            updated = any([func(process_list) for func in pipline])

    @staticmethod
    def is_solved(process_list: list[list]) -> bool:
        filled_lines = [all(map(lambda x: isinstance(x, str) and x.isdigit(), line)) for line in process_list]

        return all(filled_lines)

    def is_solved_correctly(self, process_list: list[list]) -> bool:
        if not self.is_solved(process_list):
            return False

        for i, line in enumerate(process_list):
            if set('123456789').difference(set(line)):
                print(f'wrong line {i}: {line}')
                return False
        return True

    def contain_errors(self, process_list: list[list]) -> list | bool:
        empty_hints = [[] in line for line in process_list]
        if any(empty_hints):
            return empty_hints

        for line in process_list:
            line_counter = {}
            for elem in line:
                if not self._is_hint(elem):
                    line_counter[elem] = line_counter.get(elem, 0) + 1
            if any([True for amount in line_counter.values() if amount > 1]):
                return line

        return False

    @staticmethod
    def add_hints(board: list[list]) -> list:
        """Replace (in-place) unknown values with hints (list of possible values)"""
        for line in board:
            for i in range(9):
                line[i] = list(map(str, range(1, 10))) if line[i] == '.' else line[i]
        return board

    @staticmethod
    def _is_hint(hint: list | str) -> bool:
        return isinstance(hint, list)

    def _remove_known_values_from_line(self, line: list[list | str]) -> bool:
        updated = False
        for elem in line:
            if not self._is_hint(elem):
                continue

            known_values = [value for value in line if not self._is_hint(value)]

            for value in known_values:
                if value in elem:
                    elem.remove(value)
                    updated = True

        return updated

    def _write_known_value_from_hints_in_line(self, line: list[list | str]) -> bool:
        updated = False

        for i, elem in enumerate(line):

            if not self._is_hint(elem):
                continue

            if len(elem) == 1:
                line[i] = elem[0]
                updated = True

        return updated

    def _check_unique_value_in_hints_in_line(self, line: list[list | str]) -> bool:
        need_update = False
        for i, elem in enumerate(line):
            if not self._is_hint(elem):
                continue

            other_hints = [hint for hint in line if self._is_hint(hint) and hint is not elem]

            for n in elem:
                if all([(n not in other_hint) for other_hint in other_hints]):
                    line[i] = n
                    need_update = True

        return need_update

    def _remove_unique_pair_in_hints_in_line(self, line: list[list | str]) -> bool:
        need_update = False
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
                            need_update = True

        return need_update

    def _remove_except_unique_pair_values_in_hints_in_line(self, line: list[list | str]) -> bool:
        need_update = False
        hints: list[list] = [hint for hint in line if self._is_hint(hint)]

        possibility_indexes = {n: [] for n in '123456789'}
        for possibility in possibility_indexes:
            for i, hint in enumerate(hints):
                if possibility in hint:
                    possibility_indexes[possibility].append(i)

        pos_indexes_2 = [{pos: tuple(pos_indexes)} for pos, pos_indexes in possibility_indexes.items() if
                         len(pos_indexes) == 2]

        index_pos = {}
        for d in pos_indexes_2:
            for n, indexes in d.items():
                if not index_pos.get(indexes):
                    index_pos[indexes] = [n]
                else:
                    index_pos.get(indexes).append(n)

        for index_pair, value_pair in index_pos.items():
            if len(value_pair) != 2:
                continue
            for i in index_pair:
                for n in hints[i]:
                    if n in value_pair:
                        continue
                    hints[i].remove(n)
                    need_update = True

        return need_update

    def remove_known_values_from_hints(self, process_list: list[list]) -> bool:
        updated = False
        for line in process_list:
            updated_line = self._remove_known_values_from_line(line)
            updated = updated or updated_line
        return updated

    def write_known_value_from_hints(self, process_list: list[list]) -> bool:
        updated = False
        for line in process_list:
            updated_line = self._write_known_value_from_hints_in_line(line)
            updated = updated or updated_line
        return updated

    def check_unique_value_in_hints(self, process_list: list[list]) -> bool:
        need_update = False
        for line in process_list:
            need_line_update = self._check_unique_value_in_hints_in_line(line)
            need_update = need_update or need_line_update

        return need_update

    def remove_unique_pair_in_hints(self, process_list: list[list]) -> bool:
        need_update = False
        for line in process_list:
            need_line_update = self._remove_unique_pair_in_hints_in_line(line)
            need_update = need_update or need_line_update

        return need_update

    def remove_except_unique_pair_values_in_hints(self, process_list: list[list]) -> bool:
        need_update = False
        for line in process_list:
            need_line_update = self._remove_except_unique_pair_values_in_hints_in_line(line)
            need_update = need_update or need_line_update
        return need_update

    @staticmethod
    def make_process_list(board: list[list]) -> list:
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

    def gues(self, process_list: list[list]) -> None:

        for i, line in enumerate(process_list[:9]):
            for j, elem in enumerate(line):
                if not self._is_hint(elem):
                    continue
                for n in elem:
                    board_tmp = deepcopy(process_list[:9])
                    print(f'gues: {n=} in {elem=} in {i=} {j=} {line=}')
                    board_tmp[i][j] = n
                    tmp_solution = Solution()
                    tmp_solution.process_list = tmp_solution.make_process_list(board_tmp)

                    try:
                        tmp_solution.process_without_gues(tmp_solution.process_list)
                        print(f'unknown state')
                    except SudokuFailed:
                        print('failed')
                        process_list[i][j].remove(n)
                        self.process_without_gues(process_list)
                    except SudokuSolved as e:
                        print('solved')
                        self.process_list = tmp_solution.process_list
                        raise e

