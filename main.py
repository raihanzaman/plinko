import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Game")

# Peg and ball properties
PEG_RADIUS = 5
BALL_RADIUS = 8

# Plinko board dimensions
ROWS = 14
COLS = ROWS - 1
PEG_SPACING = 40

# Gravity
GRAVITY = 1

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = 0

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

# Generate pegs in a triangle shape, excluding the top peg
pegs = []
for row in range(2, ROWS):  # Start from row 2 to exclude the top peg
    for col in range(row+1):
        x = WIDTH // 2 + (col - row / 2) * PEG_SPACING
        y = (row * PEG_SPACING + PEG_SPACING // 2 )
        pegs.append((x, y))