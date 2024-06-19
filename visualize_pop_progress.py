import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import argparse
import os


# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("data_file", type=str, help="Path to the data file (CSV)")

# Parse arguments
args = parser.parse_args()

# Check if the data file exists
if not os.path.isfile(args.data_file):
    print(f"Error: The file '{args.data_file}' does not exist.")
    exit(1)


# Read the entire data file to determine the limits of the plot
data = np.genfromtxt(args.data_file, delimiter=",")
min_x, max_x = np.min(data[:, 1]), np.max(data[:, 1])
min_y, max_y = np.min(data[:, 2]), np.max(data[:, 2])
min_z, max_z = np.min(data[:, 3]), np.max(data[:, 3])
lim = max(abs(min_x), abs(max_x), abs(min_y), abs(max_y))

# To adjust the contour for a better view
best_solution = data[np.argmin(data[:, 3])]
best_x, best_y = best_solution[1], best_solution[2]


# Create a new figure and 3D axis with fixed limits
fig = plt.figure("Sphere function")
ax = fig.add_subplot(111, projection="3d")

# Configuration variables
frames_per_generation = 10
num_generations = int(np.max(data[:, 0]))  # Number of frames (generations)


# Update the plot for each frame of the animation
def update(frame):
    generation_index = frame // frames_per_generation

    ax.clear()
    ax.set_xlim(1.2 * (best_x - lim), 1.2 * (best_x + lim))
    ax.set_ylim(1.2 * (best_y - lim), 1.2 * (best_y + lim))
    ax.set_zlim(min_z, max_z * 1.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Objective Value")

    # Set camera angle (rotation)
    ax.view_init(elev=30, azim=frame)

    # Overlay a contour plot of a sphere function
    sphere_x = np.linspace(best_x - lim, best_x + lim)
    sphere_y = np.linspace(best_y - lim, best_y + lim)
    sphere_x, sphere_y = np.meshgrid(sphere_x, sphere_y)

    # Rastrigin function
    # A = 10
    # sphere_z = (
    #     (A * 2)
    #     + (
    #         (sphere_x - best_x) ** 2
    #         - A * np.cos(2 * np.pi * (sphere_x - best_x))
    #     )
    #     + (
    #         (sphere_y - best_y) ** 2
    #         - A * np.cos(2 * np.pi * (sphere_y - best_y))
    #     )
    # )

    sphere_z = (sphere_x - best_x) ** 2 + (sphere_y - best_y) ** 2
    sphere_z += best_solution[-1]

    ax.plot_surface(sphere_x, sphere_y, sphere_z, cmap="viridis", alpha=0.7)

    # Read data for the current frame
    frame_data = data[data[:, 0] == generation_index]
    if frame_data.size == 0:
        return

    best_curr_z = np.min(frame_data[:, 3])

    # Scatter plot of the population for the current frame
    ax.scatter(
        frame_data[:, 1],
        frame_data[:, 2],
        frame_data[:, 3],
        c="b",
    )

    # Add a text annotation for the generation number
    # and number of population members
    ax.text2D(
        -0.3,
        1.1,
        f"Generation: {generation_index}\nBest value: {best_curr_z}\nNum population members: {len(frame_data)}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
    )

    # # Save the current figure as an image file
    # plt.savefig(f"generation_images/generation_{generation_index:03d}.png")


# Create the animation
ani = FuncAnimation(
    fig,
    update,
    frames=num_generations * frames_per_generation,
    interval=1,
)

# # To save the animation as an mp4 file
# ffmpeg_writer = FFMpegWriter(fps=frames_per_generation * 10, bitrate=1800)
# ani.save("3d_plot_animation_IWO_with_SA_2.mp4", writer=ffmpeg_writer)

plt.show()

plt.close(fig)
