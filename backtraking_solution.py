from time import time


def solve(board: list[list]) -> bool:
    """With recursion try to insert num to empty fields. If board not solved field return 0 value."""
    empty_indexes = find_empty(board)

    if not empty_indexes:
        return True

    row, col = empty_indexes

    for num in range(1, 10):
        if valid(board, num, empty_indexes):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False


def valid(board: list[list], num: int, pos: tuple) -> bool:
    """Check rows, columns, boxes if num conflicts with other fields """
    # Check row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for line_index in range(len(board)):
        if board[line_index][pos[1]] == num and pos[0] != line_index:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(board: list[list]) -> None:
    """Print board with separators"""
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def find_empty(matrix: list[list]) -> None | tuple:
    """Find board indexes for empty field (=0) """
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return i, j  # row, col

    return None


if __name__ == "__main__":
    # board = [
    #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
    #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
    #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
    #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
    #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
    #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
    #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
    #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
    #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
    # ]
    # board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
    #          ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    #          [".", "9", "8", ".", ".", ".", ".", "6", "."],
    #          ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    #          ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    #          ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    #          [".", "6", ".", ".", ".", ".", "2", "8", "."],
    #          [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    #          [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

    board = [["3", ".", ".", ".", ".", ".", ".", ".", "9"],
             [".", ".", ".", ".", "7", ".", "1", ".", "2"],
             [".", ".", ".", ".", ".", "9", "5", ".", "."],
             [".", "7", ".", ".", "5", ".", ".", ".", "."],
             ["1", ".", ".", "4", ".", ".", "6", "8", "."],
             [".", ".", "6", ".", ".", ".", ".", ".", "."],
             ["7", "1", ".", ".", "9", ".", ".", ".", "5"],
             [".", ".", ".", ".", ".", "3", "8", ".", "."],
             ["4", ".", ".", ".", ".", ".", ".", "2", "."]]

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
    #
    for line in board:
        for j, elem in enumerate(line):
            line[j] = 0 if elem == '.' else int(elem)

    print_board(board)
    start_time = time()

    solve(board)

    end_time = time()

    print("___________________")
    print("")
    print_board(board)

    elapsed_time = end_time - start_time

    print(f"The task took {elapsed_time:.2f} seconds to complete.")
