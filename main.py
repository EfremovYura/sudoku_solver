__version__ = '0.1'

import time

from solution import Solution


def main(sudoku_board: list[list]):
    """"""
    start_time = time.time()


    solution = Solution()
    solution.solve_sudoku(sudoku_board)

    print(f'{solution.is_solved(sudoku_board)=}')
    print(f'{solution.is_solved_correctly(sudoku_board)=}')
    print(*sudoku_board, sep='\n')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The task took {elapsed_time:.2f} seconds to complete.")

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
