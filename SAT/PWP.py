import time
import os
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import patches as patches
import src.Z3_pwp_solver as solver
import sys


def present_wrapping_problem():
    instances_directory = "src/instances"
    all_files = os.listdir(instances_directory)
    os.close

    for instance_file in all_files:
        with open(instances_directory + "/" + instance_file, "r") as file:
            solve_instance(file)


def solve_instance(file):
    start = time.time()
    content = file.readlines()
    WIDTH = int(content[0].split(" ")[0])
    HEIGHT = int(content[0].split(" ")[1])
    n = int(content[1])
    presents_dimensions = []
    for i in range(2, 2 + n):
        w = int(content[i].split(" ")[0])
        h = int(content[i].split(" ")[1])
        presents_dimensions.append([w, h])

    corners = solver.solve_pwp(WIDTH, HEIGHT, n, presents_dimensions)
    end = time.time()
    print("PAPER DIMENSIONS: " + str(WIDTH) + "x" + str(HEIGHT))
    print("Elapsed time: " + "%.2f" % (end - start) + " seconds")

    concatenation = []
    for i in range(len(corners)):
        concatenation.append([corners[i][0]] + [corners[i][1]] + [presents_dimensions[i][0]]
                             + [presents_dimensions[i][1]])

    with open("out/" + str(WIDTH) + "x" + str(HEIGHT) + "-out.txt", "w") as f:
        f.write(str(WIDTH) + " " + str(HEIGHT) + "\n")
        f.write(str(n) + "\n")
        for i in range(n):
            f.write(str(presents_dimensions[i][0]) + " " + str(presents_dimensions[i][1]) + "   "
                    + str(corners[i][0]) + " " + str(corners[i][1]) + "\n")

    draw_squares(WIDTH, HEIGHT, concatenation, n)


def draw_squares(width, height, squares_corners, n):
    colors = sns.color_palette(n_colors=n).as_hex()
    fig, ax = plt.subplots(1)
    plt.ion()
    ax.set_title(str(width) + "x" + str(height))
    ax.grid(color="black", lw=0.5)
    for i, quadruple in enumerate(squares_corners):
        color = colors[i]
        draw_rectangle(
            ax, width, height, quadruple[0].as_long(), quadruple[1].as_long(), quadruple[2], quadruple[3], color)
        fig.canvas.draw()
        fig.canvas.flush_events()

    fig.savefig("out/images/" + str(width) + "x" + str(height) + "-out.png")
    plt.close()


def draw_rectangle(ax, w, h, x, y, present_width, present_height, color):
    rect = patches.Rectangle((x, y), present_width, present_height,
                             edgecolor="black", facecolor=color, alpha=0.8)
    ax.set_xticks(range(0, w + 1, 1))
    ax.set_yticks(range(0, h + 1, 1))
    ax.add_patch(rect)


if len(sys.argv) == 1:
    present_wrapping_problem()
elif len(sys.argv) == 2:
    f = sys.argv[1]
    with open("./src/instances/" + f, "r") as file:
        solve_instance(file)
