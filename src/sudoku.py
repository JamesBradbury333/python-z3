from z3 import And, If, Solver, Int, Distinct, sat


def main():
    grid_cells = sudoku_grid_cells()
    # print(grid_cells)
    all_cells_rule = all_cells_1_to_9_rule(grid_cells)
    row_rule = row_1_to_9_rule(grid_cells)
    col_rule = col_1_to_9_rule(grid_cells)


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
            rule_list.append(And(cell >= 1, cell<=9))
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

    print(rule_list)
    return rule_list


# Rule for 3x3 sub-grids
def sub_boxes_rule(grid_cells):
    pass


# add problem



    





if __name__ == "__main__":
    main()
