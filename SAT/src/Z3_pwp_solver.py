from z3 import *


def solve_pwp(WIDTH, HEIGHT, n, dimensions):

    # define a 2D-array of corners
    corners = [[Int("x_%s_%s" % (i, j)) for j in range(2)]
               for i in range(n)]

    # CORNERS CONSTRAINT: each corner must be inside the paper roll
    corner_c = [And(And(0 <= corners[i][0], corners[i][0] < WIDTH), And(0 <= corners[i][1], corners[i][1] < HEIGHT))
                for i in range(n)]

    # DIMENSIONS CONSTRAINT: each rectangle must fit inside the paper roll
    dimensions_c = [And(corners[i][0] + dimensions[i][0] <= WIDTH, corners[i][1] + dimensions[i][1] <= HEIGHT)
                    for i in range(n)]

    # OVERLAP CONSTRAINT: rectangles must not overlap
    overlap_c = [Or(Or(corners[j][0] >= corners[i][0] + dimensions[i][0], corners[j][1] >= corners[i][1] + dimensions[i][1]),
                    Or(corners[i][0] >= corners[j][0] + dimensions[j][0], corners[i][1] >= corners[j][1] + dimensions[j][1]))
                 for i in range(n) for j in range(i+1, n)]

    # sum_horizontal_c = [Sum([If(And(corners[i][1] <= k, corners[i][1] + dimensions[i][1] > k),
    #                             dimensions[i][0], 0) for i in range(n)]) <= WIDTH for k in range(HEIGHT)]

    # sum_vertical_c = [Sum([If(And(corners[i][0] <= k, corners[i][0] + dimensions[i][0] > k),
    #                           dimensions[i][1], 0) for i in range(n)]) <= HEIGHT for k in range(WIDTH)]

    s = Solver()
    s.add(corner_c + dimensions_c + overlap_c)

    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(corners[i][j]) for j in range(2)]
             for i in range(n)]
        return r
    else:
        print("failed to solve")
