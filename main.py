import math
import random
import sys

import numpy as np
import pygame
from numba import njit

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
DAMPING = 0.99

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ragdoll Prototype")
clock = pygame.time.Clock()


# Decorator to log execution time
def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.6f} seconds")
        return result

    return wrapper


# JIT-compiled functions
@njit
def apply_gravity_and_damping(
    positions, prev_positions, width, height, gravity, damping
):
    for i in range(len(positions)):
        # Update velocity
        vx = positions[i, 0] - prev_positions[i, 0]
        vy = positions[i, 1] - prev_positions[i, 1]

        # Store previous positions
        prev_positions[i, 0] = positions[i, 0]
        prev_positions[i, 1] = positions[i, 1]

        # Apply gravity and damping
        positions[i, 1] += gravity
        positions[i, 0] += vx * damping
        positions[i, 1] += vy * damping

        # Boundary collision
        if positions[i, 0] < 0 or positions[i, 0] > width:
            positions[i, 0] = max(0, min(width, positions[i, 0]))
            prev_positions[i, 0] = positions[i, 0]
        if positions[i, 1] < 0 or positions[i, 1] > height:
            positions[i, 1] = max(0, min(height, positions[i, 1]))
            prev_positions[i, 1] = positions[i, 1]


@njit
def apply_constraints(positions, constraints, constraint_distance):
    for constraint in constraints:
        i, j = constraint
        dx = positions[j, 0] - positions[i, 0]
        dy = positions[j, 1] - positions[i, 1]
        distance = np.sqrt(dx**2 + dy**2)
        if distance > constraint_distance:
            # Normalize the direction vector
            if distance > 0:
                dx /= distance
                dy /= distance
            # Calculate the correction needed
            correction = (distance - constraint_distance) * 0.5
            # Move parts closer
            positions[i, 0] += dx * correction
            positions[i, 1] += dy * correction
            positions[j, 0] -= dx * correction
            positions[j, 1] -= dy * correction


# Ragdoll class
class Ragdoll:
    def __init__(self, x, y):
        # Initialize parts as NumPy arrays
        self.positions = np.array(
            [
                [x, y],  # Head
                [x, y + 40],  # Torso
                [x - 30, y + 80],  # Left Arm
                [x + 30, y + 80],  # Right Arm
                [x - 20, y + 130],  # Left Leg
                [x + 20, y + 130],  # Right Leg
            ],
            dtype=np.float64,
        )

        self.prev_positions = np.copy(self.positions)
        self.sizes = np.array([20, 30, 25, 25, 25, 25])
        self.colors = np.array(
            [
                (255, 0, 0),  # Head (RED)
                (0, 0, 255),  # Torso (BLUE)
                (0, 0, 255),  # Left Arm (BLUE)
                (0, 0, 255),  # Right Arm (BLUE)
                (0, 0, 255),  # Left Leg (BLUE)
                (0, 0, 255),  # Right Leg (BLUE)
            ]
        )

        self.constraints = np.array(
            [
                (0, 1),  # Head to Torso
                (1, 2),  # Torso to Left Arm
                (1, 3),  # Torso to Right Arm
                (1, 4),  # Torso to Left Leg
                (1, 5),  # Torso to Right Leg
            ]
        )

    def __iter__(self):
        """Iterator to yield parts of the ragdoll."""
        for pos, color, size in zip(self.positions, self.colors, self.sizes):
            yield (pos, color, size)

    def generate_parts(self):
        """Generator to yield parts of the ragdoll with metadata."""
        for i, (pos, color, size) in enumerate(
            zip(self.positions, self.colors, self.sizes)
        ):
            yield {
                "index": i,
                "position": pos,
                "color": color,
                "size": size,
            }

    def update(self):
        # Apply gravity and damping
        apply_gravity_and_damping(
            self.positions, self.prev_positions, WIDTH, HEIGHT, GRAVITY, DAMPING
        )

        # Apply constraints
        apply_constraints(self.positions, self.constraints, 50)

    def draw(self, surface):
        for pos, color, size in self:
            pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), size)

        # Draw constraints
        for i, j in self.constraints:
            x1, y1 = self.positions[i]
            x2, y2 = self.positions[j]
            pygame.draw.line(
                surface,
                BLACK,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                2,
            )


# Main game loop
def main():
    ragdoll = Ragdoll(WIDTH // 2, HEIGHT // 2)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Reset ragdoll on click
                ragdoll = Ragdoll(*pygame.mouse.get_pos())

        # Update
        ragdoll.update()

        # Draw
        screen.fill(WHITE)
        ragdoll.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
