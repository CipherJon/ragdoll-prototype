import math
import random
import sys

import pygame

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


# Ragdoll class
class Ragdoll:
    def __init__(self, x, y):
        self.parts = [
            {
                "x": x,
                "y": y,
                "prev_x": x,
                "prev_y": y,
                "size": 20,
                "color": RED,
            },  # Head
            {
                "x": x,
                "y": y + 40,
                "prev_x": x,
                "prev_y": y + 40,
                "size": 30,
                "color": BLUE,
            },  # Torso
            {
                "x": x - 30,
                "y": y + 80,
                "prev_x": x - 30,
                "prev_y": y + 80,
                "size": 25,
                "color": BLUE,
            },  # Left Arm
            {
                "x": x + 30,
                "y": y + 80,
                "prev_x": x + 30,
                "prev_y": y + 80,
                "size": 25,
                "color": BLUE,
            },  # Right Arm
            {
                "x": x - 20,
                "y": y + 130,
                "prev_x": x - 20,
                "prev_y": y + 130,
                "size": 25,
                "color": BLUE,
            },  # Left Leg
            {
                "x": x + 20,
                "y": y + 130,
                "prev_x": x + 20,
                "prev_y": y + 130,
                "size": 25,
                "color": BLUE,
            },  # Right Leg
        ]
        self.constraints = [
            (0, 1),  # Head to Torso
            (1, 2),  # Torso to Left Arm
            (1, 3),  # Torso to Right Arm
            (1, 4),  # Torso to Left Leg
            (1, 5),  # Torso to Right Leg
        ]

    def update(self):
        for part in self.parts:
            # Apply gravity
            part["y"] += GRAVITY

            # Update velocity
            vx = part["x"] - part["prev_x"]
            vy = part["y"] - part["prev_y"]
            part["prev_x"] = part["x"]
            part["prev_y"] = part["y"]
            part["x"] += vx * DAMPING
            part["y"] += vy * DAMPING

            # Boundary collision
            if part["x"] < 0 or part["x"] > WIDTH:
                part["x"] = max(0, min(WIDTH, part["x"]))
                part["prev_x"] = part["x"]
            if part["y"] < 0 or part["y"] > HEIGHT:
                part["y"] = max(0, min(HEIGHT, part["y"]))
                part["prev_y"] = part["y"]

        # Apply constraints
        for i, j in self.constraints:
            part1 = self.parts[i]
            part2 = self.parts[j]
            dx = part2["x"] - part1["x"]
            dy = part2["y"] - part1["y"]
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 50:  # Constraint distance
                # Normalize the direction vector
                if distance > 0:
                    dx /= distance
                    dy /= distance
                # Calculate the correction needed
                correction = (distance - 50) * 0.5
                # Move parts closer
                part1["x"] += dx * correction
                part1["y"] += dy * correction
                part2["x"] -= dx * correction
                part2["y"] -= dy * correction

    def draw(self, surface):
        for part in self.parts:
            pygame.draw.circle(
                surface, part["color"], (int(part["x"]), int(part["y"])), part["size"]
            )

        # Draw constraints
        for i, j in self.constraints:
            part1 = self.parts[i]
            part2 = self.parts[j]
            pygame.draw.line(
                surface,
                BLACK,
                (int(part1["x"]), int(part1["y"])),
                (int(part2["x"]), int(part2["y"])),
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
