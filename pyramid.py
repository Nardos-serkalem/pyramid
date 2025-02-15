import numpy as np
import os
import time
import math

SCREEN_SIZE = 40
SCALE = 10
ROT_SPEED = 0.1

PYRAMID_VERTICES = np.array([
    [0, 1, 0],   
    [-1, -1, -1], [1, -1, -1],  
    [1, -1, 1],  [-1, -1, 1]
])

PYRAMID_EDGES = [(0, 1), (0, 2), (0, 3), (0, 4),
                 (1, 2), (2, 3), (3, 4), (4, 1)]

theta_x, theta_y, theta_z = 0, 0, 0

def rotation_matrix_x(angle):
    return np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])


def rotation_matrix_y(angle):
    return np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

def rotation_matrix_z(angle):
    return np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

def project_3d_to_2d(points):
    projected_points = []
    for x, y, z in points:
        x_proj = int(SCREEN_SIZE // 2 + x * SCALE)
        y_proj = int(SCREEN_SIZE // 4 - y * SCALE)  
        projected_points.append((x_proj, y_proj))
    return projected_points


def render_frame(screen):
    os.system("cls")  
    for row in screen:
        print("".join(row))

def main():
    global theta_x, theta_y, theta_z

    while True:
        rotation_x = rotation_matrix_x(theta_x)
        rotation_y = rotation_matrix_y(theta_y)
        rotation_z = rotation_matrix_z(theta_z)

        rotated_vertices = []
        for vertex in PYRAMID_VERTICES:
            rotated = np.dot(rotation_x, vertex)
            rotated = np.dot(rotation_y, rotated)
            rotated = np.dot(rotation_z, rotated)
            rotated_vertices.append(rotated)

        projected_points = project_3d_to_2d(rotated_vertices)
        screen = [[" " for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE // 2)]

        for start, end in PYRAMID_EDGES:
            x1, y1 = projected_points[start]
            x2, y2 = projected_points[end]
            if 0 <= x1 < SCREEN_SIZE and 0 <= y1 < SCREEN_SIZE // 2:
                screen[y1][x1] = "#"
            if 0 <= x2 < SCREEN_SIZE and 0 <= y2 < SCREEN_SIZE // 2:
                screen[y2][x2] = "#"

        render_frame(screen)
        theta_x = (theta_x + ROT_SPEED) % (2 * math.pi)
        theta_y = (theta_y + ROT_SPEED / 2) % (2 * math.pi)
        theta_z = (theta_z + ROT_SPEED / 3) % (2 * math.pi)

        time.sleep(0.1)  
if __name__ == "__main__":
    main()

