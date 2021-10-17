from PIL import Image
from random import random

image = Image.new("RGB", (1754, 1240))  # with default black color

pixels = image.load()

maze = []
for i in range(image.width):
    maze.append([])
    for j in range(image.height):
        maze[-1].append(0 if random() < 0.76 else 1)

def at(maze, x, y):
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]):
        return 0
    return maze[x][y]

iterations = 6
for _ in range(iterations):
    new_maze = [list(row) for row in maze]

    for i in range(image.width):
        for j in range(image.height):
            total = 0
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)):
                total += at(maze, i + dx, j + dy)

            new_maze[i][j] = 0 if total <= 2 else 1

    maze = new_maze

for x in range(image.width):
    for y in range(image.height):
        pixels[(x, y)] = (0, 0, 0) if maze[x][y] == 0 else (255, 255, 255)

image.save("noise.pdf")
