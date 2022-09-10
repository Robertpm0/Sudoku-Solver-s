import pulp as  plp



def addSudukoConstraints(prob,gridVars,rows,cols,grids,vals):

    for row in rows:
        for col in cols:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([gridVars[row][col][value] for value in vals]),
            sense=plp.LpConstraintEQ,rhs=1,name=f"contrain_sum_{row}_{col}"))


    for row in rows:
        for value in vals:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([gridVars[row][col][value]*value for col in cols]),
            sense=plp.LpConstraintEQ,rhs=value,name=f"contrain_unique_row{row}_{value}"))


    for col in cols:
        for value in vals:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([gridVars[row][col][value]*value for row in rows]),
            sense=plp.LpConstraintEQ,rhs=value,name=f"contrain_unique_col{col}_{value}"))


    for grid in grids:
        gridRow=int(grid/3)
        gridCol=int(grid%3)

        for value in vals:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([gridVars[gridRow*3+row][gridCol*3+col][value]*value for col in range(0,3) for row in range(0,3)]),
            sense=plp.LpConstraintEQ,rhs=value,name=f"contraint_uniq_grid_{grid}_{value}"))

def addPrefilledConstraints(prob,inputSuduko,gridVars,rows,cols,vals):
    for row in rows:
        for col in cols:
            if(inputSuduko[row][col]!=0):
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([gridVars[row][col][value]*value for value in vals]),
                sense=plp.LpConstraintEQ,
                rhs=inputSuduko[row][col],
                name=f"constraint_prefilled_{row}_{col}"))

def extractSolution(gridVars,rows,cols,vals):
    solution = [[0 for col in cols] for row in rows]
    gridList =[]
    for row in rows:
        for col in cols:
            for value in vals:
                if plp.value(gridVars[row][col][value]):
                    solution[row][col]=value

    return solution


def printSolution(solution,rows,cols):
    print(f"\nFinal Result:")
    print("\n\n+ ------------- + ------- + --------+",end="")
    for row in rows:
        print("\n",end="\n| ")
        for col in cols:
            numEnd = " | " if ((col+1)%3 ==0) else "  "
            print(solution[row][col],end=numEnd)

        if ((row+1)%3 ==0):
            print("\n\n+-------------+-----------+----------+",end="") 

def solve_sudoku(inputSudoku):
    prob = plp.LpProblem("Suduko_Solver")
    objective=plp.lpSum(0)
    prob.setObjective(objective)

    rows=range(0,9)
    cols=range(0,9)
    grids=range(0,9)
    vals=range(1,10)
    gridVars=plp.LpVariable.dicts("grid_value",(rows,cols,vals),cat='Binary')
    addSudukoConstraints(prob,gridVars,rows,cols,grids,vals)
    addPrefilledConstraints(prob,inputSudoku,gridVars,rows,cols,vals)

    prob.solve()
    statuss = plp.LpStatus[prob.status]
    print(f'solution status={plp.LpStatus[prob.status]}')

    if statuss =='Optimal':
        solution = extractSolution(gridVars,rows,cols,vals)
        printSolution(solution,rows,cols)

# ENTER YOUR OWN PROBLEM HERE
sudoku_puz = [
    [8,3,0,0,5,0,7,1,0],
    [0,0,0,0,1,0,0,0,9],
    [1,0,9,6,0,8,3,0,0],
    [0,2,1,0,0,4,0,3,0],
    [9,0,0,0,6,0,0,0,2],
    [0,4,0,8,0,0,9,6,0],
    [0,0,4,5,0,3,1,0,7],
    [7,0,0,0,4,0,0,0,0],
    [0,9,5,0,7,0,0,8,4]
]

solve_sudoku(inputSudoku=sudoku_puz)

