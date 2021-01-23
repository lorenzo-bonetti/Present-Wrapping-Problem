import time
from minizinc import Instance, Model, Solver
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys


def present_wrapping_problem():
    model_path = "src/Project.mzn"
    pwp = Model(model_path)
    instances_directory = "src/Instances"
    gecode = Solver.lookup("gecode")
    all_files = os.listdir(instances_directory)
    os.close

    for instance_file in all_files:
        instance = Instance(gecode, pwp)
        with open(instances_directory + "/" + instance_file, "r") as file:
            solve_instance(instance, file)


def draw_squares(width, height, squares_corners, n):
    colors = sns.color_palette(n_colors=n).as_hex()
    fig, ax = plt.subplots(1)
    plt.ion()
    ax.set_title(str(width) + "x" + str(height))
    ax.grid(color="black", lw=0.5)
    for i, quadruple in enumerate(squares_corners):
        color = colors[i]
        draw_rectangle(ax, width, height, quadruple[0], quadruple[1], quadruple[2], quadruple[3], color)
        fig.canvas.draw()
        fig.canvas.flush_events()

    fig.savefig("out/images/" + str(width) + "x" + str(height) + "-out.png")
    plt.close()


def draw_rectangle(ax, w, h, x, y, present_width, present_height, color):
    rect = patches.Rectangle((x, y), present_width, present_height, edgecolor="black", facecolor=color, alpha=0.8)
    ax.set_xticks(range(0, w + 1, 1))
    ax.set_yticks(range(0, h + 1, 1))
    ax.add_patch(rect)


def solve_instance(instance, file):
    start = time.time()
    content = file.readlines()
    width = int(content[0].split(" ")[0])
    height = int(content[0].split(" ")[1])
    n = int(content[1])
    presents_dimensions = []
    for i in range(2, 2 + n):
        w = int(content[i].split(" ")[0])
        h = int(content[i].split(" ")[1])
        presents_dimensions.append([w, h])

    instance["WIDTH"] = width
    instance["HEIGHT"] = height
    instance["n"] = n
    instance["presents_dimensions"] = presents_dimensions
    instance["durations_x"] = [width] * n
    instance["durations_y"] = [height] * n
    result = instance.solve()
    end = time.time()
    corners_x = result["corners_x"]
    corners_y = result["corners_y"]
    print("PAPER DIMENSIONS: " + str(width) + "x" + str(height))
    print("Elapsed time: " + "%.2f" % (end - start) + " seconds")
    concatenation = []
    for i in range(len(corners_x)):
        concatenation.append([corners_x[i]] + [corners_y[i]] + [presents_dimensions[i][0]]
                             + [presents_dimensions[i][1]])

    with open("out/" + str(width) + "x" + str(height) + "-out.txt", "w") as f:
        f.write(str(width) + " " + str(height) + "\n")
        f.write(str(n) + "\n")
        for i in range(n):
            f.write(str(presents_dimensions[i][0]) + " " + str(presents_dimensions[i][1]) + "   "
                    + str(corners_x[i]) + " " + str(corners_y[i]) + "\n")

    draw_squares(width, height, concatenation, n)


if len(sys.argv) == 1:
    present_wrapping_problem()
elif len(sys.argv) == 2:
    f = sys.argv[1]
    instance = Instance(Solver.lookup("gecode"), Model("./src/Project.mzn"))
    with open("./src/Instances/" + f, "r") as file:
        solve_instance(instance, file)


