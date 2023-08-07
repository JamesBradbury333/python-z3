from z3 import And, If, Solver, Int, Distinct, sat


def main():
    s = Solver()
    grid_cells = sudoku_grid_cells()
    all_cells_rule = all_cells_1_to_9_rule(grid_cells)
    row_rule = row_1_to_9_rule(grid_cells)
    col_rule = col_1_to_9_rule(grid_cells)
    mini_grid_rule = mini_grid_1_to_9_rule(grid_cells)
    game_rules = all_cells_rule + row_rule + col_rule + mini_grid_rule

    s.add(game_rules)

    puzzle = (
        (0, 0, 0, 0, 9, 4, 0, 3, 0),
        (0, 0, 0, 5, 1, 0, 0, 0, 7),
        (0, 8, 9, 0, 0, 0, 0, 4, 0),
        (0, 0, 0, 0, 0, 0, 2, 0, 8),
        (0, 6, 0, 2, 0, 1, 0, 5, 0),
        (1, 0, 2, 0, 0, 0, 0, 0, 0),
        (0, 7, 0, 0, 0, 0, 5, 2, 0),
        (9, 0, 0, 0, 6, 5, 0, 0, 0),
        (0, 4, 0, 9, 7, 0, 0, 0, 0),
    )
    puzzle_theorums = generate_puzzle_theorums(puzzle, grid_cells)

    s.add(puzzle_theorums)
    print(s.check())
    if s.check() == sat:
        m = s.model()
        nicer = sorted([(d, m[d]) for d in m], key=lambda x: str(x[0]))
        print(nicer)
    else:
        print("Can't solve the problem")


def sudoku_grid_cells():
    matrix = []
    for y in range(9):
        row = []
        for x in range(9):
            row.append(Int(f"cell{x,y}"))

        matrix.append(row)
    return matrix


# Rule for all cells


def all_cells_1_to_9_rule(grid_cells):
    rule_list = []
    for row in grid_cells:
        for cell in row:
            rule_list.append(And(cell >= 1, cell <= 9))
    return rule_list


# Rule for rows
def row_1_to_9_rule(grid_cells):
    rule_list = []
    for row in grid_cells:
        rule = Distinct(*row)
        rule_list.append(rule)
    return rule_list


# Rule for columns
def col_1_to_9_rule(grid_cells):
    rule_list = []
    for x in range(9):
        col_list = []
        for y in range(9):
            col_list.append(grid_cells[y][x])
        rule_list.append(Distinct(col_list))
    return rule_list


# Rule for 3x3 sub-grids
def mini_grid_1_to_9_rule(grid_cells):
    rule_list = []
    for iprime in range(3):
        for jprime in range(3):
            mini_grid_cells = []
            for i in range(3):
                for j in range(3):
                    mini_grid_cells.append(grid_cells[3 * iprime + i][3 * jprime + j])
            rule_list.append(Distinct(*mini_grid_cells))
    return rule_list


# add problem
def generate_puzzle_theorums(puzzle: list[list], grid_cells):
    return [
        If(puzzle[i][j] == 0, True, grid_cells[i][j] == puzzle[i][j])
        for i in range(9)
        for j in range(9)
    ]


if __name__ == "__main__":
    main()
